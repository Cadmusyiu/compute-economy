# The Compute Economy: GPU Pricing in the Age of AI Infrastructure

**作者：** Cadmus Yiu  
**日期：** 2026-06-19  
**數據截止：** 2026-06-19 21:30 HKT  
**Interactive Dashboard：** [cadmusyiu.github.io/compute-economy](https://cadmusyiu.github.io/compute-economy/)

---

## 摘要

GPU 算力正處於從「稀缺硬件」到「標準化商品」的過渡期。H100 現貨價格在兩個月內從 $2.82/hr 暴漲至 $8.97/hr（+218%），但市場同時存在 121 倍的價格離散度——這是全球最無效率的現貨市場之一。本文結合 GPU Tracker、SemiAnalysis 和 Yahoo Finance 的數據，分析 GPU 算力定價的結構、驅動因素，以及對 Compute Futures 的啟示。

**核心發現：**
- H100 市場處於 **Demand Spike 狀態**（> $5/hr alert threshold）
- NVDA 與 DXY 呈顯著負相關（r = -0.56），弱美元是 NVDA 的順風
- AI 與加密貨幣算力市場已完全脫鉤（r = -0.17）
- Blackwell 世代溢價 613% 反映代際升級的跳躍

---

## 1. GPU 定價的宏觀背景

### 1.1 AI Capex 週期的矛盾

NVIDIA（NVDA, $210.69）股價從 5 月中高位 $225.57 回落約 6.6%，反映市場對 AI capex 回報率的質疑正在升溫。與此同時，H100 算力價格卻在同期上演驚人的反彈——由 4 月低位 $2.82/hr 衝上 $8.97/hr，升幅超過兩倍。

這個 divergence 值得關注。**股價下跌、算力上漲**的組合，傾向於供應面限制（supply constraint）而不是需求面轉弱（demand weakening）。如果需求放緩，兩者應該同步下跌。

**圖 1：H100 現貨價格歷史趨勢（2023–2026）**

![H100 Historical Trend](https://raw.githubusercontent.com/Cadmusyiu/compute-economy/main/dashboard/plots/h100_historical_trend.png)

*數據來源：SemiAnalysis + GPU Tracker。2026 年 6 月數據點由 GPU Tracker median 估算。*

### 1.2 NVDA 與宏觀的關係：DXY 才是真正的風向標

500 日 Pearson 相關系數：**-0.56**（強負相關）

NVDA 與美元指數（DXY）的 -0.56 相關性是我們所有 macro data 中最強的信號。這不是 NVDA 特有的——它是 risk-on / risk-off 邏輯的體現——但 -0.56 的幅度說明了 NVDA 對宏觀流動性的高度敏感。

DXY 從 5 月中的 ~98.88 反彈到目前的 ~100.80，同期 NVDA 從 $225.57 跌到 $210.69。如果 DXY 繼續走強（Fed 鷹派立場 + 全球增長放緩），NVDA 短線會持續受壓。

**圖 2：NVDA vs DXY 500日價格疊加**

![NVDA vs DXY Overlay](https://raw.githubusercontent.com/Cadmusyiu/compute-economy/main/dashboard/plots/nvda_dxy_overlay.png)

關於可操作的宏觀信號：歷史模式（非預測）顯示，DXY > 102 是 NVDA 的警戒線；DXY < 99 則是潛在的買入窗口。

### 1.3 AI 與加密貨幣算力市場的脫鉤

NVDA vs BTC 的 500 日相關系數：**-0.17**（接近零）。

這個數字的意義：如果加密貨幣挖礦還在顯著影響 GPU 需求，NVDA 和 BTC 應該有顯著正相關。但數據顯示兩者已經沒有線性關係。

原因很直接：
- Bitcoin 挖礦已全面轉向 ASIC，GPU 不參與
- Ethereum 轉 PoS 後，GPU mining 的工業化需求基本消失
- AI 的 compute demand 是獨立的故事——不因 Bitcoin crash 而受影響，也不因 Bitcoin rally 而受推動

---

## 2. GPU 算力定價的結構分析

### 2.1 H100 現貨價格演變

| 時期 | 價格 ($/hr) | 背景 |
|:-----|:------------|:------|
| 2023 H1 | $2.70–$3.40 | ChatGPT 發布前後，AI boom 初始階段 |
| 2023 H2 | ~$6.62 | AI 泡沫頂峰，H100 供不應求 |
| 2024 | $3.00–$5.00 | 價格回調，供應逐步跟上 |
| 2025 | $2.50–$3.60 | 市場穩定，競爭加劇 |
| 2026 Mar | Sold Out | On-demand 中斷，產能轉移至 Blackwell |
| 2026 Apr | **$2.82**（週期低位） | SemiAnalysis spot 估算 |
| 2026 Jun | **$8.97**（當前） | GPU Tracker median |

從 $2.82 到 $8.97 的 +218% 反彈，潛在的驅動因素包括：

1. **DeepSeek / 開源模型的意外效果**（推測）—— 低成本的強大模型反而刺激了推論需求，因為更多開發者/公司可以 afford 部署
2. **H100 產能轉移**—— NVIDIA 將 wafer allocation 從 H100 轉移到 Blackwell，導致 H100 供應自然收縮
3. **季節性需求**—— 2025 年同期也有類似反彈（$3.60 → ~$5.00），但幅度只有今年的三分之一
4. **恐慌性搶購**—— 供應短缺預期引發搶租，價格自我實現

### 2.2 Generation Spread：算力的通貨膨脹

| GPU 世代 | 中位數 ($/hr) | 對比 H100 |
|:---------|:--------------|:----------|
| A100 | ~$8.30 | -7% |
| **H100** | **$8.97** | **基準** |
| H200 | $11.97 | +33% |
| B200 | $19.56 | +118% |
| B300 | $19.57 | +118% |
| GB200 | $64.00 | **+613%** |

**圖 3：GPU 世代定價對比**

![GPU Generation Comparison](https://raw.githubusercontent.com/Cadmusyiu/compute-economy/main/dashboard/plots/gpu_gen_comparison.png)

Generation premium 的結構透露了重要信息：

- **H200 只是 minor refresh**（+33%）——不值得為這個溢價選擇 H200 而非 H100
- **B200 是真正的代際躍進**（+118%）——Blackwell 的定價能力來自於 FP8 算力對 H100 的 5x 提升
- **GB200 是另一個物種**（+613%，$64/hr）——超大規模專用 cluster 定價，普通開發者不是目標客戶

這意味著當 B200 開始大規模量產時，H100 的定價可能加速下跌——上一代產品的自然折舊 + 下一代產品的供給替代。

### 2.3 市場碎片化：121x 的價格離散度

H100 現貨價格從 **$0.80/hr**（Verda, EU-Central, Spot）到 **$97.44/hr**（GCP, 多 GPU instance），差距 **121 倍**。

**圖 4：H100 價格離散度**

![H100 Price Spread](https://raw.githubusercontent.com/Cadmusyiu/compute-economy/main/dashboard/plots/h100_spread.png)

這個極端的離散度反映了三個層次的市場結構：

**Layer 1 — Marketplace（$0.80–$2.50/hr）**
- Vast.ai、Verda、RunPod 等 peer-to-peer marketplace
- 閒置產能變現，spot instance
- 典型的供應方：散戶、中小型數據中心、閒置雲端實例
- 邊際成本幾乎為零（已經是 sunk cost）

**Layer 2 — Mid-tier Cloud（$5–$15/hr）**
- 各大雲端供應商的標準 on-demand 配置
- 包括 basic networking、有限的 SLA
- 這是大多數 AI 開發者使用的價格區間

**Layer 3 — Hyperscaler Multi-GPU（$50–$97/hr）**
- GCP、AWS、Azure 的 8x 或以上 H100 cluster config
- 包括高速 InfiniBand networking、專業 support、SLA
- 企業級用戶定價，包含大量的非算力溢價

這個三層結構的意義：

**這是一個極度低效率的市場。** 同樣是 H100 算力，121 倍的價格差距在傳統金融市場是不可想像的。GPU Tracker 這樣的 aggregator 存在的意義正是 arbitrage——用戶可以用 1% 的價格租到同等算力。

但這個低效率也暗示了市場的成熟方向：隨著透明度提升（更多 aggregator、更多定價指數），價格應該逐漸收斂。Compute Futures 的推出會加速這個過程。

---

## 3. 對 Compute Futures 的啟示

### 3.1 市場基礎設施的現狀

CME Compute Futures 的討論在 2024–2025 年間已有 murmur——類似 CME Bitcoin Futures（2017）的邏輯，將非傳統資產標準化。

當前障礙：

1. **121x spread 的存在**—— 沒有一個可信的「公允價格」。$8.97 的 median 是一個起點，但市場效率不足以為期貨合約提供可靠的結算價
2. **數據源的碎片化**—— GPU Tracker 很好，但它的覆蓋度以 marketplace 為主，hyperscaler pricing 的透明度很低
3. **Contract spec 的標準化**—— 什麼 GPU？多少個？哪個 provider？reference index 如何構建？

樂觀的一面是，**GPU Tracker、SemiAnalysis GPU Pricing Index、SiliconData Index** 這三個獨立數據源的出現，正在為標準化打下基礎。當期的價格離散度其實是市場缺乏統一基準的症狀，而不是絕對算力價值的分歧。

### 3.2 算力定價作為先行指標

目前 NVDA 股價尚未充分反映 GPU 算力市場的 demand surge。H100 中位數 $8.97/hr 是 14 個月前的 3 倍，但 NVDA 股價比 2025 年 6 月只高了約 15%。

**這意味著 H100 spot price 可能是 NVDA 的先行指標。** 如果 NVDA 最終會 catch up 算力市場的信號，那麼：

- H100 維持在 $8–$12/hr → NVDA 有上行空間
- H100 回落至 $4–$6/hr → NVDA 的 AI narrative 可能被重新定價

---

## 4. 風險情景

### 4.1 供應突然釋放（中高概率）

如果 B200 / H200 ramp-up 符合預期，H100 供應在 Q3 可能大量釋放。H100 median 可能回落至 $4–$6/hr。NVDA 短線受壓（margin compression fear）。

**Dashboard 監察信號：** H100 listings 急升 > 5,500 + 價格向下突破移動平均線

### 4.2 需求放緩（中等概率）

AI startup funding 冷卻，或 hyperscaler 宣布 capex 削減。最受影響的是 Layer 2 pricing（$5–$15/hr），這是 marginal demand 的定價區間。Marketplace pricing（$0.80–$2.50）因已是邊際成本，下跌空間有限。

**監察信號：** H100 volume 急升 + NVDA+H100 同步下跌

### 4.3 宏觀衰退（中低概率）

全球經濟衰退 → Enterprise IT budget 凍結 → AI experiment 被 defer。這是最差的 scenario——影響是 systemic 的。GPU 算力市場可能比 NVDA stock 更有韌性：spot contract 是 variable cost，衰退時企業會減少長期承諾但可能繼續 run experiments on spot。

**監察信號：** DXY > 103 + NVDA < $180 + H100 listings 急升

### 4.4 算力價格繼續暴漲（中低概率）

Blackwell ramp-up 延遲 + Inferencing demand 爆炸式增長。H100 median 可能升到 $12–$15/hr。NVDA 應會跟升，但滯後 2–4 星期。

**監察信號：** H100 > $12 + listings 持續下跌（供應萎縮）

---

## 5. 結論與路徑

GPU 算力市場正處於一個特殊的節點。一方面，H100 現貨價格的暴漲（+218%）和市場 121x 的離散度都指向供應緊張和市場不成熟。另一方面，contract premium 為負（$2.10–$2.70 contract vs $8.97 spot）暗示市場預期這個短缺是暫時的。

**關鍵問題：$8.97/hr 是結構性失衡的新常態，還是週期性波動的頂部？**

現有數據不足以給出明確答案。2 天的 daily time-series 只能告訴我們當前的 snapshot。真正的價值來自於持續的數據積累——30 天後可以開始計算 rolling average 和 volatility；90 天後可以分析 seasonality；180 天後可以建立有意義的預測模型。

**這個 dashboard\* 是一個開始，不是終點。**

\*[cadmusyiu.github.io/compute-economy](https://cadmusyiu.github.io/compute-economy/) — 自動化 dashboard，每日三次更新 H100 pricing、generation spread 和 macro correlation。

---

**免責聲明：** 本文為個人研究，不構成投資建議。所有 speculative 觀點已明確標註。數據來源包括 GPU Tracker、SemiAnalysis public preview、Yahoo Finance。

**Reference Index：**
- GPU Tracker: [gputracker.dev](https://gputracker.dev)
- SemiAnalysis GPU Pricing Analysis: [semianalysis.com](https://www.semianalysis.com/p/gpu-pricing-analysis-and-the-ai-ecosystem)
- NVIDIA (NVDA): Yahoo Finance
- Correlation Matrix: 500-day Pearson, computed via custom Python script

---

*Research Article #001 — 2026-06-19*
*GitHub Repo: [Cadmusyiu/compute-economy](https://github.com/Cadmusyiu/compute-economy)*
