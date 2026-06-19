# 🔍 Compute Economy Dashboard v1 — Assessment
> Generated: 2026-06-19 21:32 HKT
> Data: GPU Tracker (gputracker.dev) | Macro: yfinance | History: SemiAnalysis

## 📊 Summary

**Regime:** BULL — H100 spot at **$8.97/hr** (above $5 alert threshold)

**Trend:** ⚠️ DEMAND SURGE — 3.2x above Apr 2026 low of $2.82/hr

---

## 📈 Plots Generated

### 1. H100 Historical Trend (2023–2026)
![H100 Historical Trend](plots/h100_historical_trend.png)
- **Interactive HTML**: `dashboard/plots/h100_historical_trend.html`
- SemiAnalysis data points overlaid with current GPU Tracker pricing
- From $3.05 (2023 H1) → $6.62 peak (2023 H2) → $2.82 (Apr 2026 trough) → $8.97 (Now)
- March 2026 marked "Sold Out" — demand outstripping supply

### 2. GPU Generation Comparison
![GPU Generation Comparison](plots/gpu_gen_comparison.png)
- **Interactive HTML**: `dashboard/plots/gpu_gen_comparison.html`
- Log-scale bar chart: H100 → H200 → B200 → B300 → GB200
- B200 median: $19.56/hr (+118% vs H100)
- GB200 median: $64.00/hr (+613% vs H100)

### 3. H100 Price Spread by Provider
![H100 Price Spread](plots/h100_spread.png)
- **Interactive HTML**: `dashboard/plots/h100_spread.html`
- Provider-by-provider min–max–median breakdown
- Verda cheapest spot: $0.80/hr vs GCP max: $97.44/hr
- **121x spread** — insane market inefficiency

---

## 🏷️ Key Indicators

| Indicator | Value | Status |
|:----------|:------|:------|
| H100 Median Spot | **$8.97/hr** | 🔴 Alert (>$5) |
| H100 Cheapest Spot | $0.80/hr (Verda) | 🟢 Bargain |
| H100 Most Expensive | $97.44/hr (GCP) | 🔴 Hyperscaler tax |
| NVDA | **$210.69** | — |
| Bitcoin | **$62,478** | — |
| USD Index | 100.76 | — |
| Gold | $4,174.60/oz | — |
| Natural Gas | $3.20 | — |

## 📝 Narrative

The compute market is experiencing a **sharp demand surge**. H100 spot at $8.97/hr represents a **218% premium** over the April 2026 trough of $2.82/hr — and the market was already "Sold Out" in March. This is not normal seasonality.

**Key observations:**
1. **Supply crunch confirmed**: March sold-out status + 3.2x price surge = genuine capacity constraints
2. **Market inefficiency extreme**: 121x price spread between cheapest and most expensive H100 listing
3. **NVDA correlation**: NVDA at $210.69, likely to benefit from compute demand tightening
4. **Gen-on-gen premium**: Each new GPU generation commands 33–118% premium over previous

**What to watch:**
- H100 median crossing $10/hr would signal full-blown shortage
- B200/B300 availability — Blackwell ramp could relieve H100 pressure
- Hyperscaler capex announcements — are they adding capacity fast enough?

---

## 🎯 Next Actions

- [ ] Track H100 daily: watch for $10/hr breach
- [ ] Monitor NVDA options flow for institutional sentiment
- [ ] Compare with SemiAnalysis subscriber data if trial access obtained
- [ ] Add B200/B300 time series as GPU Tracker updates

---

## 📁 Data Files

| File | Description | Size |
|:-----|:------------|:-----|
| `raw_data/macro_30d_history.csv` | 30d history for NVDA, BTC-USD, DX-Y.NYB, NG=F, GC=F | 2.8 KB |
| `raw_data/nvda_5yr_history.csv` | 5 years of NVDA daily closes (1,255 rows) | 56 KB |
| `raw_data/gputracker_2026-06-19.json` | Full GPU Tracker snapshot | 4.4 KB |
| `raw_data/semianalysis_2026-06-19.md` | SemiAnalysis research notes | 3.7 KB |

## 📁 Plot Files

| Plot | HTML | PNG | 
|:-----|:-----|:----|
| H100 Historical Trend | ✅ 9.3 KB | ✅ 140 KB |
| GPU Generation Comparison | ✅ 9.4 KB | ✅ 97 KB |
| H100 Price Spread | ✅ 10.6 KB | ✅ 112 KB |

---
*Dashboard v1 complete. Ready for presentation.*
