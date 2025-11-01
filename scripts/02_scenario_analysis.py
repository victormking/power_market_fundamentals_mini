# scripts/02_q06_q09.py
import os
from pathlib import Path
import duckdb
import pandas as pd

# --- Paths ---
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT_ANS = BASE / "outputs" / "answers"
OUT_ANS.mkdir(parents=True, exist_ok=True)

# Input CSVs
PATH_PRICE_DRIVERS = (BASE / "outputs" / "v_price_drivers_daily.csv").as_posix()
PATH_LMP_MONTHLY   = (BASE / "outputs" / "v_lmp_components_monthly.csv").as_posix()
PATH_RENEW_CURT    = (BASE / "outputs" / "v_renew_share_curtailment.csv").as_posix()

# --- DuckDB ---
con = duckdb.connect()

# Create temp views from CSVs (safe cross-platform)
con.execute(f"CREATE OR REPLACE TEMP VIEW v_price_drivers_daily AS SELECT * FROM read_csv_auto('{PATH_PRICE_DRIVERS}', header=TRUE);")
con.execute(f"CREATE OR REPLACE TEMP VIEW v_lmp_components_monthly AS SELECT * FROM read_csv_auto('{PATH_LMP_MONTHLY}', header=TRUE);")
con.execute(f"CREATE OR REPLACE TEMP VIEW v_renew_share_curtailment AS SELECT * FROM read_csv_auto('{PATH_RENEW_CURT}', header=TRUE);")

def save_df(df: pd.DataFrame, name: str):
    out_path = OUT_ANS / name
    df.to_csv(out_path, index=False)
    print("✔ saved ->", out_path)

# ------------------
# Q6: DART spread stats by region
# ------------------
q6 = con.execute("""
  SELECT region,
         MIN(dart_spread_usd_mwh) AS dart_min,
         AVG(dart_spread_usd_mwh) AS dart_avg,
         MAX(dart_spread_usd_mwh) AS dart_max
  FROM v_price_drivers_daily
  GROUP BY 1
  ORDER BY 1
""").df()
save_df(q6, "q06_dart_spread_stats_by_region.csv")

# ------------------
# Q7: Price deltas vs Baseline
# ------------------
q7 = con.execute("""
WITH monthly AS (
  SELECT region,
         scenario,
         date_trunc('month', date)::DATE AS month,
         AVG(avg_price_usd_mwh) AS price
  FROM v_price_drivers_daily
  GROUP BY 1,2,3
),
base AS (
  SELECT region, month, price AS base_price
  FROM monthly
  WHERE scenario = 'Baseline'
)
SELECT m.region, m.scenario, m.month, m.price, b.base_price,
       m.price - b.base_price AS price_delta_vs_baseline
FROM monthly m
JOIN base b USING (region, month)
WHERE m.scenario <> 'Baseline'
ORDER BY m.region, m.month, m.scenario
""").df()
save_df(q7, "q07_price_delta_vs_baseline.csv")

# ------------------
# Q8: Correlation (natgas vs price) by region & scenario
# ------------------
q8 = con.execute("""
  SELECT region, scenario,
         corr(avg_price_usd_mwh, natgas_monthly) AS r_natgas_price
  FROM v_price_drivers_daily
  GROUP BY 1,2
  ORDER BY 1,2
""").df()
save_df(q8, "q08_corr_natgas_vs_price_by_scenario.csv")

# ------------------
# Q9: Curtailment & renew share deltas vs Baseline
# ------------------
q9 = con.execute("""
WITH monthly AS (
  SELECT region,
         scenario,
         month::DATE AS month,
         AVG(avg_renew_share_pct) AS renew_share_pct,
         AVG(curtailment_mwh_month) AS curtailment_mwh
  FROM v_renew_share_curtailment
  GROUP BY 1,2,3
),
base AS (
  SELECT region, month, renew_share_pct AS base_share, curtailment_mwh AS base_curtail
  FROM monthly WHERE scenario = 'Baseline'
)
SELECT m.region, m.scenario, m.month,
       m.renew_share_pct, m.curtailment_mwh,
       b.base_share, b.base_curtail,
       (m.renew_share_pct - b.base_share) AS renew_share_delta_vs_baseline,
       (m.curtailment_mwh - b.base_curtail) AS curtailment_delta_vs_baseline
FROM monthly m
JOIN base b USING (region, month)
WHERE m.scenario <> 'Baseline'
ORDER BY m.region, m.month, m.scenario
""").df()
save_df(q9, "q09_curtailment_and_share_deltas_vs_baseline.csv")

