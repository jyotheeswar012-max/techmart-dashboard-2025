# 🛍️ TechMart Business Analytics Dashboard 2025

[![Live Dashboard](https://img.shields.io/badge/🚀%20Live%20Demo-GitHub%20Pages-success?style=for-the-badge)](https://jyotheeswar012-max.github.io/techmart-dashboard-2025/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?style=flat-square&logo=plotly&logoColor=white)](https://plotly.com)
[![pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)](./tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](./LICENSE)

> **An end-to-end retail analytics project** — automated data pipeline, 12+ interactive charts, scenario analysis engine, and a full pytest test suite.

---

## 📊 Live Dashboard

**👉 [View Live →](https://jyotheeswar012-max.github.io/techmart-dashboard-2025/)**

| Metric | Value |
|---|---|
| 💰 Total Revenue | $5,357,458 |
| 🛝 Transactions | 9,353 |
| 👥 Customers | 1,198 |
| 📈 Interactive Charts | 12+ |
| 🌎 Regions Covered | 4 (US National) |

---

## 📁 Project Structure

```
techmart-dashboard-2025/
├── docs/                        # GitHub Pages (live dashboard)
│   └── index.html
├── pipeline/                    # ✨ Automated data pipeline
│   ├── __init__.py
│   └── fetch_data.py            # yfinance + requests + metric helpers
├── tests/                       # ✅ pytest test suite
│   ├── __init__.py
│   ├── test_metrics.py          # Unit tests: CAGR, margin, scenario
│   └── test_pipeline_integration.py
├── scenario_analysis/           # 📈 What-If analysis documentation
│   └── README.md
├── superstore_2025_full.csv     # Source dataset (9,353 transactions)
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🔄 Automated Data Pipeline

The `pipeline/fetch_data.py` module replaces static CSV files with a live data ingestion system:

```bash
# Run the full pipeline
python pipeline/fetch_data.py
```

| Source | Library | Data |
|---|---|---|
| Stock/ETF prices | `yfinance` | SPY, QQQ, XRT (Retail ETF) |
| FX rates | `requests` + Open Exchange Rates | USD cross rates |
| Internal sales | CSV → timestamped snapshot | Superstore transactions |

**Output:** `data/market_context.csv`, `data/fx_rates.csv`, `data/superstore_snapshot_YYYYMMDD.csv`

---

## 📈 Scenario Analysis

Ask "What if?" questions and see the impact on revenue and profit:

```python
from pipeline.fetch_data import scenario_revenue_impact

# What if TechMart grows 5% next year?
result = scenario_revenue_impact(
    base_revenue=5_357_458,
    growth_pct=0.05,
    margin=0.1245
)
# Projected Revenue: $5,625,331  |  Delta: +$267,873
```

See [`scenario_analysis/README.md`](./scenario_analysis/README.md) for full scenarios (optimistic, pessimistic, margin compression).

---

## ✅ Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests with coverage
pytest tests/ -v --tb=short

# With coverage report
pytest tests/ -v --cov=pipeline --cov-report=term-missing
```

**Test coverage includes:**
- `calculate_cagr` — 8 test cases (happy path, edge cases, error handling)
- `calculate_profit_margin` — 5 test cases
- `scenario_revenue_impact` — 5 test cases
- `refresh_superstore_snapshot` — integration tests

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-0.2-purple?style=flat-square)
![pytest](https://img.shields.io/badge/pytest-7.x-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)

---

## 🚀 Quick Start

```bash
git clone https://github.com/jyotheeswar012-max/techmart-dashboard-2025.git
cd techmart-dashboard-2025
pip install -r requirements.txt

# Run pipeline
python pipeline/fetch_data.py

# Run tests
pytest tests/ -v

# Open dashboard
open docs/index.html
```

---

## 📄 License

MIT © 2025 [A. Jyotheeswar Reddy](https://github.com/jyotheeswar012-max)
