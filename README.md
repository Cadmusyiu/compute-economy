# Compute Economy — Auto Assessment Repo

> 🎮 **Play live**: https://cadmusyiu.github.io/compute-economy/


> 自動分析 GPU compute pricing data，判斷 computing market 嘅健康度、趨勢同 macro 影響。
> Built for Cadmus's personal research.

## 目標

1. **自動收集** GPU pricing data（每日一次）
2. **定期評估** compute market 狀態（供應/需求/價格趨勢）
3. **產生可讀報告** — 幫 Cadmus 快速判斷市場方向
4. **新指標 alert** — 當有新 pricing anomaly 或 regime shift 時通知

## 目錄結構

```
compute-economy/
├── raw_data/              # 原始數據 (JSON/CSV/MD)
│   ├── gputracker_*.json       — GPU Tracker listings
│   ├── semianalysis_*.md       — SemiAnalysis data notes
│   └── silicondata_*.json      — Silicon Data (if trial)
├── dashboard/             # 可視化檔案
│   ├── dashboard_v1.html       — Dashboard 第一版
│   └── plots/                  — Python 生成嘅圖表
├── scripts/               # 自動化 scripts
│   ├── collect_daily.py        — 每日 data collection
│   ├── assess_market.py        — 市場評估 engine
│   └── alert_check.py          — Alert 檢查
├── notebooks/             # Jupyter notebooks
│   └── correlation_analysis.ipynb
├── RESEARCH_LOG.md        # 每日 research log
├── ASSESSMENT.md          # 最新 assessment report（自動更新）
└── README.md              # 呢個檔
```

## Data Sources

| Source | Type | Cost | Frequency |
|:-------|:-----|:-----|:----------|
| GPU Tracker (gputracker.dev) | Spot market listings | Free | Daily |
| SemiAnalysis (public preview) | Historical + spot pricing | Free | Weekly |
| Silicon Data (trial) | Index + forward curve | $499/mo (7d trial) | Real-time |
| Yahoo Finance (NVDA, BTC, etc.) | Macro correlation | Free | Daily |

## Market Health Indicators

| Indicator | Description | Signal |
|:----------|:------------|:-------|
| H100 Spot Price | 即期租用價格 | ↑=demand>supply |
| 1yr Contract Premium | 長期 vs 即期溢價 | ↑=market expects shortage |
| Listing Count | GPU Tracker 上架量 | ↓=supply tight |
| NVDA/H100 Ratio | NVDA 股價 vs compute 租價 | ↑=mispricing |
| On-Demand Availability | 有冇得即租 | Sold Out = extreme tight |

## Alert Thresholds (初版)

- 🔴 H100 spot > $5/hr → demand spike
- 🟡 H100 spot < $1.50/hr → supply glut
- 🔴 NVDA/H100 ratio > 3σ from 30d ma → anomaly
- 🟡 Listing count drop > 20% in 7d → supply tightening

## 用法

```bash
# 每日收集
python3 scripts/collect_daily.py

# 跑 assessment
python3 scripts/assess_market.py

# 檢查 alert
python3 scripts/alert_check.py
```
