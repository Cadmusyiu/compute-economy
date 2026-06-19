#!/usr/bin/env python3
"""
GPU Market Data Collector — Daily Snapshot
Collects publicly available GPU pricing data + macro indicators
Appends to CSV for time-series analysis
"""

import csv
import json
import os
import urllib.request
from datetime import datetime, timezone, timedelta

HKT = timezone(timedelta(hours=8))
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(DATA_DIR, "gpu_price_timeseries.csv")
NOTES_PATH = os.path.join(DATA_DIR, "daily_notes.md")

def fetch_url(url, headers=None):
    """Fetch URL with timeout and error handling"""
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERROR: {e}"

def extract_gputracker_stats():
    """Extract GPU Tracker public stats"""
    html = fetch_url("https://gputracker.dev/gpu-cloud-statistics-2026")
    if html.startswith("ERROR"):
        return {"H100_min": None, "H100_median": None, "H100_p25": None, "H100_max": None,
                "B200_min": None, "listings_count": None}
    
    import re
    data = {}
    
    # H100 pricing
    m = re.search(r'\$([\d.]+)/hr.*?cheapest.*?H100', html, re.DOTALL)
    if m: data["H100_min"] = float(m.group(1))
    
    m = re.search(r'\$([\d.]+)/hr.*?median.*?H100', html, re.DOTALL)
    if m: data["H100_median"] = float(m.group(1))
    
    m = re.search(r'\$([\d.]+)/hr.*?25th.*?H100', html, re.DOTALL)
    if m: data["H100_p25"] = float(m.group(1))
    
    m = re.search(r'(\d+)\s*Live listings', html, re.DOTALL)
    if m: data["listings_count"] = int(m.group(1))
    
    return data

def extract_semianalysis_data():
    """Extract H100 spot price from SemiAnalysis preview"""
    html = fetch_url("https://api.semianalysis.com/dashboards/gpu_spot_pricing_preview/")
    if html.startswith("ERROR"):
        return {"SA_H100_spot": None, "SA_H100_1y": None}
    
    import re
    data = {}
    
    # H100 spot (Apr 2026 row)
    m = re.search(r'H100.*?Apr\s+2026\s*\$?([\d.]+)', html)
    if m: data["SA_H100_spot"] = float(m.group(1))
    
    # H100 1-year contract
    m = re.search(r'H100.*?Apr\s+2026\s*\$?[\d.]+.*?\$?([\d.]+)-?\$?([\d.]*)', html)
    if m:
        # Find the 1y column - harder to parse from HTML
        pass
    
    return data

def main():
    now = datetime.now(HKT)
    date_str = now.strftime("%Y-%m-%d")
    
    print(f"=== GPU Data Collection for {date_str} ===")
    
    # 1. GPU Tracker stats
    gputracker = extract_gputracker_stats()
    print(f"GPU Tracker:")
    for k, v in gputracker.items():
        print(f"  {k}: {v}")
    
    # 2. SemiAnalysis
    sa_data = extract_semianalysis_data()
    print(f"\nSemiAnalysis:")
    for k, v in sa_data.items():
        print(f"  {k}: {v}")
    
    # 3. NVDA price
    # Free alternative: Yahoo Finance scrape (no API key needed)
    yahoo_url = "https://query1.finance.yahoo.com/v8/finance/chart/NVDA?interval=1d"
    html = fetch_url(yahoo_url, {"User-Agent": "Mozilla/5.0"})
    nvda_price = None
    if not html.startswith("ERROR"):
        try:
            data = json.loads(html)
            meta = data.get("chart", {}).get("result", [{}])[0].get("meta", {})
            nvda_price = meta.get("regularMarketPrice")
        except:
            pass
    print(f"\nNVDA: {nvda_price}")
    
    # 4. BTC price
    btc_url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"
    html = fetch_url(btc_url)
    btc_price = None
    if not html.startswith("ERROR"):
        try:
            data = json.loads(html)
            btc_price = float(data["bpi"]["USD"]["rate"].replace(",", ""))
        except:
            pass
    print(f"BTC: {btc_price}")
    
    # Append to CSV
    headers = ["date", "H100_min", "H100_median", "H100_p25", "listings_count",
               "SA_H100_spot", "NVDA", "BTC"]
    
    row = {
        "date": date_str,
        "H100_min": gputracker.get("H100_min"),
        "H100_median": gputracker.get("H100_median"),
        "H100_p25": gputracker.get("H100_p25"),
        "listings_count": gputracker.get("listings_count"),
        "SA_H100_spot": sa_data.get("SA_H100_spot"),
        "NVDA": nvda_price,
        "BTC": btc_price
    }
    
    file_exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    
    print(f"\n✅ Appended to {CSV_PATH}")
    
    # Update daily notes
    # Format BTC price string
    btc_str = f"${btc_price:,.0f}" if btc_price else "N/A"
    nvda_str = f"${nvda_price:.2f}" if nvda_price else "N/A"
    h100_min = gputracker.get("H100_min") if gputracker.get("H100_min") else "N/A"
    h100_med = gputracker.get("H100_median") if gputracker.get("H100_median") else "N/A"
    h100_p25 = gputracker.get("H100_p25") if gputracker.get("H100_p25") else "N/A"
    listings = gputracker.get("listings_count") if gputracker.get("listings_count") else "N/A"
    
    note = (
        f"\n## {date_str}\n"
        f"- H100 spot: ${h100_min}/hr (min) | ${h100_med}/hr (median)\n"
        f"- H100 P25: ${h100_p25}/hr\n"
        f"- Listings: {listings}\n"
        f"- NVDA: {nvda_str}\n"
        f"- BTC: {btc_str}\n"
    )
    
    with open(NOTES_PATH, "a") as f:
        f.write(note)
    
    print(f"✅ Notes appended to {NOTES_PATH}")

if __name__ == "__main__":
    main()