# scripts/02_q10.py
from pathlib import Path
import duckdb
import pandas as pd

# --- Paths ---
HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT_ANS = BASE / "outputs" / "answers"
OUT_ANS.mkdir(parents=True, exist_ok=True)

# Input CSVs (views exported from DuckDB earlier)
PATH_PRICE_DRIVERS = (BASE / "outputs" / "v_price_drivers_daily.csv").as_posix()

# --- DuckDB ---
con = duckdb.connect()

# Register temp view from CSV
con.execute(
    f"CREATE OR REPLACE TEMP VIEW v_price_drivers_daily AS "
    f"SELECT * FROM read_csv_auto('{PATH_PRICE_DRIVERS}', header=TRUE);"
)

def save_df(df: pd.DataFrame, name: str):
    out_path = OUT_ANS / name
    df.to_csv(out_path, index=False)
    print("✔ saved ->", out_path)

# ----------------------------------------------------------
# Q10: DART spread delta (Storage_Focus vs Baseline), monthly
# ----------------------------------------------------------
# Calculates monthly average DART spread per (region, scenario, month),
# joins Storage_Focus to Baseline by (region, month),
# and computes absolute and percent deltas.
q10 = con.execute("""
WITH monthly AS (
  SELECT
      region,
      scenario,
      date_trunc('month', date)::DATE AS month,
      AVG(dart_spread_usd_mwh)       AS dart_spread_month
  FROM v_price_drivers_daily
  GROUP BY 1,2,3
),
base AS (
  SELECT region, month, dart_spread_month AS base_dart
  FROM monthly
  WHERE scenario = 'Baseline'
),
stor AS (
  SELECT region, month, dart_spread_month AS storage_dart
  FROM monthly
  WHERE scenario = 'Storage_Focus'
)
SELECT
    b.region,
    b.month,
    b.base_dart,
    s.storage_dart,
    (s.storage_dart - b.base_dart)                         AS dart_delta_vs_baseline,
    CASE
      WHEN b.base_dart = 0 THEN NULL
      ELSE (s.storage_dart - b.base_dart) / b.base_dart
    END                                                    AS dart_pct_change_vs_baseline
FROM base b
JOIN stor s
  ON s.region = b.region AND s.month = b.month
ORDER BY b.region, b.month;
""").df()

save_df(q10, "q10_dart_spread_delta_storage_focus.csv")

# ----------------------------------------------------------
# Q11: Capacity additions by region & technology (annual MW)
# ----------------------------------------------------------
# Source: data/capacity_expansion_plan.csv
# Columns expected: region, tech, year, add_capacity_mw
# Output: outputs/answers/q11_capacity_additions_by_tech.csv
# ----------------------------------------------------------

from pathlib import Path
import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT_ANS = BASE / "outputs" / "answers"
OUT_ANS.mkdir(parents=True, exist_ok=True)

PATH_CAP_PLAN = (BASE / "data" / "capacity_expansion_plan.csv").as_posix()

con = duckdb.connect()

# Load file
con.execute(f"""
  CREATE OR REPLACE TEMP VIEW capacity_plan AS
  SELECT * FROM read_csv_auto('{PATH_CAP_PLAN}', header=TRUE);
""")

# Simple aggregation by region, tech, and year
q11 = con.execute("""
SELECT
    region,
    tech AS technology,
    year,
    SUM(add_capacity_mw) AS total_add_mw
FROM capacity_plan
GROUP BY region, tech, year
ORDER BY region, tech, year;
""").df()

out_path = OUT_ANS / "q11_capacity_additions_by_tech.csv"
q11.to_csv(out_path, index=False)
print("✔ saved ->", out_path)

# ----------------------------------------------------------
# Q12: Annual curtailment & renewable share summary
# ----------------------------------------------------------
# Source: outputs/v_renew_share_curtailment.csv
# Columns expected: region, scenario, month, avg_renew_share_pct, curtailment_mwh_month
# Output: outputs/answers/q12_annual_curtailment_and_share.csv
# ----------------------------------------------------------

