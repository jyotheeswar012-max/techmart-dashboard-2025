"""
TechMart Data Pipeline
======================
Automated daily data ingestion, transformation, and KPI export.

Usage:
    python pipeline/fetch_data.py          # run all steps
    python pipeline/fetch_data.py --dry-run  # validate without writing files

Sources:
    - yfinance  : live market & retail-sector ETF data
    - requests  : FX rates (Open Exchange Rates free tier)
    - pandas    : transform & export to data/
    - json      : KPI summary for downstream consumers

Outputs (written to data/):
    market_context.csv       — daily closing prices for SPY, QQQ, XRT
    fx_rates.csv             — latest USD exchange rates
    superstore_snapshot_YYYYMMDD.csv — timestamped data snapshot
    kpi_summary.json         — aggregated KPIs for dashboard consumption
    pipeline_log.txt         — append-only run log
"""

import os
import sys
import json
import logging
import datetime
import argparse
import time
from pathlib import Path

import pandas as pd

# ── Optional dependencies (graceful fallback) ─────────────────────────────────
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "data"
LOG_FILE = OUTPUT_DIR / "pipeline_log.txt"
SOURCE_CSV = ROOT_DIR / "superstore_2025_full.csv"

# ── Logging setup ─────────────────────────────────────────────────────────────
def setup_logging(dry_run: bool = False) -> logging.Logger:
    """Configure console + file logging."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fmt = "%(asctime)s  %(levelname)-8s  %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]
    if not dry_run:
        handlers.append(logging.FileHandler(LOG_FILE, encoding="utf-8"))
    logging.basicConfig(level=logging.INFO, format=fmt, datefmt=datefmt, handlers=handlers)
    return logging.getLogger("techmart_pipeline")


# ── Retry helper ──────────────────────────────────────────────────────────────
def _with_retry(fn, retries: int = 3, delay: float = 2.0, logger: logging.Logger = None):
    """Call fn() up to `retries` times, sleeping `delay` seconds between attempts."""
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except Exception as exc:
            msg = f"Attempt {attempt}/{retries} failed: {exc}"
            if logger:
                logger.warning(msg)
            else:
                print(f"[WARN] {msg}")
            if attempt < retries:
                time.sleep(delay)
    raise RuntimeError(f"All {retries} attempts failed for {fn.__name__}")


# ── 1. Market Context ─────────────────────────────────────────────────────────
def fetch_market_context(
    tickers: list[str] | None = None,
    period: str = "1mo",
    dry_run: bool = False,
    logger: logging.Logger = None,
) -> pd.DataFrame:
    """
    Fetch daily closing prices for SPY, QQQ, and XRT (retail sector ETF).
    These provide macro context for interpreting TechMart sales trends.

    Args:
        tickers:  List of Yahoo Finance ticker symbols. Defaults to [SPY, QQQ, XRT].
        period:   Lookback period string accepted by yfinance (e.g. '1mo', '3mo', '1y').
        dry_run:  If True, fetches data but does NOT write to disk.
        logger:   Logger instance.

    Returns:
        DataFrame with columns [date, SPY, QQQ, XRT] or empty DataFrame on failure.
    """
    log = logger or logging.getLogger("techmart_pipeline")
    if not HAS_YFINANCE:
        log.warning("yfinance not installed — skipping market context. Run: pip install yfinance")
        return pd.DataFrame()

    tickers = tickers or ["SPY", "QQQ", "XRT"]
    log.info("Fetching market data for: %s (period=%s)", tickers, period)

    try:
        def _download():
            return yf.download(tickers, period=period, auto_adjust=True, progress=False)

        raw = _with_retry(_download, logger=log)

        if raw.empty:
            log.warning("yfinance returned empty DataFrame for %s", tickers)
            return pd.DataFrame()

        close = raw["Close"].reset_index()
        close.rename(columns={"Date": "date"}, inplace=True)
        close["date"] = pd.to_datetime(close["date"]).dt.date

        if not dry_run:
            out_path = OUTPUT_DIR / "market_context.csv"
            close.to_csv(out_path, index=False)
            log.info("Saved → %s  (%d rows)", out_path, len(close))
        else:
            log.info("[DRY-RUN] Would save market_context.csv (%d rows)", len(close))

        return close

    except Exception as exc:
        log.error("fetch_market_context failed: %s", exc, exc_info=True)
        return pd.DataFrame()


# ── 2. FX Rates ────────────────────────────────────────────────────────────────
def fetch_fx_rates(
    app_id: str = "",
    dry_run: bool = False,
    logger: logging.Logger = None,
) -> dict:
    """
    Fetch latest USD exchange rates via Open Exchange Rates (free tier).
    Set environment variable OXR_APP_ID with your free API key.
    Sign up at https://openexchangerates.org — no credit card required.

    Args:
        app_id:   API key. Falls back to OXR_APP_ID env var if not provided.
        dry_run:  If True, fetches but does NOT write to disk.
        logger:   Logger instance.

    Returns:
        dict mapping currency codes to float rates (base=USD),
        or empty dict if app_id not configured.
    """
    log = logger or logging.getLogger("techmart_pipeline")
    if not HAS_REQUESTS:
        log.warning("requests not installed — skipping FX fetch. Run: pip install requests")
        return {}

    app_id = app_id or os.getenv("OXR_APP_ID", "")
    if not app_id:
        log.info("OXR_APP_ID not set — skipping FX fetch (optional enrichment).")
        return {}

    url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}&base=USD"
    log.info("Fetching FX rates from Open Exchange Rates...")

    try:
        def _fetch():
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()

        payload = _with_retry(_fetch, logger=log)
        rates = payload.get("rates", {})

        if not rates:
            log.warning("OXR response contained no rates — check your API key.")
            return {}

        df = pd.DataFrame(list(rates.items()), columns=["currency", "rate_vs_usd"])
        df.sort_values("currency", inplace=True)

        if not dry_run:
            out_path = OUTPUT_DIR / "fx_rates.csv"
            df.to_csv(out_path, index=False)
            log.info("Saved → %s  (%d currencies)", out_path, len(df))
        else:
            log.info("[DRY-RUN] Would save fx_rates.csv (%d currencies)", len(df))

        return rates

    except Exception as exc:
        log.error("fetch_fx_rates failed: %s", exc, exc_info=True)
        return {}


# ── 3. Superstore Snapshot ─────────────────────────────────────────────────────
def refresh_superstore_snapshot(
    source_csv: str | Path | None = None,
    dry_run: bool = False,
    logger: logging.Logger = None,
) -> pd.DataFrame:
    """
    Read the master sales CSV, validate schema, stamp with a run timestamp,
    and write a dated snapshot to data/.

    In a production environment this step would call an ERP API or database;
    here it demonstrates the transform-and-snapshot pattern used in real pipelines.

    Args:
        source_csv: Path to the source CSV. Defaults to superstore_2025_full.csv.
        dry_run:    If True, reads and validates but does NOT write to disk.
        logger:     Logger instance.

    Returns:
        Processed DataFrame, or empty DataFrame if source not found.

    Raises:
        ValueError: if required columns are missing from the source CSV.
    """
    log = logger or logging.getLogger("techmart_pipeline")
    src = Path(source_csv) if source_csv else SOURCE_CSV

    if not src.exists():
        log.error("Source CSV not found: %s", src)
        return pd.DataFrame()

    log.info("Reading source CSV: %s", src)
    df = pd.read_csv(src)
    log.info("Loaded %d rows × %d columns", *df.shape)

    # Schema validation — fail fast if expected columns are absent
    required_cols = {"Order ID", "Sales", "Profit", "Category", "Region", "Order Date"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Source CSV is missing required columns: {missing}")

    # Light transforms
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["pipeline_run_at"] = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

    stamp = datetime.datetime.utcnow().strftime("%Y%m%d")
    out_path = OUTPUT_DIR / f"superstore_snapshot_{stamp}.csv"

    if not dry_run:
        df.to_csv(out_path, index=False)
        log.info("Snapshot saved → %s  (%d rows)", out_path, len(df))
    else:
        log.info("[DRY-RUN] Would save %s (%d rows)", out_path.name, len(df))

    return df


# ── 4. KPI Summary Export ──────────────────────────────────────────────────────
def generate_kpi_summary(
    df: pd.DataFrame,
    dry_run: bool = False,
    logger: logging.Logger = None,
) -> dict:
    """
    Compute top-level KPIs from the snapshot DataFrame and export as JSON.
    This JSON can be consumed by a live dashboard or monitoring system.

    Computed KPIs:
        - total_revenue, total_profit, profit_margin_pct
        - transaction_count, avg_order_value
        - revenue_by_category (dict)
        - revenue_by_region   (dict)
        - top_product         (str)
        - generated_at        (ISO 8601 timestamp)

    Args:
        df:       Snapshot DataFrame (output of refresh_superstore_snapshot).
        dry_run:  If True, computes but does NOT write to disk.
        logger:   Logger instance.

    Returns:
        dict of computed KPIs.
    """
    log = logger or logging.getLogger("techmart_pipeline")

    if df.empty:
        log.warning("generate_kpi_summary received empty DataFrame — skipping.")
        return {}

    try:
        total_rev = float(df["Sales"].sum())
        total_profit = float(df["Profit"].sum())
        margin = total_profit / total_rev if total_rev else 0.0
        txn_count = int(df["Order ID"].nunique())
        avg_order = total_rev / txn_count if txn_count else 0.0

        rev_by_cat = (
            df.groupby("Category")["Sales"]
            .sum()
            .round(2)
            .sort_values(ascending=False)
            .to_dict()
        )
        rev_by_region = (
            df.groupby("Region")["Sales"]
            .sum()
            .round(2)
            .sort_values(ascending=False)
            .to_dict()
        )

        top_product = "N/A"
        if "Product Name" in df.columns:
            top_product = str(
                df.groupby("Product Name")["Sales"].sum().idxmax()
            )

        summary = {
            "generated_at": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "total_revenue": round(total_rev, 2),
            "total_profit": round(total_profit, 2),
            "profit_margin_pct": round(margin * 100, 2),
            "transaction_count": txn_count,
            "avg_order_value": round(avg_order, 2),
            "revenue_by_category": rev_by_cat,
            "revenue_by_region": rev_by_region,
            "top_product": top_product,
        }

        log.info(
            "KPIs → Revenue: $%,.0f | Profit: $%,.0f | Margin: %.1f%%",
            total_rev, total_profit, margin * 100,
        )

        if not dry_run:
            out_path = OUTPUT_DIR / "kpi_summary.json"
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(summary, fh, indent=2)
            log.info("KPI summary saved → %s", out_path)
        else:
            log.info("[DRY-RUN] Would save kpi_summary.json")

        return summary

    except Exception as exc:
        log.error("generate_kpi_summary failed: %s", exc, exc_info=True)
        return {}


# ── 5. Metric Helpers (pure functions, no I/O) ─────────────────────────────────
def calculate_cagr(start_value: float, end_value: float, years: float) -> float:
    """
    Compound Annual Growth Rate.

    Args:
        start_value: Metric value at the start of the period (must be > 0).
        end_value:   Metric value at the end of the period.
        years:       Number of years in the period (must be > 0).

    Returns:
        CAGR as a decimal, e.g. 0.12 == 12%.

    Raises:
        ValueError: if start_value <= 0 or years <= 0.

    Example:
        >>> calculate_cagr(1_000_000, 1_610_510, 5)
        0.10000...  # ≈ 10% CAGR
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
        revenue: Total revenue (must be != 0).
        profit:  Net profit (may be negative).

    Returns:
        Margin as a decimal, e.g. 0.15 == 15%.

    Raises:
        ValueError: if revenue == 0.
    """
    if revenue == 0:
        raise ValueError("revenue cannot be zero")
    return profit / revenue


def scenario_revenue_impact(
    base_revenue: float,
    growth_pct: float,
    margin: float,
    discount_shift_pct: float = 0.0,
    new_category_revenue: float = 0.0,
) -> dict:
    """
    Scenario Analysis: project revenue and profit given growth assumptions.
    Mirrors the logic used in the dashboard's What-If Engine.

    Args:
        base_revenue:          Current period revenue.
        growth_pct:            Assumed organic growth rate (e.g. 0.05 == +5%).
        margin:                Current net profit margin (e.g. 0.316 == 31.6%).
        discount_shift_pct:    Change in average discount rate (e.g. 0.05 == +5pp).
                               Each +5pp erodes margin by ~2.8pp.
        new_category_revenue:  Incremental revenue from a new product category.

    Returns:
        dict with keys: base_revenue, growth_pct, projected_revenue,
        projected_profit, effective_margin, delta_revenue, delta_profit.

    Example:
        >>> scenario_revenue_impact(5_311_299, 0.05, 0.316)
        {'base_revenue': 5311299, 'growth_pct': 5.0, ...}
    """
    discount_margin_impact = (discount_shift_pct / 0.05) * (-0.028)
    effective_margin = max(0.0, margin + discount_margin_impact)
    projected_revenue = base_revenue * (1 + growth_pct) + new_category_revenue
    projected_profit = projected_revenue * effective_margin
    base_profit = base_revenue * margin

    return {
        "base_revenue": round(base_revenue, 2),
        "growth_pct": round(growth_pct * 100, 2),
        "discount_shift_pct": round(discount_shift_pct * 100, 2),
        "new_category_revenue": round(new_category_revenue, 2),
        "projected_revenue": round(projected_revenue, 2),
        "projected_profit": round(projected_profit, 2),
        "effective_margin": round(effective_margin * 100, 2),
        "delta_revenue": round(projected_revenue - base_revenue, 2),
        "delta_profit": round(projected_profit - base_profit, 2),
    }


# ── CLI entry point ────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TechMart Data Pipeline — fetch, transform, and export KPIs."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and compute without writing any output files.",
    )
    parser.add_argument(
        "--period",
        default="1mo",
        help="yfinance lookback period for market data (default: 1mo).",
    )
    return parser.parse_args()


def main() -> int:
    """Run all pipeline steps. Returns 0 on success, 1 on any step failure."""
    args = parse_args()
    log = setup_logging(dry_run=args.dry_run)
    run_ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    log.info("=" * 55)
    log.info("  TechMart Data Pipeline — %s", run_ts)
    log.info("  Mode: %s", "DRY-RUN" if args.dry_run else "LIVE")
    log.info("=" * 55)

    exit_code = 0

    # Step 1: Market context
    try:
        fetch_market_context(period=args.period, dry_run=args.dry_run, logger=log)
    except Exception as exc:
        log.error("[STEP 1] Market context failed: %s", exc)
        exit_code = 1

    # Step 2: FX rates
    try:
        fetch_fx_rates(dry_run=args.dry_run, logger=log)
    except Exception as exc:
        log.error("[STEP 2] FX rates failed: %s", exc)
        exit_code = 1

    # Step 3: Superstore snapshot
    df = pd.DataFrame()
    try:
        df = refresh_superstore_snapshot(dry_run=args.dry_run, logger=log)
    except Exception as exc:
        log.error("[STEP 3] Superstore snapshot failed: %s", exc)
        exit_code = 1

    # Step 4: KPI summary (depends on Step 3)
    try:
        summary = generate_kpi_summary(df, dry_run=args.dry_run, logger=log)
        if summary:
            log.info("[Scenario Demo] +5%% growth, 0pp discount shift:")
            result = scenario_revenue_impact(
                base_revenue=summary["total_revenue"],
                growth_pct=0.05,
                margin=summary["profit_margin_pct"] / 100,
            )
            for k, v in result.items():
                log.info("  %-28s %s", k + ":", v)
    except Exception as exc:
        log.error("[STEP 4] KPI summary failed: %s", exc)
        exit_code = 1

    status = "SUCCESS" if exit_code == 0 else "COMPLETED WITH ERRORS"
    log.info("=" * 55)
    log.info("  Pipeline %s", status)
    log.info("=" * 55)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
