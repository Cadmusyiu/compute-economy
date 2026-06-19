#!/usr/bin/env python3
"""
compute-economy: Daily GPU Price Collection Script

Collects public GPU pricing data from multiple sources.
Runs daily via cron job to build time series.

Sources:
- GPU Tracker (gputracker.dev) — public listing stats
- Yahoo Finance — NVDA, BTC, macro tickers
- SemiAnalysis — public pricing preview (weekly scrape)
"""

import json
import csv
import os
import subprocess
import urllib.request
import ssl
from datetime import datetime, timezone
from pathlib import Path

# === Config ===
DATA_DIR = Path(__file__).resolve().parent.parent / "raw_data"
DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "dashboard"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DIR, exist_ok=True)

# === Data Fetch Functions ===

def fetch_gputracker():
    """Fetch public GPU listing stats from gputracker.dev"""
    url = "https://gputracker.dev/"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        
        import re
        stats = {}
        
        # Look for listing counts
        listing_match = re.search(r'(\d[\d,]*)\s*listings?', html, re.IGNORECASE)
        if listing_match:
            stats["total_listings"] = int(listing_match.group(1).replace(",", ""))
        
        # Look for price ranges — filter realistic H100 rates (>$0.50/hr)
        price_matches = re.findall(r'\$\s*(\d+\.\d+)\s*/\s*hr', html)
        if price_matches:
            prices = [float(p) for p in price_matches if float(p) > 0.5]
            if prices:
                stats["min_price_hr"] = min(prices)
                stats["max_price_hr"] = max(prices)
                stats["avg_price_hr"] = round(sum(prices) / len(prices), 2)
        
        # GPU model counts
        gpu_models = re.findall(r'(H100|A100|B200|H200|A6000|RTX 4090|RTX 5090)[^<]*', html)
        stats["gpu_models_found"] = list(set(gpu_models))
        
        stats["fetch_time_utc"] = datetime.now(timezone.utc).isoformat()
        stats["source"] = "gputracker.dev"
        
        return stats
    except Exception as e:
        return {"error": str(e), "source": "gputracker.dev", "fetch_time_utc": datetime.now(timezone.utc).isoformat()}


def fetch_yfinance_tickers(tickers=["NVDA", "BTC-USD", "GC=F", "NG=F", "DX-Y.NYB"]):
    """Fetch closing prices for correlation tickers via yfinance"""
    stats = {}
    stats["fetch_time_utc"] = datetime.now(timezone.utc).isoformat()
    stats["source"] = "yfinance"
    stats["tickers"] = {}
    
    # Try using subprocess to call yfinance
    try:
        result = subprocess.run(
            ["python3", "-c", f"""
import json, yfinance as yf
tickers = {json.dumps(tickers)}
data = {{}}
for t in tickers:
    try:
        stock = yf.Ticker(t)
        hist = stock.history(period="5d")
        if not hist.empty:
            data[t] = {{
                "close": float(hist["Close"].iloc[-1]),
                "prev_close": float(hist["Close"].iloc[-2]) if len(hist) > 1 else None,
                "date": str(hist.index[-1].date())
            }}
    except Exception as e:
        data[t] = {{"error": str(e)}}
print(json.dumps(data, default=str))
"""],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout:
            stats["tickers"] = json.loads(result.stdout.strip())
    except Exception as e:
        stats["error"] = str(e)
    
    return stats


def save_data(source_name: str, data: dict):
    """Save fetched data to JSON file"""
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = DATA_DIR / f"{source_name}_{date_str}.json"
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"  ✅ Saved: {filename}")
    return filename


def append_to_timeseries(data: dict):
    """Append today's data to the master timeseries CSV"""
    csv_path = DATA_DIR.parent / "gpu_price_timeseries.csv"
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    row = {
        "date": date_str,
        "H100_min": data.get("gputracker", {}).get("min_price_hr"),
        "H100_median": data.get("gputracker", {}).get("avg_price_hr"),
        "H100_p25": None,
        "listings_count": data.get("gputracker", {}).get("total_listings"),
        "SA_H100_spot": None,
        "NVDA": None,
        "BTC": None,
    }
    
    # Add ticker data — map to existing column names
    tickers = data.get("yfinance", {}).get("tickers", {})
    for t, v in tickers.items():
        if isinstance(v, dict) and "close" in v:
            ticker_key = t.replace("-USD", "").replace("=F", "")
            if ticker_key == "NVDA":
                row["NVDA"] = v["close"]
            elif ticker_key == "BTC":
                row["BTC"] = v["close"]
    
    # Write CSV (append or create)
    fieldnames = ["date", "H100_min", "H100_median", "H100_p25", "listings_count", "SA_H100_spot", "NVDA", "BTC"]
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    
    print(f"  ✅ Timeseries appended: {csv_path}")


def main():
    print("=" * 50)
    print(f"Compute Economy Daily Collector — {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 50)
    
    # 1. Fetch GPU Tracker
    print("\n📡 Fetching GPU Tracker...")
    gputracker_data = fetch_gputracker()
    save_data("gputracker", gputracker_data)
    
    # 2. Fetch YFinance tickers
    print("\n📈 Fetching YFinance tickers...")
    yfinance_data = fetch_yfinance_tickers()
    save_data("yfinance", yfinance_data)
    
    # 3. Merge and save timeseries
    combined = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "gputracker": gputracker_data,
        "yfinance": yfinance_data,
    }
    
    append_to_timeseries(combined)
    
    print("\n" + "=" * 50)
    print("✅ Daily collection complete!")
    print("=" * 50)
    
    # Quick summary
    print("\n📊 Quick Summary:")
    if "avg_price_hr" in gputracker_data:
        print(f"  H100 Avg Spot: ${gputracker_data['avg_price_hr']}/hr")
    if "total_listings" in gputracker_data:
        print(f"  Total Listings: {gputracker_data['total_listings']}")
    if "tickers" in yfinance_data:
        for t, v in yfinance_data["tickers"].items():
            if isinstance(v, dict) and "close" in v:
                print(f"  {t}: ${v['close']:.2f}")


if __name__ == "__main__":
    main()
