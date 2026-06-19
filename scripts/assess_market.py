#!/usr/bin/env python3
"""
compute-economy: Market Assessment Script

Analyzes collected GPU pricing data and produces:
- Current market regime classification
- Trend analysis
- Key indicators with status (normal/warning/alert)
- Short narrative assessment
"""

import json
import csv
import os
import statistics
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "raw_data"
TSV_PATH = DATA_DIR.parent / "gpu_price_timeseries.csv"
ASSESSMENT_PATH = DATA_DIR.parent / "ASSESSMENT.md"

# === Indicators ===

INDICATORS = {
    "H100_median": {
        "name": "H100 Spot Price",
        "unit": "$/hr",
        "alert_high": 5.0,
        "warn_high": 4.0,
        "warn_low": 1.50,
        "alert_low": 1.0,
        "description": "Market-clearing spot rental price for H100 GPUs"
    },
    "listings_count": {
        "name": "GPU Tracker Listings",
        "unit": "count",
        "description": "Number of GPU rental listings — proxy for supply liquidity",
        "trend_reversed": True  # ↓ = bearish for supply
    },
}

ALERT_THRESHOLDS = {
    "h100_spot_high": {"value": 5.0, "label": "🔴 Demand Spike"},
    "h100_spot_low": {"value": 1.50, "label": "🟡 Supply Glut"},
    "listing_drop_7d": {"pct": 20, "label": "🟡 Supply Tightening"},
}