from pathlib import Path
import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT_ANS = BASE / "outputs" / "answers"
OUT_ANS.mkdir(parents=True, exist_ok=True)

PATH_CURT = (BASE / "outputs" / "v_renew_share_curtailment.csv").as_posix()

con = duckdb.connect()

# Load renewables/curtailment data
con.execute(f"""
  CREATE OR REPLACE TEMP VIEW renew_curt AS
  SELECT * FROM read_csv_auto('{PATH_CURT}', header=TRUE);
""")

# Aggregate to annual totals
q12 = con.execute("""
SELECT
    region,
    scenario,
    EXTRACT(YEAR FROM month) AS year,
    SUM(curtailment_mwh_month) AS total_curtailment_mwh,
    AVG(avg_renew_share_pct)   AS avg_renew_share_pct
FROM renew_curt
GROUP BY region, scenario, year
ORDER BY region, scenario, year;
""").df()

out_path = OUT_ANS / "q12_annual_curtailment_and_share.csv"
q12.to_csv(out_path, index=False)
print("✔ saved ->", out_path)

import os
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# Q13: Summer Peak Stress Screen (Jun–Sep)
# Composite z-score per (region, month) using:
#   - Monthly CDD (load proxy) from daily drivers
#   - Monthly congestion_usd_mwh (from LMP components)
#   - Monthly curtailment_mwh_month (Baseline scenario)
#
# Output: outputs/answers/q13_summer_peak_stress.csv
# ----------------------------------------------------------

# Paths
HERE = os.path.dirname(__file__)
BASE = os.path.abspath(os.path.join(HERE, os.pardir))
out_dir = os.path.join(BASE, "outputs", "answers")
os.makedirs(out_dir, exist_ok=True)

p_drivers = os.path.join(BASE, "outputs", "v_price_drivers_daily.csv")
p_lmp     = os.path.join(BASE, "outputs", "v_lmp_components_monthly.csv")
p_renew   = os.path.join(BASE, "outputs", "v_renew_share_curtailment.csv")
out_csv   = os.path.join(out_dir, "q13_summer_peak_stress.csv")

# Load data
drivers = pd.read_csv(p_drivers, parse_dates=["date"])
lmp     = pd.read_csv(p_lmp, parse_dates=["month"])
renew   = pd.read_csv(p_renew, parse_dates=["month"])

# ---- Build monthly CDD (Jun–Sep) from daily drivers ----
drivers["month"] = drivers["date"].values.astype("datetime64[M]")
drivers_summer = drivers[drivers["date"].dt.month.isin([6, 7, 8, 9])]

# Some synthetic sets might use lowercase or slightly different naming.
# We expect a 'cdd' column from the drivers view—fail fast with a clear error if absent.
if "cdd" not in drivers_summer.columns:
    raise RuntimeError(
        f"'cdd' column not found in {p_drivers}. "
        "Make sure v_price_drivers_daily.csv includes a 'cdd' column."
    )

cdd_monthly = (
    drivers_summer
    .groupby(["region", "month"], as_index=False)["cdd"]
    .mean()
    .rename(columns={"cdd": "cdd_monthly"})
)

# ---- Monthly congestion (Jun–Sep) from LMP components ----
lmp_summer = lmp[lmp["month"].dt.month.isin([6, 7, 8, 9])]

need_cols = {"region", "month", "congestion_usd_mwh"}
missing = need_cols.difference(lmp_summer.columns)
if missing:
    raise RuntimeError(
        f"Missing columns in {p_lmp}: {missing}. "
        "Expected at least ['region','month','congestion_usd_mwh']."
    )

cong_monthly = lmp_summer[["region", "month", "congestion_usd_mwh"]].copy()

# ---- Monthly curtailment (Jun–Sep) — use Baseline scenario to avoid duplication ----
if "scenario" not in renew.columns:
    raise RuntimeError(
        f"'scenario' column not found in {p_renew}. "
        "Expected columns: ['region','scenario','month','avg_renew_share_pct','curtailment_mwh_month']."
    )

renew_base = renew[(renew["scenario"] == "Baseline") & (renew["month"].dt.month.isin([6, 7, 8, 9]))]

