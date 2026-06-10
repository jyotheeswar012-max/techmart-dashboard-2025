# 📈 Scenario Analysis

This module demonstrates **"What-If" business analysis** — a key skill for data analysts and data scientists. Instead of just showing historical data, scenario analysis lets stakeholders model future outcomes.

---

## What Is It?

Scenario analysis answers questions like:

| Question | Parameter | Impact Metric |
|---|---|---|
| What if revenue grows by 5%? | `growth_pct = 0.05` | Projected revenue & profit |
| What if margins compress by 2%? | `margin = 0.10` (from 0.12) | Profit delta |
| What if we enter a new region? | `new_region_sales = X` | Total revenue uplift |
| What if COGS rises 8%? | `cogs_increase = 0.08` | Break-even point |

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run scenario analysis from the pipeline
python pipeline/fetch_data.py
```

The `scenario_revenue_impact()` function in `pipeline/fetch_data.py` is the core engine:

```python
from pipeline.fetch_data import scenario_revenue_impact

# TechMart 2025 baseline
result = scenario_revenue_impact(
    base_revenue=5_357_458,  # actual 2025 revenue
    growth_pct=0.05,          # +5% growth assumption
    margin=0.1245             # current profit margin
)

print(result)
# {
#   'base_revenue':       5357458.0,
#   'growth_pct':         5.0,
#   'projected_revenue':  5625330.9,
#   'projected_profit':    700503.5,
#   'delta_revenue':       267872.9
# }
```

---

## Scenarios Explored

### 📈 Optimistic (+10% Growth)

```python
scenario_revenue_impact(5_357_458, growth_pct=0.10, margin=0.1245)
# Projected Revenue : $5,893,204
# Projected Profit  : $  734,204
# Delta             : $  535,746
```

### 📉 Pessimistic (-5% Decline)

```python
scenario_revenue_impact(5_357_458, growth_pct=-0.05, margin=0.1245)
# Projected Revenue : $5,089,585
# Projected Profit  : $  634,154
# Delta             : $ -267,873
```

### 📊 Margin Compression (margin drops to 10%)

```python
scenario_revenue_impact(5_357_458, growth_pct=0.05, margin=0.10)
# Projected Revenue : $5,625,331
# Projected Profit  : $  562,533  (vs $700,504 at 12.45%)
# Profit Impact     : -$137,971
```

---

## Extension Ideas

- **Streamlit UI** — sliders for `growth_pct` and `margin`, live chart updates
- **Monte Carlo simulation** — run 10,000 scenarios with randomised inputs
- **Regional breakdown** — apply different growth rates per region (West, East, Central, South)
- **Sensitivity table** — grid of growth_pct × margin showing profit outcomes