def load_timeseries():
    """Load the timeseries CSV into a list of dicts"""
    rows = []
    if not os.path.isfile(TSV_PATH):
        return rows
    
    with open(TSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def classify_regime(h100_spot):
    """Classify current market regime based on H100 spot price"""
    if h100_spot is None or h100_spot == 0:
        return "UNKNOWN", "Insufficient data"
    
    if h100_spot > 5:
        return "BULL", f"Demand surge — H100 ${h100_spot:.2f}/hr (above $5 alert)"
    elif h100_spot > 3.5:
        return "TIGHT", f"Above-average demand — H100 ${h100_spot:.2f}/hr"
    elif h100_spot > 2.0:
        return "NEUTRAL", f"Normal range — H100 ${h100_spot:.2f}/hr"
    elif h100_spot > 1.0:
        return "WEAK", f"Below-average — H100 ${h100_spot:.2f}/hr"
    else:
        return "GLUT", f"Supply glut — H100 ${h100_spot:.2f}/hr (below $1.50 warn)"


def compute_trend(rows, field="H100_median", window=7):
    """Compute price trend over a rolling window"""
    vals = []
    for r in rows[-window:]:
        try:
            v = float(r.get(field, "") or 0)
            if v > 0:
                vals.append(v)
        except (ValueError, TypeError):
            continue
    
    if len(vals) < 3:
        return None, "insufficient_data"
    
    n = len(vals)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(vals) / n
    
    num = sum((x[i] - x_mean) * (vals[i] - y_mean) for i in range(n))
    den = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if den == 0:
        return None, "flat"
    
    slope = num / den
    
    if slope > 0.05:
        direction = "🟢 RISING"
    elif slope < -0.05:
        direction = "🔴 FALLING"
    else:
        direction = "⚪ FLAT"
    
    return slope, direction


def check_alerts(rows):
    """Check all alert conditions"""
    alerts = []
    
    if not rows:
        return alerts
    
    latest = rows[-1]
    
    try:
        h100_spot = float(latest.get("H100_median", "") or 0)
    except (ValueError, TypeError):
        h100_spot = None
    
    if h100_spot and h100_spot > ALERT_THRESHOLDS["h100_spot_high"]["value"]:
        alerts.append({
            "level": "🔴",
            "indicator": "H100 Spot",
            "message": f"${h100_spot:.2f}/hr exceeds alert threshold ${ALERT_THRESHOLDS['h100_spot_high']['value']}/hr",
            "label": ALERT_THRESHOLDS["h100_spot_high"]["label"]
        })
    
    if h100_spot and h100_spot < ALERT_THRESHOLDS["h100_spot_low"]["value"]:
        alerts.append({
            "level": "🟡",
            "indicator": "H100 Spot",
            "message": f"${h100_spot:.2f}/hr below warning threshold ${ALERT_THRESHOLDS['h100_spot_low']['value']}/hr",
            "label": ALERT_THRESHOLDS["h100_spot_low"]["label"]
        })
    
    # Check 7-day listing drop
    if len(rows) >= 2:
        try:
            latest_listings = float(latest.get("listings_count", "") or 0)
            oldest = rows[-min(len(rows), 7)]
            oldest_listings = float(oldest.get("listings_count", "") or 0)
            
            if oldest_listings > 0:
                drop_pct = (oldest_listings - latest_listings) / oldest_listings * 100
                if drop_pct > ALERT_THRESHOLDS["listing_drop_7d"]["pct"]:
                    alerts.append({
                        "level": "🟡",
                        "indicator": "GPU Listings",
                        "message": f"Listings dropped {drop_pct:.1f}% in {(min(len(rows), 7))} days",
                        "label": ALERT_THRESHOLDS["listing_drop_7d"]["label"]
                    })
        except (ValueError, TypeError):
            pass
    
    return alerts


def generate_assessment(rows):
    """Generate full market assessment report"""
    if not rows:
        return "# Compute Economy Assessment\n\nNo data collected yet."
    
    latest = rows[-1]
    
    try:
        h100_spot = float(latest.get("H100_median", "") or 0)
    except (ValueError, TypeError):
        h100_spot = None
    
    # Regime classification
    regime, regime_detail = classify_regime(h100_spot)
    
    # Trend
    slope, direction = compute_trend(rows)
    
    # Alerts
    alerts = check_alerts(rows)
    
    # Build report
    report = []
    report.append("# 🔍 Compute Economy Assessment\n")
    report.append(f"> Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")
    report.append(f"> Data points: {len(rows)} days\n")
    
    # Summary
    report.append("## 📊 Summary\n")
    report.append(f"**Regime:** {regime}")
    if regime_detail:
        report.append(f" | *{regime_detail}*")
    report.append("\n\n")
    
    if direction:
        report.append(f"**Trend:** {direction}")
        if slope:
            report.append(f" ({slope:.4f}/day)")
    report.append("\n\n")
    
    # Alerts
    if alerts:
        report.append("## ⚠️ Active Alerts\n")
        for a in alerts:
            report.append(f"- {a['level']} **{a['label']}**: {a['message']}")
        report.append("\n")
    else:
        report.append("## ✅ No Active Alerts\n\n")
    
    # Key Indicators
    report.append("## 📈 Key Indicators\n\n")
    report.append("| Indicator | Value | Status |\n")
    report.append("|:----------|:------|:------|\n")
    
    if h100_spot and h100_spot > 0:
        if h100_spot > 5.0:
            status = "🔴 Alert"
        elif h100_spot > 3.5:
            status = "🟡 Elevated"
        elif h100_spot > 2.0:
            status = "🟢 Normal"
        elif h100_spot > 1.0:
            status = "🟡 Weak"
        else:
            status = "🔴 Glut"
        report.append(f"| H100 Spot | ${h100_spot:.2f}/hr | {status} |\n")
    else:
        report.append(f"| H100 Spot | No data | ⚪ Pending |\n")
    
    if "listings_count" in latest:
        try:
            listings = float(latest.get("listings_count", "") or 0)
            if listings > 0:
                report.append(f"| GPU Listings | {int(listings):,} | — |\n")
        except (ValueError, TypeError):
            pass
    
    for ticker in ["NVDA", "BTC"]:
        if ticker in latest:
            try:
                val = float(latest.get(ticker, "") or 0)
                if val > 0:
                    label = ticker
                    if ticker == "BTC":
                        label = "Bitcoin"
                    report.append(f"| {label} | ${val:,.2f} | — |\n")
            except (ValueError, TypeError):
                pass
    
    report.append("\n")
    
    # Narrative
    report.append("## 📝 Narrative\n\n")
    
    if h100_spot and h100_spot > 0:
        if h100_spot > 4:
            report.append(f"H100 spot at **${h100_spot:.2f}/hr** signals elevated demand.")
            report.append(" The compute market remains supply-constrained.")
            report.append(" NVDA tailwinds intact. Monitor for further tightening.\n")
        elif h100_spot > 2.5:
            report.append(f"H100 spot at **${h100_spot:.2f}/hr** is in the normal range.")
            report.append(" Market is balanced. No extreme signals.\n")
        elif h100_spot > 1.5:
            report.append(f"H100 spot at **${h100_spot:.2f}/hr** is below average.")
            report.append(" Supply is adequate. Watch for further softening.\n")
        else:
            report.append(f"H100 spot at **${h100_spot:.2f}/hr** indicates supply glut.")
            report.append(" Excess compute capacity available. Bearish for GPU pricing.\n")
    else:
        report.append("H100 spot price data is still being collected.")
        report.append(" The GPU Tracker site was unreachable during this collection cycle.\n")
        report.append(" Will retry on next cycle.\n")
    
    report.append("\n")
    
    # Next actions
    report.append("## 🎯 Next Actions\n\n")
    if regime in ("BULL", "TIGHT"):
        report.append("- [ ] Monitor for supply constraints (Reddit/HN chatter)\n")
        report.append("- [ ] Check if hyperscalers are buying spot (volume spike)\n")
        report.append("- [ ] Watch NVDA earnings impact\n")
    elif regime in ("GLUT", "WEAK"):
        report.append("- [ ] Check if this is seasonal or structural\n")
        report.append("- [ ] Look for enterprise demand signals\n")
        report.append("- [ ] Consider short NVDA / long compute thesis\n")
    else:
        report.append("- [x] Fix GPU Tracker data source connection\n")
        report.append("- [ ] Continue daily data collection\n")
        report.append("- [ ] Add more data sources\n")
    
    report.append("\n---\n")
    report.append(f"*Auto-generated by compute-economy assessment engine*\n")
    
    return "".join(report)


def main():
    print("=" * 50)
    print("Compute Economy — Market Assessment Engine")
    print("=" * 50)
    
    rows = load_timeseries()
    print(f"Loaded {len(rows)} data points from timeseries\n")
    
    report = generate_assessment(rows)
    
    with open(ASSESSMENT_PATH, "w") as f:
        f.write(report)
    
    print(f"✅ Assessment saved: {ASSESSMENT_PATH}")
    print("\n" + "=" * 50)
    print(report[:500])
    print("...")


if __name__ == "__main__":
    main()