need_cols_renew = {"region", "month", "curtailment_mwh_month"}
missing_r = need_cols_renew.difference(renew_base.columns)
if missing_r:
    raise RuntimeError(
        f"Missing columns in {p_renew}: {missing_r}. "
        "Expected 'curtailment_mwh_month' in v_renew_share_curtailment.csv."
    )

curt_monthly = renew_base[["region", "month", "curtailment_mwh_month"]].copy()

# ---- Merge three components on (region, month) ----
df = (
    cdd_monthly
    .merge(cong_monthly, on=["region", "month"], how="inner")
    .merge(curt_monthly, on=["region", "month"], how="inner")
)

if df.empty:
    raise RuntimeError(
        "After merging CDD, congestion, and curtailment (Baseline), "
        "the dataframe is empty. Check that region/month values align across CSVs."
    )

# ---- Compute per-region z-scores and composite stress score ----
def zscore_by_region(s: pd.Series) -> pd.Series:
    # If constant series, std can be 0; return zeros in that case
    std = s.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - s.mean()) / std

df = df.sort_values(["region", "month"]).reset_index(drop=True)

df["z_cdd"] = df.groupby("region", group_keys=False)["cdd_monthly"].apply(zscore_by_region)
df["z_congestion"] = df.groupby("region", group_keys=False)["congestion_usd_mwh"].apply(zscore_by_region)
df["z_curtailment"] = df.groupby("region", group_keys=False)["curtailment_mwh_month"].apply(zscore_by_region)

df["stress_score"] = df["z_cdd"] + df["z_congestion"] + df["z_curtailment"]

# Rank within region (higher stress first)
df["rank_in_region"] = (
    df.groupby("region")["stress_score"]
      .rank(method="dense", ascending=False)
      .astype(int)
)

# Simple flag for presentation: "high stress" if composite ≥ 1.5
df["stress_flag"] = (df["stress_score"] >= 1.5)

# Tidy columns and save
out_cols = [
    "region", "month",
    "cdd_monthly", "congestion_usd_mwh", "curtailment_mwh_month",
    "z_cdd", "z_congestion", "z_curtailment",
    "stress_score", "rank_in_region", "stress_flag"
]
df[out_cols].sort_values(["region", "stress_score"], ascending=[True, False]).to_csv(out_csv, index=False)

print(f"✔ Q13 saved -> {out_csv}")

import os
import pandas as pd
import numpy as np

# ----------------------------------------------------------
# Q14: Driver Attribution by Region (nat gas vs CDD)
# Regress daily avg_price_usd_mwh on natgas_monthly and CDD.
# For each region:
#   - OLS via numpy.linalg.lstsq
#   - Report n_obs, R^2, betas, standardized betas, importance %
# Output -> outputs/answers/q14_driver_attribution_by_region.csv
# ----------------------------------------------------------

HERE = os.path.dirname(__file__)
BASE = os.path.abspath(os.path.join(HERE, os.pardir))
in_csv  = os.path.join(BASE, "outputs", "v_price_drivers_daily.csv")
out_dir = os.path.join(BASE, "outputs", "answers")
os.makedirs(out_dir, exist_ok=True)
out_csv = os.path.join(out_dir, "q14_driver_attribution_by_region.csv")

# Load
df = pd.read_csv(in_csv, parse_dates=["date"])

# Required columns
required = {"region", "date", "avg_price_usd_mwh", "cdd", "natgas_monthly"}
missing = required.difference(df.columns)
if missing:
    raise RuntimeError(
        f"Missing columns in {in_csv}: {missing}. "
        "Expected at least: region, date, avg_price_usd_mwh, cdd, natgas_monthly."
    )

# Keep only needed cols and drop NA
df = df[["region", "date", "avg_price_usd_mwh", "cdd", "natgas_monthly"]].dropna()

