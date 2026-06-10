# 🛍️ TechMart Business Analytics Dashboard 2025

[![Live Dashboard](https://img.shields.io/badge/🚀%20Live%20Demo-GitHub%20Pages-success?style=for-the-badge)](https://jyotheeswar012-max.github.io/techmart-dashboard-2025/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![pytest](https://img.shields.io/badge/Tests-pytest%2018%20cases-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](./tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

> **An end-to-end retail analytics project** demonstrating data pipeline automation, 16+ interactive charts, an interactive **What-If Scenario Analysis Engine**, and a full pytest test suite — transforming raw transaction data into actionable business decisions.

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

## 💡 Key Business Insights

> *"Analysis of 9,353 transactions reveals that discounts over 20% erode profit margins by ~15% — dropping from 31.7% to under 17% — suggesting a tiered discount cap strategy for low-margin categories could recover an estimated $130K+ in annual profit."*

### Top 3 Findings

1. **🏷️ Discount Danger Zone**: Net margin collapses at the 21%+ bracket (turns negative at –0.2%). Limiting discounts to ≤15% for Books, Food, and Sports could protect ~$130K in annual profit.

2. **📅 Q4 Dominance & Risk**: Q4 generated 32.9% of annual revenue ($1.75M). A stockout scenario in Electronics during November–December would disproportionately impact the full-year P&L — demand forecasting is critical.

3. **🎂 36–45 is the Power Cohort**: The 36–45 age group contributes 31.7% of revenue ($1.68M) with the highest average order value. Retention-focused loyalty program enhancements for this segment yield the highest expected ROI.

---

## 🔬 Scenario Analysis ("What-If" Engine)

The dashboard includes an **interactive Scenario Analysis tab** powered by live JavaScript calculations:

```
📈 Optimistic (+10% growth, stable margin):  Revenue $5.84M  |  Profit $1.85M  |  +$170K
📉 Pessimistic (−5% decline, margin −2pp):   Revenue $5.05M  |  Profit $1.46M  |  −$218K
🏷️ Discount +5% (margin impact −2.8pp):      Revenue $5.31M  |  Profit $1.53M  |  −$144K
🆕 New Category +$200K:                       Revenue $5.51M  |  Profit $1.74M  |  + $68K
```

Use the sliders at `/scenario` tab to model any combination in real time.

---

## 📁 Project Structure

```
techmart-dashboard-2025/
├── docs/                        # ✅ GitHub Pages (live dashboard)
│   └── index.html               # Self-contained: 16+ Plotly charts + Scenario Engine
├── pipeline/                    # ✨ Automated data pipeline
│   ├── __init__.py
│   └── fetch_data.py            # yfinance + requests + metric helpers
├── tests/                       # ✅ pytest test suite (18 tests)
│   ├── __init__.py
│   ├── test_metrics.py          # CAGR, margin, scenario — 13 unit tests
│   └── test_pipeline_integration.py  # 5 integration tests
├── scenario_analysis/           # 📈 What-If analysis documentation
│   └── README.md
├── superstore_2025_full.csv     # Source dataset (9,353 transactions)
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🔄 Automated Data Pipeline

```bash
# Run full pipeline (fetches market data + creates timestamped snapshot)
python pipeline/fetch_data.py
```

| Source | Library | Data Fetched |
|---|---|---|
| Stock/ETF prices | `yfinance` | SPY, QQQ, XRT (Retail sector ETF) |
| FX Rates | `requests` + OXR API | USD cross rates (set `OXR_APP_ID` env var) |
| Internal Sales | CSV → snapshot | Timestamped export to `data/` |

---

## ✅ Running Tests

```bash
pip install -r requirements.txt

# Run all 18 tests
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=pipeline --cov-report=term-missing
```

**Coverage:**
- `calculate_cagr` — 8 tests (known values, edge cases, error handling)
- `calculate_profit_margin` — 5 tests
- `scenario_revenue_impact` — 5 tests
- `refresh_superstore_snapshot` — integration tests

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2-purple?style=flat-square)
![pytest](https://img.shields.io/badge/pytest-7.x-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

---

## 🚀 Quick Start

```bash
git clone https://github.com/jyotheeswar012-max/techmart-dashboard-2025.git
cd techmart-dashboard-2025
pip install -r requirements.txt

python pipeline/fetch_data.py   # run pipeline
pytest tests/ -v                # run tests
open docs/index.html            # open dashboard locally
```

---

## 📄 License

MIT © 2025 [A. Jyotheeswar Reddy](https://www.linkedin.com/in/a-jyotheeswar-reddy/)
