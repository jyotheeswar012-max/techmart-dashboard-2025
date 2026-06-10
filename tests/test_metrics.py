"""
pytest test suite — core metric functions
==========================================
Run:  pytest tests/ -v
"""

import pytest
import sys
import os

# Make pipeline importable from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.fetch_data import (
    calculate_cagr,
    calculate_profit_margin,
    scenario_revenue_impact,
)


# ── calculate_cagr ────────────────────────────────────────────────────────────
class TestCalculateCAGR:
    def test_known_cagr(self):
        """$1 000 → $1 610.51 over 5 years ≈ 10% CAGR."""
        result = calculate_cagr(1000, 1610.51, 5)
        assert abs(result - 0.10) < 0.001

    def test_cagr_zero_growth(self):
        """Same start and end → 0% CAGR."""
        assert calculate_cagr(500, 500, 3) == pytest.approx(0.0)

    def test_cagr_one_year(self):
        """Single year: CAGR == simple growth rate."""
        result = calculate_cagr(100, 115, 1)
        assert result == pytest.approx(0.15)

    def test_cagr_raises_on_zero_start(self):
        with pytest.raises(ValueError, match="start_value"):
            calculate_cagr(0, 1000, 5)

    def test_cagr_raises_on_negative_start(self):
        with pytest.raises(ValueError):
            calculate_cagr(-100, 1000, 5)

    def test_cagr_raises_on_zero_years(self):
        with pytest.raises(ValueError, match="years"):
            calculate_cagr(100, 200, 0)

    def test_cagr_raises_on_negative_years(self):
        with pytest.raises(ValueError):
            calculate_cagr(100, 200, -2)

    def test_cagr_large_values(self):
        """TechMart scale: $5M → $8M over 4 years."""
        result = calculate_cagr(5_000_000, 8_000_000, 4)
        assert 0.12 < result < 0.13  # ~12.5%


# ── calculate_profit_margin ───────────────────────────────────────────────────
class TestCalculateProfitMargin:
    def test_standard_margin(self):
        assert calculate_profit_margin(1_000_000, 124_500) == pytest.approx(0.1245)

    def test_margin_zero_profit(self):
        assert calculate_profit_margin(500_000, 0) == pytest.approx(0.0)

    def test_margin_100_percent(self):
        assert calculate_profit_margin(100, 100) == pytest.approx(1.0)

    def test_margin_raises_on_zero_revenue(self):
        with pytest.raises(ValueError, match="revenue"):
            calculate_profit_margin(0, 5000)

    def test_margin_negative_profit(self):
        """Loss scenario returns negative margin."""
        result = calculate_profit_margin(100_000, -20_000)
        assert result == pytest.approx(-0.20)


# ── scenario_revenue_impact ───────────────────────────────────────────────────
class TestScenarioRevenueImpact:
    BASE = 5_357_458
    MARGIN = 0.1245

    def test_five_percent_growth(self):
        result = scenario_revenue_impact(self.BASE, 0.05, self.MARGIN)
        assert result["projected_revenue"] == pytest.approx(self.BASE * 1.05, rel=1e-3)
        assert result["growth_pct"] == 5.0

    def test_zero_growth(self):
        result = scenario_revenue_impact(self.BASE, 0.0, self.MARGIN)
        assert result["delta_revenue"] == pytest.approx(0.0, abs=1)
        assert result["projected_revenue"] == pytest.approx(self.BASE, rel=1e-3)

    def test_negative_growth(self):
        """Recession scenario: -10% revenue."""
        result = scenario_revenue_impact(self.BASE, -0.10, self.MARGIN)
        assert result["delta_revenue"] < 0

    def test_projected_profit_consistency(self):
        """projected_profit = projected_revenue * margin."""
        result = scenario_revenue_impact(self.BASE, 0.08, self.MARGIN)
        expected_profit = result["projected_revenue"] * self.MARGIN
        assert result["projected_profit"] == pytest.approx(expected_profit, rel=1e-2)

    def test_return_keys(self):
        result = scenario_revenue_impact(1_000_000, 0.1, 0.2)
        expected_keys = {
            "base_revenue", "growth_pct", "projected_revenue",
            "projected_profit", "delta_revenue"
        }
        assert set(result.keys()) == expected_keys
