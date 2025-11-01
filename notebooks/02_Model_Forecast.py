
# 02_Model_Forecast.py
# Time-aware train/test, OLS + XGBoost for price modeling, and ARIMA for demand (optional).
# Usage:
#   pip install pandas numpy scikit-learn statsmodels xgboost
#   python notebooks/02_Model_Forecast.py

import os
import pandas as pd
import numpy as np

from sklearn.model_selection import TimeSeriesSplit
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

# Paths (adjust if needed)
BASE = os.path.dirname(os.path.dirname(__file__))
VIEW_CSV = os.path.join(BASE, "outputs", "v_price_drivers_daily.csv")  # Export this from DuckDB first!

df = pd.read_csv(VIEW_CSV, parse_dates=['date'])

# Keep only needed columns
keep = [
    'date','region','avg_price_usd_mwh','total_demand_mwh',
    'energy_cost_usd_mwh','congestion_cost_usd_mwh','losses_cost_usd_mwh',
    'renewable_share_pct','curtailment_mwh','hdd','cdd','dart_spread_usd_mwh',
    'natgas_monthly','scenario'
]
df = df[keep].dropna()

# Train/test split by time (2023-2024 train, 2025 test)
train = df[df['date'] < '2025-01-01'].copy()
test  = df[df['date'] >= '2025-01-01'].copy()

target = 'avg_price_usd_mwh'
num_feats = ['total_demand_mwh','energy_cost_usd_mwh','congestion_cost_usd_mwh','losses_cost_usd_mwh',
             'renewable_share_pct','curtailment_mwh','hdd','cdd','dart_spread_usd_mwh','natgas_monthly']
cat_feats = ['region','scenario']

X_train = train[num_feats + cat_feats]
y_train = train[target]
X_test  = test[num_feats + cat_feats]
y_test  = test[target]

pre = ColumnTransformer([
    ("num", StandardScaler(with_mean=False), num_feats),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_feats),
])

# 1) OLS (via LinearRegression) for interpretable coefficients (after one-hot/scale)
ols = Pipeline([("pre", pre), ("model", LinearRegression(n_jobs=None))])

# 2) XGBoost for non-linear interactions
xgb = Pipeline([("pre", pre), ("model", XGBRegressor(
    n_estimators=400, max_depth=6, learning_rate=0.06, subsample=0.9, colsample_bytree=0.9, random_state=42
))])

results = []

for name, model in [("OLS", ols), ("XGB", xgb)]:
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, pred)
    mape = mean_absolute_percentage_error(y_test, pred)
    r2 = r2_score(y_test, pred)
    results.append({"model": name, "MAE": round(mae,2), "MAPE": round(mape,3), "R2": round(r2,3)})

metrics = pd.DataFrame(results)
OUT_METRICS = os.path.join(BASE, "outputs", "q07_model_metrics.csv")
metrics.to_csv(OUT_METRICS, index=False)

# Save sample predictions for Power BI
pred_out = pd.DataFrame({
    "date": test["date"],
    "region": test["region"],
    "y_true": y_test.values,
    "y_pred": pred
})
pred_out_path = os.path.join(BASE, "outputs", "q08_price_forecast_sample.csv")
pred_out.to_csv(pred_out_path, index=False)

print("Saved:", OUT_METRICS, "and", pred_out_path)
