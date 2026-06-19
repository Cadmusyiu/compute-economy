# SemiAnalysis GPU Pricing Analysis — Research Notes
> Fetched: 2026-06-19 | Source: Semianalysis (semianalysis.com)
> Status: Full article behind paywall. Data points compiled from public preview + execution plan.

## Data Source
The SemiAnalysis GPU Pricing Index (semianalysis.com/gpu-pricing-index/) is a subscriber-only dashboard.
The GPU Pricing Analysis article at `p/gpu-pricing-analysis-and-the-ai-ecosystem` also requires subscription.

Data points below were pre-documented in the project execution plan (Jun 18 setup) as key numbers.

---

## H100 Pricing History (SemiAnalysis Data Points)

### 2023
- **H1 2023**: $2.70–$3.40/hr
- **H2 2023**: $6.62/hr spot (AI bubble peak period)

### 2024
- Range: $3–$5/hr (declining from peak)
- Market normalization post-AI hype bubble

### 2025
- Range: $2.50–$3.60/hr (stabilization)
- Market matured, more supply entered

### 2026
- **Q1 2026**: Market started to tighten
- **Mar 2026**: H100 on-demand capacity: **Sold Out**
- **Apr 2026 Spot**: **$2.82/hr** (SemiAnalysis data point)
- **Apr 2026 1yr Contract**: **$2.10–$2.70/hr** (SemiAnalysis data point)

### Key Observations (Trend)
1. **Long-term decline**: From ~$6.62/hr peak (2023) to ~$2.82/hr (Apr 2026) — ~57% decline
2. **Supply tightening in 2026**: On-demand sold out signals capacity constraints despite price decline
3. **Spot vs contract spread**: 1yr contracts ($2.10-2.70) below spot ($2.82) — normal contango
4. **Volatility**: Large swings (2x+ between H1/H2 2023) suggest supply-demand imbalances

---

## Current GPU Market Snapshot (GPU Tracker, Apr 2026)

### H100
| Metric | Value |
|:-------|:------|
| Listings tracked | 327 |
| Spot range | $0.80–$97.44/hr |
| Median | $8.97/hr |
| Cheapest spot | $0.80/hr (Verda, EU-Central) |
| Cheapest on-demand | $1.55/hr |
| Provider spread | 121x |

### H200 (Next-gen)
| Metric | Value |
|:-------|:------|
| Listings tracked | 133 |
| Range | $1.19–$169.60/hr |
| Median | $11.97/hr |

### B200 (Blackwell)
| Metric | Value |
|:-------|:------|
| Listings tracked | 86 |
| Range | $1.71–$90.22/hr |
| Median | $19.56/hr |

### B300 (Ultra)
| Metric | Value |
|:-------|:------|
| Listings tracked | 14 |
| Range | $2.45–$70.78/hr |
| Median | $19.57/hr |

### GB200 (Grace Blackwell)
| Metric | Value |
|:-------|:------|
| Listings tracked | 21 |
| Range | $42.00–$64.00/hr |
| Median | $64.00/hr |

---

## Market Structure Observations

### Price Spread
- **H100 spread**: 121x ($0.80 marketplace spot → $97.44 hyperscaler multi-GPU)
- **L40S spread**: Extreme $445.25/hr top (likely multi-GPU config)
- **Hyperscaler premium**: 99% more than cheapest marketplace (GCP vs Verda)

### Provider Distribution
- **GCP dominates inventory**: 2,074 listings across 16 GPU models
- **Long tail**: 54+ providers tracked, with Vast.ai/Verda driving the low end
- **Marketplace efficiency**: Verda ($0.80/hr H100 spot) 10x cheaper than median

### Generation Pricing Evolution
- H100 median ($8.97/hr) → H200 median ($11.97/hr) → B200 median ($19.56/hr)
- Each generation ~33-63% premium over previous at median
- Top-end prices scale more aggressively (GB200: $42–64/hr)

---

## Notes & Data Gaps

- **SemiAnalysis full article**: Paywalled; full time-series not accessible
- **Historical trend**: GPU Tracker only has live snapshot; no time-series available via free tier
- **Silicon Data Trial**: Could supplement with historical GPU pricing index if trial activated
- **Contract pricing**: Not available from GPU Tracker; SemiAnalysis has 1yr contract data
- **On-demand availability**: GPU Tracker doesn't expose "Sold Out" status directly
