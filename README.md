# 🛍️ TechMart Business Analytics Dashboard 2025

[![Live Dashboard](https://img.shields.io/badge/🚀%20Live%20Demo-GitHub%20Pages-success?style=for-the-badge)](https://jyotheeswar012-max.github.io/techmart-dashboard-2025/)
[![Daily Pipeline](https://github.com/jyotheeswar012-max/techmart-dashboard-2025/actions/workflows/pipeline.yml/badge.svg)](https://github.com/jyotheeswar012-max/techmart-dashboard-2025/actions/workflows/pipeline.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![pytest](https://img.shields.io/badge/Tests-pytest%2018%20cases-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](./tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

> **An end-to-end retail analytics project** — automated data pipeline, 16+ interactive Plotly charts, a live **What-If Scenario Analysis Engine**, and a full pytest test suite. Raw transaction data → actionable business decisions.

---

## 🚀 Live Dashboard

**👉 [Open Interactive Dashboard →](https://jyotheeswar012-max.github.io/techmart-dashboard-2025/)**

| Metric | Value |
|---|---|
| 💰 Total Revenue | $5,311,299 |
| 📈 Total Profit | $1,677,063 |
| 📊 Avg Profit Margin | 31.7% |
| 🧾 Transactions | 9,353 |
| 👥 Unique Customers | 1,198 |
| 🌍 Regions | 4 (US National) |
| 📦 Categories | 7 |
| 📉 Interactive Charts | 16+ |

---

## 📸 Dashboard Screenshots

> All charts are fully interactive in the live dashboard — hover for tooltips, click to filter, drag to zoom.

### Overview Tab — KPI Header & Monthly Trend

![Overview — KPI header, 8 metric cards, Monthly Sales & Profit dual-axis chart](https://github.com/user-attachments/assets/ef86d4e7-2f35-40ba-aabb-2f0d464819ec)

### Overview Tab — Growth, Quarterly & Regional Breakdown

![Overview — MoM Revenue Growth %, Quarterly Performance, Revenue by Region, Customer Segment Split](https://github.com/user-attachments/assets/b7fd8183-bff6-4a40-8fe0-d72f06d39ad2)

### Products & Categories — Revenue, Margin & Top 10

![Products — Category Revenue vs Profit grouped bar, Profit Margin % by Category with avg line, Top 10 Products horizontal bar](https://github.com/user-attachments/assets/094ea927-bbb7-4ee2-86e5-6a69352c1ec7)

### Products — Discount Impact & Category Treemap

![Products — Discount Bracket Sales & Margin Impact dual-axis chart, Category Revenue Share Treemap](https://github.com/user-attachments/assets/55a16b0f-aff4-496f-a3f7-6b8e4c1f29f8)

### Customers Tab — Age Groups, Payments & Loyalty

![Customers — Revenue & Profit by Age Group, Payment Method Usage, Loyalty Tier Donut, Segment Revenue vs Profit Bubble](https://github.com/user-attachments/assets/82cd6e69-9330-411c-ac2e-1f322bd5c9f9)

### Operations Tab — Day of Week, Shipping & Cumulative YTD

![Operations — Sales by Day of Week (weekend peak highlighted), Shipping Mode Analysis, Revenue by Region Donut, Cumulative Revenue YTD vs Target](https://github.com/user-attachments/assets/81ee0891-d612-4bdb-a9d8-e8e00bde38b6)

### Scenario Analysis Engine — Live What-If Sliders

![Scenario Analysis — 4 interactive sliders, projected KPI cards updating in real time, Scenario vs Baseline bar chart, Sensitivity line chart](https://github.com/user-attachments/assets/9061fcc6-eb21-452d-953d-eb22cf80164a)

### Key Insights Tab — Business Narrative & Analytics

![Key Insights — 6 insight cards with business recommendations, Revenue Concentration Pareto chart, Profit Margin Heatmap by Category & Region](https://github.com/user-attachments/assets/cdbaf2e6-b7b4-4c5c-9fec-c294abe090de)

---

## 💡 Key Business Insights

> *"Analysis of 9,353 transactions reveals that discounts over 20% erode profit margins by ~15% — dropping from 31.7% to under 17% — suggesting a tiered discount cap strategy for low-margin categories could recover an estimated $130K+ in annual profit."*

1. **🏷️ Discount Danger Zone** — Net margin turns negative at the 21%+ bracket. Limiting discounts to ≤15% for Books, Food, and Sports could protect ~$130K in annual profit.

2. **📅 Q4 Dominance & Risk** — Q4 generated 32.9% of annual revenue ($1.75M). A stockout scenario in Electronics during Nov–Dec would disproportionately impact the full-year P&L — demand forecasting is critical.

3. **🎂 36–45 is the Power Cohort** — The 36–45 age group contributes 31.7% of revenue ($1.68M) with the highest average order value. Retention-focused loyalty program enhancements for this segment yield the highest expected ROI.

---

## 🔬 Scenario Analysis Engine

The dashboard's **Scenario tab** runs live JavaScript calculations as you drag sliders:

```
📈 Optimistic  (+10% growth, stable margin)   →  Revenue $5.84M  |  Profit $1.85M  |  +$170K
📉 Pessimistic (−5% decline, margin −2pp)     →  Revenue $5.05M  |  Profit $1.46M  |  −$218K
🏷️  Discount +5pp (margin impact −2.8pp)      →  Revenue $5.31M  |  Profit $1.53M  |  −$144K
🆕 New Category +$200K                         →  Revenue $5.51M  |  Profit $1.74M  |  + $68K
```

---

## 📁 Project Structure

```
techmart-dashboard-2025/
├── index.html                   # ✅ GitHub Pages root (full dashboard)
├── docs/
│   ├── index.html               # Mirror copy for /docs Pages config
│   └── screenshots/             # Dashboard screenshots
├── pipeline/
│   ├── __init__.py
│   └── fetch_data.py            # Automated pipeline
├── tests/
│   ├── __init__.py
│   ├── test_metrics.py          # 13 unit tests
│   └── test_pipeline_integration.py  # 5 integration tests
├── data/                        # Pipeline outputs (auto-generated)
│   ├── market_context.csv
│   ├── fx_rates.csv
│   ├── kpi_summary.json
│   └── superstore_snapshot_YYYYMMDD.csv
├── .github/workflows/
│   └── pipeline.yml             # Daily cron at 06:00 UTC
├── superstore_2025_full.csv     # Source dataset (9,353 rows)
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🔄 Data Pipeline — Setup Guide

The pipeline has **zero required configuration** — it runs out of the box.
The `OXR_APP_ID` variable is **100% optional** (FX rate enrichment only).

### Quickstart (no API keys needed)

```bash
git clone https://github.com/jyotheeswar012-max/techmart-dashboard-2025.git
cd techmart-dashboard-2025
pip install -r requirements.txt
python pipeline/fetch_data.py
```

**What runs without any API key:**

| Step | Source | Output | Requires Key? |
|---|---|---|---|
| Market data | `yfinance` (free) | `data/market_context.csv` | ❌ No |
| Sales snapshot | Local CSV | `data/superstore_snapshot_YYYYMMDD.csv` | ❌ No |
| KPI summary | Computed | `data/kpi_summary.json` | ❌ No |
| FX rates | Open Exchange Rates | `data/fx_rates.csv` | ✅ Optional |

### Optional: Enable FX Rate Enrichment

```bash
export OXR_APP_ID="your_app_id_here"
python pipeline/fetch_data.py
```

### CLI flags

```bash
python pipeline/fetch_data.py --dry-run
python pipeline/fetch_data.py --period 3mo
```

### Automated via GitHub Actions

Runs **daily at 06:00 UTC** via `.github/workflows/pipeline.yml`.
Check run history: [Actions tab →](https://github.com/jyotheeswar012-max/techmart-dashboard-2025/actions)

---

## ✅ Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
pytest tests/ -v --cov=pipeline --cov-report=term-missing
```

| Test file | Cases | Covers |
|---|---|---|
| `test_metrics.py` | 13 | `calculate_cagr`, `calculate_profit_margin`, `scenario_revenue_impact` |
| `test_pipeline_integration.py` | 5 | `refresh_superstore_snapshot`, `generate_kpi_summary` |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2-purple?style=flat-square)
![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

---

## 📄 License

MIT © 2025 [A. Jyotheeswar Reddy](https://www.linkedin.com/in/a-jyotheeswar-reddy/)
