# Compute Economy Research — 6 日執行計劃

> **Timeframe: 6/18 (Fri) 晚 — 6/24 (Tue) 生日**
> 目標：完成第一階段（Understand Market Structure + Build Data Pipeline）
> 每日 ~2-4 hrs（視乎你同怡萱嘅活動安排）

---

## 🗓️ Day-by-Day 執行

### Day 1: 6/18 (Fri) 今晚 — Setup

- [ ] **1. 開 Silicon Data Portal 帳號** → portal.silicondata.com
      - Base Package $499/mo — 有 7-day free trial
      - 趁假期用 trial, 7 日內 cancel 就唔使俾錢
      - Trial 內容：SiliconIndex Dashboard, H100/A100/B200 indices, 90 日歷史數據
- [ ] **2. Bookmark 啲 data sources**
      - gputracker.dev — free listings data
      - SemiAnalysis GPU Pricing Preview — free H100 spot chart
      - silicondata.com — GPU index chart
- [ ] **3. 安裝 GPU price tracker script**（我幫你準備好）
- [ ] **4. 定立 research log 格式**

**Output：** ✅ Data sources access + 自動 data collection

---

### Day 2: 6/19 (Sat) — 和媽媽妹妹食飯日（比較忙）

**輕量任務（~1 hr）：**

- [ ] 睇 GPU Tracker 嘅 public stats（已經 fetch 咗 27 條 key stats）
- [ ] 睇 SemiAnalysis 嘅 H100 pricing history（2023-2026 數據已有）
- [ ] 記低關鍵數字：
      - H100 spot Apr 2026: $2.82/hr
      - H100 1yr contract: $2.10-2.70/hr
      - H100 on-demand Mar 2026: Sold Out
      - 最低 spot: $0.80/hr (marketplace)
      - 最高: $97.44/hr (hyperscaler multi-GPU)
- [ ] 開一個 Google Sheet / Notion page 做 central research log

**Output：** 📊 核心 market observations recorded

---

### Day 3: 6/20 (Sun) — 全天可用 🎯 Key Day

**主要 research session（~3-4 hrs）：**

- [ ] **Build 第一版 Compute Price Dashboard**
      - 用 Python / Notion / Google Sheets 做一個 tracking dashboard
      - Columns: Date, H100 Spot, H100 1m/6m/1y, B200, NVDA, BTC, Nat Gas, USD index
- [ ] **Analyze H100 pricing history from SemiAnalysis**（已有 2023-2026 data）
      - 2023 H1: $2.70-3.40/hr
      - 2023 H2: $6.62 spot（AI bubble peak！）
      - 2024: 跌到 $3-5
      - 2025: 穩定在 $2.50-3.60
      - 2026 Q1: 開始 tight（Sold Out）
      - → Trend: 長期下跌，但 volatility 大，2026 年 supply 開始 tight
- [ ] **NVDA vs H100 rental correlation plot**（用 Python 手動做）
- [ ] **Log 所有觀測點去 research log**

**Output：** 🖥️ Dashboard v1 + 第一個 quantitative insight

---

### Day 4: 6/21 (Mon) — 廣州出發日

**輕量任務（~1 hr）：**

- [ ] **Si 深入 Silicon Data trial**（趁仲有 trial access）
      - 玩下佢哋啲 dashboard：Index、Forward Curve、Token Market Pulse
      - 比較 SemiAnalysis data 同 Silicon Data data 有冇 discrepancy
- [ ] **Read Kael Research GPU Economics article**（inference cost analysis）
- [ ] **Update dashboard with 今日嘅 data point**

**Output：** 🔍 跨 provider data comparison notes

---

### Day 5: 6/22 (Tue) — 廣州 Day 2，晚上返 HK

**主要 research session（~2-3 hrs）：**

- [ ] **Build correlation matrix**（用儲咗一星期嘅 data）
      - H100 spot vs NVDA
      - H100 spot vs BTC
      - H100 spot vs USD index
      - H100 spot vs Natural Gas
- [ ] **初步 inference：** 邊啲 correlation 有意義？
- [ ] **Write research note #1**：Compute Market Structure 觀測總結

**Output：** 📝 Research Note #1 Draft

---

### Day 6: 6/23 (Wed) — 全天可用 🎯 Wrap-up

**衝刺日（~4 hrs）：**

- [ ] **Finalize Research Note #1**（可以 share 俾朋友／齋自己 keep）
- [ ] **Cancel Silicon Data trial**（如果唔打算俾 $499/mo）
- [ ] **決定下一階段方向：**
      - 繼續免費 data tracking（weekly snapshot）
      - 定係 subscribe SemiAnalysis data product？
      - 定係等 CME futures 上市先再 active？
- [ ] **Set up ongoing data collection cron job**
- [ ] **Review the week's findings with me** — 我可以幫你 synthesize

**Output：** ✅ Phase 1 Complete — Documented knowledge + data pipeline

---

### Day 7: 6/24 (Thu) — 生日 🎂 放鬆

**唔好做 research，享受生日 😊**

---

## 📋 Daily Data Pipeline（我幫你自動化）

我會 set 好一個 script 每日自動 collect 公開 GPU price data：

```
每日自動收集：
├─ GPU Tracker 嘅 public stats（5,213 listings）
├─ SemiAnalysis public preview（H100 spot）
├─ NVDA / BTC / USD index closing price
└─ → Append to CSV
```

噉你每日打開睇下就得，唔使手動收集。

---

## 🎯 6 日結束時你會有嘅嘢

| Deliverable | Status |
|:------------|:-------|
| 1️⃣ GPU Price Dashboard v1（至少 5 日 data points） | 🔲 |
| 2️⃣ H100 2023-2026 Price History Analysis | 🔲 |
| 3️⃣ Correlation Matrix（GPU × NVDA × BTC × USD × Energy） | 🔲 |
| 4️⃣ Research Note #1：「Compute Market Structure & Macro Implications」 | 🔲 |
| 5️⃣ Automated Data Pipeline（每日自動 collect） | 🔲 |
| 6️⃣ 清楚決定：下一階段要點推進（追 CME 定繼續自己收集） | 🔲 |

---

## ⚠️ 注意點

- **Silicon Data trial $499/mo** — 可以 7 日 free trial，到期前 cancel
- **SemiAnalysis 嘅 public preview 係免費嘅** — 你唔使俾錢就有個 overview
- **GPU Tracker 係免費嘅** — 最全面的 public dataset
- **總預算**：如果你只係用 free tier + trial，呢個假期可以 $0 完成第一階段
