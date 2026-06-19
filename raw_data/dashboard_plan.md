# Dashboard v1 Plan — Day 3 (Jun 20)
> Purpose: Build interactive dashboard for compute price tracking

## Dashboard Layout

### Sheet 1: GPU Price Tracker (Daily Snapshot)
| Column | Source | Type | Notes |
|:-------|:-------|:-----|:------|
| Date | Auto | Date | Daily |
| H100 Spot (min) | GPU Tracker | $/hr | Cheapest listing |
| H100 Spot (median) | GPU Tracker | $/hr | Market center |
| H100 Spot (max) | GPU Tracker | $/hr | Most expensive |
| H100 P25 | GPU Tracker | $/hr | 25th percentile |
| H100 On-Demand (min) | GPU Tracker | $/hr | Cheapest on-demand |
| H100 Listings Count | GPU Tracker | count | Supply indicator |
| H200 Spot (median) | GPU Tracker | $/hr | Next-gen comparison |
| B200 Spot (median) | GPU Tracker | $/hr | Blackwell comparison |
| H100 1yr Contract | SemiAnalysis | $/hr | Contract discount |
| A100 Spot (median) | GPU Tracker | $/hr | Legacy comparison |

### Sheet 2: Macro Correlates
| Column | Source | Frequency | Notes |
|:-------|:-------|:----------|:------|
| Date | Auto | Daily | |
| NVDA Close | Yahoo Finance | Daily | NVIDIA stock |
| BTC/USD | CoinDesk | Daily | Crypto correlator |
| USD Index | Yahoo Finance | Daily | DXY |
| Natural Gas | Yahoo Finance | Daily | Energy cost proxy |

### Sheet 3: Derived Metrics
| Metric | Formula | Purpose |
|:-------|:--------|:--------|
| H100 Spread Ratio | Max/Min | Market efficiency |
| NVDA/H100 Ratio | $NVDA / H100 spot | Compute value vs stock |
| Generation Premium | B200 median / H100 median | Adoption rate proxy |
| Spot/Contract Spread | Spot - 1yr Contract | Supply tightness signal |
| Hyperscaler Premium | Hyperscaler min / Marketplace min | Platform pricing power |

## Correlation Pairs to Plot

### Primary (High Interest)
1. **H100 Spot Price vs NVDA Stock Price** — Does compute cost lead or lag NVIDIA stock?
2. **H100 Spot Price vs BTC Price** — Crypto mining → AI compute spillover?
3. **H100 Spot Price vs DXY (USD Index)** — USD strength vs hardware cost proxy

### Secondary
4. **H100 Listings Count vs Price** — Supply-demand relationship
5. **H100 Spot vs 1yr Contract** — "Compute yield curve" slope
6. **H100 vs A100 Pricing** — Generation substitution effect
7. **H200 vs H100 Pricing** — Technology premium over time

### Macro
8. **GPU Composite Index vs Natural Gas** — Energy vs compute cost
9. **GPU Composite Index vs NVDA** — Overall market health

## Data Gaps to Fill Before Day 3 Build

### Critical Gaps
| Gap | Impact | Resolution |
|:----|:-------|:-----------|
| 🔴 No Historical GPU Tracker data | Cannot plot time-series beyond 1 day | Use SemiAnalysis historical points as proxy; start collecting daily from today |
| 🔴 SemiAnalysis full data paywalled | Missing 2023-2026 time-series | Document historical points from Execution Plan; manually fill |
| 🟡 No NVDA historical data in CSV | Cannot do correlation analysis | Collect last 30d from Yahoo Finance during script run |

### Nice-to-Have
| Gap | Notes |
|:----|:------|
| BTC 30d history | CoinDesk API can fetch |
| USD/DXY history | Yahoo Finance |
| Natural Gas history | Yahoo Finance NG=F |
| Spot vs on-demand breakdown | GPU Tracker has this — add column |
| Provider-specific pricing | Only median available; could add per-provider cheapest |

## Implementation Options

### Option A: Python (Recommended for Day 3)
- `matplotlib` + `plotly` for interactive dashboard
- `pandas` for data manipulation
- Output: HTML dashboard (`dashboard_v1.html`) + static plots
- Pros: Full control, reproducible, can add alerting
- Cons: Manual refresh needed (no live API)

### Option B: Google Sheets
- Import CSV daily
- Sheets formulas for correlation
- Pros: Accessible, shareable
- Cons: Limited visualization

### Option C: Notion
- Good for layout but limited plotting

→ **Recommendation**: Python (Option A) with Plotly for interactive HTML dashboard

## Dashboard Build Steps (Day 3 Order)

1. [ ] Install dependencies (pandas, plotly, yfinance if needed)
2. [ ] Write data loader: read CSV, normalize
3. [ ] Plot 1: H100 pricing time-series (spot min, median, max)
4. [ ] Plot 2: H100 price vs NVDA overlay
5. [ ] Plot 3: H100 price vs BTC overlay
6. [ ] Plot 4: GPU generation pricing comparison (H100 vs H200 vs B200)
7. [ ] Plot 5: Market efficiency (H100 price spread over time)
8. [ ] Compute correlation matrix
9. [ ] Generate: `dashboard/dashboard_v1.html`
10. [ ] Update Research Log with findings

## Dashboard Color Scheme
- Background: Dark (#1a1a2e)
- H100: #e94560 (red accent)
- NVDA: #76b900 (NVIDIA green)
- BTC: #f7931a (Bitcoin orange)
- DXY: #00b4d8 (blue)
- Spot: solid line
- Contract: dashed line
- Min/Median/Max: shaded range area
