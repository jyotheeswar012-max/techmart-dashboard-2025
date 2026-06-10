"""
Integration tests — pipeline utilities
=======================================
These tests run without network access (no yfinance/API calls).
Run:  pytest tests/ -v
"""

import os
import sys
import tempfile
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pipeline.fetch_data import refresh_superstore_snapshot


class TestRefreshSuperstoreSnapshot:
    def test_missing_source_returns_empty_df(self):
        df = refresh_superstore_snapshot(source_csv="/nonexistent/path.csv")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_snapshot_adds_pipeline_run_at_column(self, tmp_path):
        """Create a tiny CSV and confirm the pipeline adds timestamp column."""
        sample = pd.DataFrame({
            "Order ID": ["CA-001", "CA-002"],
            "Sales": [100.0, 250.0],
            "Profit": [20.0, 50.0],
        })
        src = tmp_path / "sample.csv"
        sample.to_csv(src, index=False)

        # Patch output dir to tmp_path
        import pipeline.fetch_data as fd
        original_dir = fd.OUTPUT_DIR
        fd.OUTPUT_DIR = str(tmp_path)

        result = refresh_superstore_snapshot(source_csv=str(src))

        fd.OUTPUT_DIR = original_dir  # restore

        assert "pipeline_run_at" in result.columns
        assert len(result) == 2
