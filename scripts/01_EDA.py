# 01_EDA.py
# Quick EDA: correlations and simple aggregations for Q03–Q06.
# Usage:
#   pip install pandas numpy matplotlib seaborn
#   python scripts/01_EDA.py

import os
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(__file__))
VIEW_CSV = os.path.join(BASE, "outputs", "v_price_drivers_daily.csv")

df = pd.read_csv(VIEW_CSV, parse_dates=['date'])

num_cols = [
    'avg_price_usd_mwh','total_demand_mwh','renewable_share_pct','curtailment_mwh',
    'hdd','cdd','dart_spread_usd_mwh','natgas_monthly',
    'energy_cost_usd_mwh','congestion_cost_usd_mwh','losses_cost_usd_mwh'
]

# Compute correlations
corr = df[num_cols].corr()

# Save correlation matrix as CSV
corr.to_csv(os.path.join(BASE, "outputs", "q03_correlations.csv"), index=True)

# Ensure charts folder exists before saving plot
charts_dir = os.path.join(BASE, "outputs", "charts")
os.makedirs(charts_dir, exist_ok=True)

# Create and save heatmap
plt.figure(figsize=(8, 6))
plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
plt.xticks(range(len(num_cols)), num_cols, rotation=90)
plt.yticks(range(len(num_cols)), num_cols)
plt.colorbar(label='Correlation')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, "q03_corr_heatmap.png"), dpi=140)

print("✅ Saved correlations and heatmap successfully.")
