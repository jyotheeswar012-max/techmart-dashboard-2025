# 🔄 Pipeline — One-Time ETL Script

> **Note:** This pipeline was run **once** to generate the static 2025 TechMart dataset used in the dashboard.
> It is **not** scheduled for daily or automated runs.
> The code is preserved here to demonstrate ETL and data cleaning methodology.

## What it does

- `fetch_data.py` — Downloads market context via `yfinance`, cleans raw sales data, enriches with optional FX rates, and outputs:
  - `data/superstore_snapshot_YYYYMMDD.csv`
  - `data/market_context.csv`
  - `data/kpi_summary.json`

## Run manually (optional)

```bash
pip install -r requirements.txt
python pipeline/fetch_data.py
```

For a live, auto-updating dashboard, see upcoming projects.
