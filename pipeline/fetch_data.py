"""
TechMart Data Pipeline
======================
Automates daily data ingestion from multiple sources.
Replaces static CSV with a live, scheduled pipeline.

Usage:
    python pipeline/fetch_data.py

Sources:
    - yfinance  : stock/market data for macro context
    - requests  : REST API calls (Alpha Vantage / Open Exchange)
    - pandas    : transform & export to data/
"""

import os
import datetime
import pandas as pd

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("[WARN] yfinance not installed. Run: pip install yfinance")

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── 1. Market Context (via yfinance) ──────────────────────────────────────────
def fetch_market_context(tickers: list[str] = None, period: str = "1mo") -> pd.DataFrame:
    """
    Fetch closing prices for a list of tickers.
    Default: S&P 500 ETF + NASDAQ ETF as macro context.
    """
    if not HAS_YFINANCE:
        return pd.DataFrame()

    tickers = tickers or ["SPY", "QQQ", "XRT"]  # XRT = Retail sector ETF
    print(f"[pipeline] Fetching market data for: {tickers}")
    raw = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    close = raw["Close"].reset_index()
    close.rename(columns={"Date": "date"}, inplace=True)
    out_path = os.path.join(OUTPUT_DIR, "market_context.csv")
    close.to_csv(out_path, index=False)
    print(f"[pipeline] Saved → {out_path}")
    return close


# ── 2. FX Rates (via Open Exchange Rates free tier) ───────────────────────────
def fetch_fx_rates(app_id: str = "") -> dict:
    """
    Fetch latest USD exchange rates.
    Sign up free at https://openexchangerates.org
    Set env var: OXR_APP_ID=your_app_id
    """
    if not HAS_REQUESTS:
        return {}

    app_id = app_id or os.getenv("OXR_APP_ID", "")
    if not app_id:
        print("[pipeline] OXR_APP_ID not set — skipping FX fetch.")
        return {}

    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}&base=USD"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json().get("rates", {})
    df = pd.DataFrame(list(data.items()), columns=["currency", "rate_vs_usd"])
    out_path = os.path.join(OUTPUT_DIR, "fx_rates.csv")
    df.to_csv(out_path, index=False)
    print(f"[pipeline] Saved → {out_path}")
    return data


# ── 3. Retail Sales Snapshot (simulated refresh of superstore data) ────────────
def refresh_superstore_snapshot(source_csv: str = None) -> pd.DataFrame:
    """
    In a real pipeline this would call an internal ERP API or database.
    Here we read the existing CSV, add a 'pipeline_run_at' timestamp,
    and write a timestamped snapshot to data/.
    """
    source_csv = source_csv or os.path.join(
        os.path.dirname(__file__), "..", "superstore_2025_full.csv"
    )
    if not os.path.exists(source_csv):
        print(f"[pipeline] Source not found: {source_csv}")
        return pd.DataFrame()

    df = pd.read_csv(source_csv)
    df["pipeline_run_at"] = datetime.datetime.utcnow().isoformat()
    stamp = datetime.datetime.utcnow().strftime("%Y%m%d")
    out_path = os.path.join(OUTPUT_DIR, f"superstore_snapshot_{stamp}.csv")
    df.to_csv(out_path, index=False)
    print(f"[pipeline] Snapshot saved → {out_path}  ({len(df):,} rows)")
    return df


# ── 4. Metrics computation helpers ────────────────────────────────────────────
def calculate_cagr(start_value: float, end_value: float, years: float) -> float:
    """
    Compound Annual Growth Rate.

    Args:
        start_value: Revenue / metric at start of period.
        end_value:   Revenue / metric at end of period.
        years:       Number of years in the period.

    Returns:
        CAGR as a decimal (e.g. 0.12 = 12%).

    Raises:
        ValueError: if start_value <= 0 or years <= 0.
    """
    if start_value <= 0:
        raise ValueError(f"start_value must be > 0, got {start_value}")
    if years <= 0:
        raise ValueError(f"years must be > 0, got {years}")
    return (end_value / start_value) ** (1 / years) - 1


def calculate_profit_margin(revenue: float, profit: float) -> float:
    """
    Net profit margin as a decimal.

    Args:
        revenue: Total revenue.
        profit:  Net profit.

    Returns:
        Margin as a decimal (e.g. 0.15 = 15%).

    Raises:
        ValueError: if revenue == 0.
    """
    if revenue == 0:
        raise ValueError("revenue cannot be zero")
    return profit / revenue


def scenario_revenue_impact(
    base_revenue: float,
    growth_pct: float,
    margin: float
) -> dict:
    """
    Scenario Analysis: project revenue and profit given a growth assumption.

    Args:
        base_revenue: Current period revenue.
        growth_pct:   Assumed growth rate (e.g. 0.05 for +5%).
        margin:       Current profit margin (e.g. 0.12 for 12%).

    Returns:
        dict with projected_revenue, projected_profit, delta_revenue.
    """
    projected_revenue = base_revenue * (1 + growth_pct)
    projected_profit = projected_revenue * margin
    return {
        "base_revenue": round(base_revenue, 2),
        "growth_pct": round(growth_pct * 100, 2),
        "projected_revenue": round(projected_revenue, 2),
        "projected_profit": round(projected_profit, 2),
        "delta_revenue": round(projected_revenue - base_revenue, 2),
    }


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  TechMart Data Pipeline — " + datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    print("=" * 55)

    fetch_market_context()
    fetch_fx_rates()
    refresh_superstore_snapshot()

    # Quick demo of scenario analysis
    result = scenario_revenue_impact(
        base_revenue=5_357_458,
        growth_pct=0.05,
        margin=0.1245
    )
    print("\n[Scenario] +5% revenue growth impact:")
    for k, v in result.items():
        print(f"  {k:25s}: {v}")

    print("\n[pipeline] Done.")
