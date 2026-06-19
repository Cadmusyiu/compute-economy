# Research Note #001 — Compute Economy 現狀與前瞻

> **日期:** 2026-06-19
> **作者:** Cadmus Yiu / CadAI
> **數據截止:** 2026-06-19 21:30 HKT
> **Dashboard:** https://cadmusyiu.github.io/compute-economy/

---

## 1. 🏔️ Macro Context（宏觀背景）

### AI Capex Cycle 現狀

AI 基礎設施投資處於一個**矛盾的十字路口**。一方面，NVIDIA（NVDA, $210.69）股價從 5 月中高位 $225.57 回落約 6.6%，反映市場對 AI capex 回報率嘅質疑正在升溫。另一方面，H100 算力價格卻喺同期上演驚人嘅反彈——由 4 月低位 $2.82/hr 衝上 $8.97/hr，升幅超過兩倍。

呢個 divergence 值得留意：**股價跌、算力貴** — 似係 supply 面 constraint 多過 demand 面 weakening。

### NVDA vs DXY — 美元弱勢 = NVDA 順風

500 日 Pearson 相關系數：**-0.56**（strong inverse）

呢個係成個數據集中最強嘅 macro signal。NVDA 走勢同美元指數（DXY, ~100.80）呈顯著負相關，意味住：
- 美元弱 → 風險資產 (risk-on) 資金流入 NVDA
- 美元強 → NVDA 受壓

DXY 喺 5 月中由 ~98.88 反彈到而家 ~100.80，同期 NVDA 由 $225.57 跌到 $210.69 — 吻合。如果 DXY 繼續走強（Fed 鷹派立場 + 全球增長放緩），NVDA 短線會持續受壓。

**投資啟示：** DXY > 102 係 NVDA 嘅警戒線；DXY < 99 係 NVDA 嘅買入信號（基於歷史模式，非預測）。

### GPU 供應鏈狀況

- **H100 on-demand：** 2026 年 3 月已 Sold Out（SemiAnalysis 數據）
- **Spot market：** H100 中位數 $8.97/hr，比 4 月 $2.82/hr 升 218%
- **Next-gen 供應：** B200（Blackwell）中位數 $19.56/hr，H200 $11.97/hr，GB200 $42–64/hr
- **Blackwell 量產（speculative）：** B200/B300 供應預期喺 2026 H2 開始 ramp-up，不過過去經驗話我哋知 Nvidia 嘅新產品 ramp-up 通常慢過市場預期

供應鏈嘅關鍵問題唔係「有冇 GPU」，而係「邊個 generation 嘅 GPU」。H100 供應緊張反而可能係因為產能轉移到 Blackwell，而非需求突然暴增。

---

## 2. 💰 GPU Pricing Analysis

### H100 Spot 價格軌跡（2023–2026）

| 時期 | 價格 ($/hr) | 註解 |
|:-----|:------------|:-----|
| 2023 H1 | $2.70–$3.40 | AI boom 前 |
| 2023 H2 | ~$6.62（歷史高位） | AI 泡沫高峰 |
| 2024 | $3.00–$5.00 | 價格回調 |
| 2025 | $2.50–$3.60 | 市場穩定 |
| 2026 Mar | Sold Out | On-demand 歸零 |
| 2026 Apr | **$2.82**（市場低位） | SemiAnalysis spot 估算 |
| 2026 Jun | **$8.97**（而家） | GPU Tracker median |

**關鍵問題：** 由 $2.82 到 $8.97，兩個月內 +218%。呢個走勢嘅 trigger 係咩？

幾個可能性：
1. **DeepSeek / open-source 模型效應**（speculative）— 低成本高效模型反而刺激咗 inferencing demand，因為更多開發者／公司可以 afford to deploy
2. **H100 產能轉移** — Nvidia 將 wafer allocation 由 H100 移到 Blackwell，導致 H100 supply 自然收縮
3. **季節性 demand** — 2025 年同期由 $3.60 升到 ~$5.00，但幅度冇咁誇張
4. **恐慌性搶購** — 唔夠 H100 → 大家爭住租 → 價格 spiraling