rows = []
for region, g in df.groupby("region", sort=True):
    g = g.dropna(subset=["avg_price_usd_mwh", "cdd", "natgas_monthly"]).copy()
    n = len(g)
    if n < 30:  # need enough observations for a stable fit
        continue

    # Design matrix (intercept + X)
    y = g["avg_price_usd_mwh"].values.astype(float)
    X = g[["natgas_monthly", "cdd"]].values.astype(float)
    X_with_const = np.column_stack([np.ones(len(X)), X])

    # OLS
    beta, residuals, rank, s = np.linalg.lstsq(X_with_const, y, rcond=None)
    # beta = [intercept, b_natgas, b_cdd]
    y_hat = X_with_const @ beta
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else np.nan

    # Standardized betas: beta_std_j = beta_j * std(X_j) / std(y)
    y_std = y.std(ddof=0)
    if y_std == 0 or np.isnan(y_std):
        b_natgas_std = 0.0
        b_cdd_std    = 0.0
    else:
        x_natgas_std = g["natgas_monthly"].values.std(ddof=0)
        x_cdd_std    = g["cdd"].values.std(ddof=0)
        b_natgas_std = (beta[1] * (x_natgas_std / y_std)) if x_natgas_std > 0 else 0.0
        b_cdd_std    = (beta[2] * (x_cdd_std / y_std)) if x_cdd_std > 0 else 0.0

    # Importance: absolute standardized betas to % share
    abs_vec = np.array([abs(b_natgas_std), abs(b_cdd_std)], dtype=float)
    ssum = abs_vec.sum()
    if ssum == 0 or np.isnan(ssum):
        imp_natgas = 0.0
        imp_cdd    = 0.0
    else:
        imp_natgas = 100.0 * abs_vec[0] / ssum
        imp_cdd    = 100.0 * abs_vec[1] / ssum

    rows.append({
        "region": region,
        "n_obs": n,
        "r2": r2,
        "beta_intercept": beta[0],
        "beta_natgas": beta[1],
        "beta_cdd": beta[2],
        "beta_natgas_std": b_natgas_std,
        "beta_cdd_std": b_cdd_std,
        "importance_natgas_pct": imp_natgas,
        "importance_cdd_pct": imp_cdd,
    })

# Save
out = pd.DataFrame(rows).sort_values(["region"]).reset_index(drop=True)
out.to_csv(out_csv, index=False)
print(f"✔ Q14 saved -> {out_csv}")

# ----------------------------------------------------------
# Q15: Price & DART volatility (monthly, by region)
# ----------------------------------------------------------
# Uses outputs/v_price_drivers_daily.csv which includes:
# ['date','region','scenario','avg_price_usd_mwh','dart_spread_usd_mwh', ...]
# Computes monthly stddev of avg price and DART spread per region.

import os
import duckdb
import pandas as pd
from pathlib import Path

BASE = os.path.dirname(os.path.dirname(__file__))
out_dir = os.path.join(BASE, "outputs", "answers")
Path(out_dir).mkdir(parents=True, exist_ok=True)

con = duckdb.connect()

daily_csv = os.path.join(BASE, "outputs", "v_price_drivers_daily.csv")
if not os.path.exists(daily_csv):
    raise FileNotFoundError(
        f"Expected file not found: {daily_csv}\n"
        "Make sure you exported v_price_drivers_daily.csv from DuckDB."
    )

# Load daily drivers
con.execute(f"""
    CREATE OR REPLACE TABLE price_daily_raw AS
    SELECT *
    FROM read_csv_auto('{daily_csv}', header=TRUE)
""")

# Sanity: require columns we need
needed_cols = {'date','region','avg_price_usd_mwh','dart_spread_usd_mwh'}
cols = set(pd.read_csv(daily_csv, nrows=1).columns)
missing = needed_cols - cols
if missing:
    raise RuntimeError(f"Q15 missing required columns: {missing}")

# Compute monthly volatility and mean DART for reference
q15 = con.execute("""
    WITH monthly AS (
        SELECT
            region,
            date_trunc('month', try_cast(date AS DATE))::DATE AS month,
            avg_price_usd_mwh,
            dart_spread_usd_mwh
        FROM price_daily_raw
        WHERE date IS NOT NULL
    )
    SELECT
        region,
        month,
        stddev_samp(avg_price_usd_mwh)   AS price_vol_usd,
        stddev_samp(dart_spread_usd_mwh) AS dart_vol_usd,
        avg(dart_spread_usd_mwh)         AS dart_mean_usd
    FROM monthly
    GROUP BY 1,2
    ORDER BY 1,2
""").df()

q15_path = os.path.join(out_dir, "q15_price_and_dart_volatility_monthly.csv")
q15.to_csv(q15_path, index=False)
print(f"✔ Q15 saved -> {q15_path}")
