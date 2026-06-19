# Compute Economy Research Log
> Project: GPU Compute Market Structure & Macro Implications
> Period: Jun 18–24, 2026 (Holiday Research Project)

---

## 2026-06-19 (Sat) — Day 2: Data Collection & Market Observations

### Sources Accessed
1. **GPU Tracker** (gputracker.dev) ✓ — Full public data snapshot obtained
2. **SemiAnalysis GPU Pricing Index** — Behind paywall; summary data from public preview
3. **SemiAnalysis GPU Pricing Analysis article** — 404/page not found (correct URL uncertain)

### Key Findings

#### GPU Tracker Snapshot (2026-04-19)
| Metric | Value |
|:-------|:------|
| Total listings tracked | 5,213+ |
| Total providers | 54+ |
| Largest provider by inventory | GCP (2,074 listings, 16 models) |
| Cheapest overall GPU | RTX5070 @ $0.007/hr (Vast.ai, Spot) |
| Cheapest H100 | $0.80/hr (Verda, EU-Central, Spot) |
| **H100 median** | **$8.97/hr** |
| H100 top | $97.44/hr (hyperscaler multi-GPU) |
| H100 price spread | 121x |
| A100 median | $8.30/hr |
| B200 median | $19.56/hr |
| H200 median | $11.97/hr |
| GB200 | $42–64/hr |
| Spot vs on-demand | Spot cheapest $0.007/hr vs on-demand cheapest $0.034/hr |

#### H100 Historical Pricing (from SemiAnalysis preview)
| Period | Price/hr | Note |
|:-------|:---------|:-----|
| 2023 H1 | $2.70–3.40 | Pre-boom |
| 2023 H2 | ~$6.62 | AI bubble peak |
| 2024 | $3.00–5.00 | Post-peak decline |
| 2025 | $2.50–3.60 | Stabilization |
| 2026 Q1 | Tightening | Supply constraints emerging |
| 2026 Mar | Sold Out | On-demand unavailable |
| 2026 Apr Spot | $2.82 | SemiAnalysis estimate |
| 2026 Apr 1yr | $2.10–2.70 | Contract below spot |

### Interesting Patterns Observed
1. **Massive price spread**: H100 ranges 121x — $0.80 marketplace spot vs $97.44 hyperscaler — suggests a fragmented, inefficient market
2. **Generation premium**: B200 median ($19.56) is 2.2x H100 median ($8.97), but only 1.6x H200 ($11.97)
3. **Supply pinch forming**: SemiAnalysis notes on-demand H100 sold out in Mar 2026 despite prices down ~57% from peak — unusual pattern
4. **Marketplace disruption**: Verda offering H100 at $0.80/hr spot — 11x below median — may indicate overcapacity at the edge vs hyperscaler tightness

### Questions for Day 3
1. What's driving the massive H100 price spread? Is it real or artifact of multi-GPU vs single-GPU listings?
2. If on-demand is Sold Out but marketplace has $0.80 spot, is the shortage real or cloud-provider specific?
3. How does B200/H200 pricing correlate with H100 pricing trajectory?
4. What's the NVDA stock price correlation with GPU compute pricing?
5. Is there a "GPU yield curve" (spot vs contract) that predicts supply/demand shifts?

### Data Collected
- [x] GPU Tracker snapshot: `raw_data/gputracker_2026-06-19.json`
- [x] SemiAnalysis notes: `raw_data/semianalysis_2026-06-19.md`
- [x] Daily price snapshot updated in `gpu_price_timeseries.csv`
- [ ] Silicon Data trial (not yet activated)

### Next Steps (Day 3 — Jun 20)
- Build dashboard with Python
- Plot H100 pricing history vs NVDA/BTC
- Analyze correlations
- See: `raw_data/dashboard_plan.md`

---

## 2026-06-18 (Fri) — Day 1: Setup

### Done
- Project repository structure created
- Data collection script (`collect_gpu_data.py`) installed and run
- Bookmarks set up for GPU Tracker, SemiAnalysis, Silicon Data
- Execution plan locked in
- Initial CSV data point captured
- NVDA initial price: $209.63

### Notes
- gputracker.dev domain had DNS resolution issues initially (NXDOMAIN from this network), but `gputracker.dev/gpu-cloud-statistics-2026` accessible via direct HTTP fetch with proper User-Agent
- SemiAnalysis article URL may need correction — the slug `gpu-pricing-analysis-and-the-ai-ecosystem` returns 404; GPU Pricing Index is paywalled