SemiAnalysis 嘅 1yr contract price（$2.10–$2.70）遠低於 spot，反映市場預期呢個短缺係暫時性——如果大家都睇好長期供應緊張，contract premium 應該係正數。反而 contract 低過 spot，暗示市場 expect supply 會恢復。

### Generation Spread 分析

| GPU Gen | 中位數 ($/hr) | vs H100 |
|:--------|:--------------|:--------|
| A100 | ~$8.30 | -7% |
| H100 | **$8.97** | Baseline |
| H200 | $11.97 | +33% |
| B200 | $19.56 | +118% |
| B300 | $19.57 | +118% |
| GB200 | $64.00 | **+613%** |

**Key observation：** 由 H100 到 GB200 嘅 generation premium 達到 613%，但 H100 到 H200 只係 +33%。呢個 spread 暗示：

- **H200 係 minor refresh** — 唔值得高溢價
- **B200 係 major leap** — +118% premium 反映真．代際升級
- **GB200 係另一個物種** — $64/hr 係超大規模 cluster 先會用，唔係普通 developer 嘅選項

### Market Fragmentation — 121x Spread

H100 價格由 **$0.80/hr**（Verda, EU-Central, Spot）到 **$97.44/hr**（GCP, 多 GPU instance），差距 **121 倍**。

呢個 fragmentation 反映咗幾件事：

1. **市場效率極低 —** 同一件 commodity（H100），121x 價格差距喺傳統市場係不可想像嘅。GPU Tracker 存在嘅意義就係 arbitrage：User 可以用 1% 嘅價錢租到同等算力。
2. **Provider 分層明顯：**
   - **Layer 1 — Marketplace（Vast.ai / Verda / RunPod）：** $0.80–$2.50/hr — 閒置產能，spot instance，可能係散戶／中小型數據中心放租
   - **Layer 2 — Mid-tier（各大 cloud 細 config）：** $5–$15/hr — 標準 on-demand pricing
   - **Layer 3 — Hyperscaler（GCP / AWS / Azure multi-GPU）：** $50–$97/hr — 包括 networking、support、SLA premium
3. **價格分散 = 機會：** 如果中型公司可以用 $0.80/hr 租到同等 H100 train 一個 model，hyperscaler 嘅 $97/hr 定價就難以持續。呢個差距係 potential compression 嘅方向。

### Compare with SemiAnalysis Historical Data

將 SemiAnalysis 嘅歷史時間序列交叉驗證 GPU Tracker 嘅 snapshot：

- **過去 trend 嘅 pattern：** H100 價格似乎係 3–4 個月週期嘅波動，每次 boom 後有 6–9 個月嘅冷卻期。2023 H2 高位 → 2024 調整；2026 Apr 低位 → Jun 反彈。如果呢個 pattern 重複，而家嘅高位應該喺 Q3 見頂然後回落。
- **但呢次唔同嘅地方**（speculative）：
  - Blackwell 量產抽走 H100 產能 — 呢個供應結構性改變係以前冇嘅
  - Inferencing demand 持續增長 vs training demand 嘅週期性
  - H100 已經係上一代產品，supply 只會自然萎縮

---

## 3. 🔗 Correlation Insights

### Correlation Matrix（500-Day Pearson r）

| Pair | r | 解讀 |
|:-----|:--|:-----|
| **NVDA vs DXY** | **-0.56** | Strong inverse — NVDA 係 risk-on 指標 |
| NVDA vs NG | -0.22 | Weak inverse |
| **NVDA vs BTC** | **-0.17** | Near zero — AI 同 crypto 已 decouple |
| DXY vs NG | +0.24 | Weak positive |
| BTC vs DXY | -0.14 | Very weak |
| BTC vs NG | +0.04 | Effectively zero |

### 對算力定價嘅含義

**1. NVDA–DXY (-0.56)：最可操作嘅 macro signal**

算力定價同 NVDA 股價有正向關係（至少邏輯上）。如果 NVDA 因為美元弱勢而受惠，呢個「順風」理論上應該亦利好 GPU 租賃市場——更多 AI startup 會得到 venture funding，推動 compute demand。

但現實係，算力定價嘅短期波動似乎更多由 supply dynamic 主導（產能、generation transition），而 macro 因素係 indirect 嘅。

**2. NVDA–BTC (-0.17)：Decoupling confirmed**

如果 Crypto 同 AI compute 仲有 direct link（好似 2021–2022 年 mining 狂潮），NVDA 同 BTC 應該有顯著正相關。但 500 日數據顯示 correlation 接近零。

含義：
- Crypto mining 對 GPU demand 嘅影響已經好微（ASIC 主導 Bitcoin，ETH 轉 POS）
- AI compute 嘅 price action 係獨立嘅 macro story，唔會因為 Bitcoin crash 而受拖累
- 反之亦然 — Bitcoin rally 唔會直接推高 GPU 租價

**3. 值得 monitoring 嘅 correlation 變化：**

如果 H100 spot 繼續升穿 $10/hr，我預計 NVDA 會 catch up（目前 NVDA 未反映呢個 demand surge）。到時 NVDA–H100 嘅 correlation 可能會 strengthening，算力定價可以作為 NVDA 嘅 leading indicator。

---

## 4. 🔮 Compute Futures Outlook

### CME Compute Futures 潛在推出時間線

關於 CME（芝加哥商品交易所）推出 Compute Futures 嘅討論，2024–2025 年間已有 murmur——類似 CME Bitcoin Futures（2017 年推出）嗰種將「non-traditional asset」標準化嘅邏輯。

**現狀：**
- 未有正式 announcement
- 市場 infrastructure 未成熟：GPU pricing 嘅 fragmentation（121x spread）係一個大障礙
- 但 GPU Tracker 呢類 aggregator 嘅出現 + SemiAnalysis GPU Pricing Index 嘅嘗試，都係邁向標準化嘅 step

### 呢個 Dashboard 點樣 Serve 作為 Underlying

我哋嘅 dashboard 暫時係一個 **proof of concept** 嘅 compute pricing index：

- **H100 median spot price：** 近似一個 simple average price benchmark
- **Generation spread：** 可以 cross-reference 嚟衡量「compute inflation」
- **121x spread 本身：** 係市場 inefficiency 嘅即時指標——如果 spread 開始縮窄，可能係市場準備好 futrues listing 嘅先兆

一個 realistic 嘅 Compute Futures contract 需要：
1. 一個可信嘅 **reference index**（類似 CME Bitcoin Reference Rate, BRR）
2. 足夠嘅 liquidity 同 volume
3. 標準化 contract specs（咩 GPU？幾多個？邊啲 provider？）

**Speculative ETA：** 如果個 market 繼續 grow，2027–2028 年有可能見到試行 contract。前提係 pricing 透明度改善——GPU Tracker 呢類 tool 嘅普及係必要條件。

### 自己累積到 Meaningful Time-Series 嘅 ETA

目前我哋有：
- 2 日嘅 daily GPU Tracker data（Jun 18, 19）
- 多個 snapshot 點（由於 script 喺同一日 collect 咗幾次）
- SemiAnalysis 5 個 historical data points（2023–2026）

**30 日後（Jul 19）：** 可以開始做簡單嘅趨勢分析（moving average、volatility estimate）
**90 日後（Sep 19）：** 足夠做 seasonality 分析，同 macro 做 rolling correlation
**180 日後（Dec 19）：** 真正有意義嘅 time-series，可以開始 build predictive model

**Target：** 1 年嘅 daily data = 足夠做 annual comparison + 建立 compute pricing seasonality profile

---

## 5. ⚠️ Risk Scenarios

### Scenario A: Supply突然Release（概率：中高）

**觸發事件：** H200 / B200 量產 ramp-up 符合預期，供應在 Q3 2026 大量釋放。

**影響：**
- H100 median 可能由 $8.97 跌番去 $4–$6/hr
- H200 median 可能同 H100 converge（如果市場將 H100 定性為「legacy」）
- NVDA 股價可能 short-term 受壓（margin compression fear）

**Dashboard signal：** H100 listings count 急升（>500）+ 價格向下突破移動平均線

### Scenario B: Demand放緩（概率：中）

**觸發事件：** AI startup funding cycle 冷卻，或 major hyperscaler 宣佈 capex 削減。

**影響：**
- 最受影響係 Layer 2 pricing（$5–$15/hr segment）— 呢個係 marginal demand 嘅定價區間
- Marketplace pricing（$0.80–$2.50）因為已經係 marginal cost，下跌空間有限
- NVDA 股價可能下跌 15–25%（假設 AI revenue 預期被下調）

**Dashboard signal：** H100 volume（listings count）急升 + NVDA+H100 同步下跌

### Scenario C: Macro Risk — Recession削減Capex（概率：中低）

**觸發事件：** 全球經濟衰退 -> Enterprise IT budget 凍結 -> AI experiment 被 defer。

**影響：**
- 呢個係最差 scenario，因為影響係 systemic 嘅—唔只係 GPU market
- DXY 應該會升（risk-off flow to USD），同時間 NVDA 同 H100 price 都跌
- 但 GPU 算力 market 可能比 NVDA stock 更有韌性：spot contract 係 variable cost，公司喺 recession 會減少 long-term commitment 但可能 still run experiments on spot

**Dashboard signal：** DXY > 103 + NVDA < $180 + H100 listings count 急升

### Scenario D: H100 Price 繼續暴漲（概率：中低）

**觸發事件：** Blackwell ramp-up 延遲 + Inferencing demand 爆炸式增長。

**影響：**
- H100 median 可能升到 $12–$15/hr（類似 2023 年高位嘅 double peak）
- Marketplace 同 Hyperscaler 嘅 spread 進一步拉闊
- NVDA 股價應該會跟升，但可能滯後 2–4 星期

**Dashboard signal：** H100 > $12 + listings count 持續下跌（供應萎縮）

---

## 6. 🎯 Next Steps

### 短期（呢個星期）

- ✅ 每日 collect GPU Tracker data（已自動化，透過 launchd 排程）
- ✅ GPU Gen Comparison 圖表生成完成
- ✅ NVDA–DXY / NVDA–BTC correlation 分析完成
- [ ] 修正 collect script — 避免同日多次 snapshot 污染 time-series（今日有 4 個 entry）
- [ ] 為 `gpu_price_timeseries.csv` 增加 schema validation 或 append-only guard

### 中期（未來 1 個月）

- [ ] 收集至少 30 日連續 daily pricing data
- [ ] 開始對比 GPU Tracker data 同 SemiAnalysis 嘅差異（如果 trial 開通）
- [ ] 建立「Spot vs Contract」spread indicator（如果 SemiAnalysis contract data 持續可用）
- [ ] 跟進 NVDA–H100 price correlation — 睇下有冇 leading/lagging relationship
- [ ] 研究 90-day rolling correlation 嘅 NVDA–BTC 走勢（短期可能同 500-day 唔同）

### 長期

- [ ] 每月更新 Research Note 一次（每月 19 號左右）
- [ ] **如果 Silicon Data trial 開通：** 比較 index pricing vs GPU Tracker marketplace pricing
- [ ] 累積 180 日 time-series 後建立初步嘅 predictive model
- [ ] 監察 CME Compute Futures 相關新聞

---

## Appendix: Key Data Points Reference

| 指標 | 數值 | Source |
|:-----|:-----|:-------|
| H100 Spot Median | $8.97/hr | GPU Tracker (Jun 19) |
| H100 Spot Min | $0.80/hr | GPU Tracker — Verda |
| H100 Spot Max | $97.44/hr | GPU Tracker — GCP |
| H100 121x Spread | $0.80–$97.44 | GPU Tracker |
| H100 Apr 2026 Spot | $2.82/hr | SemiAnalysis |
| H100 1yr Contract | $2.10–$2.70/hr | SemiAnalysis |
| H200 Median | $11.97/hr | GPU Tracker |
| B200 Median | $19.56/hr | GPU Tracker |
| GB200 Median | $64.00/hr | GPU Tracker |
| Total Listings | 5,213 | GPU Tracker (all GPU types) |
| H100 Listings | ~327 | GPU Tracker |
| NVDA | $210.69 | Yahoo Finance (Jun 19 close) |
| BTC | ~$62,478 | CoinDesk (Jun 19) |
| DXY | ~100.80 | Yahoo Finance |
| NVDA–DXY r | -0.56 | 500-day Pearson |
| NVDA–BTC r | -0.17 | 500-day Pearson |
| Regime | BULL / Demand Spike | H100 > $5/hr threshold |

---

*Research Note #001 — 2026-06-19*
*Next update: ~2026-07-19*
