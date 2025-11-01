
-- 02_views.sql
-- Derive analytical views

USE db;

-- Price drivers joined with monthly fuel (natgas) price
CREATE OR REPLACE VIEW v_price_drivers_daily AS
WITH m AS (
  SELECT
    date, region, scenario,
    avg_price_usd_mwh, total_demand_mwh,
    energy_cost_usd_mwh, congestion_cost_usd_mwh, losses_cost_usd_mwh,
    renewable_share_pct, curtailment_mwh,
    hdd, cdd, dart_spread_usd_mwh
  FROM market_daily
),
f AS (
  SELECT month, region, natgas_usd_mmbtu
  FROM fuel_prices_monthly
)
SELECT
  m.*,
  f.natgas_usd_mmbtu AS natgas_monthly
FROM m
JOIN f
  ON date_trunc('month', m.date) = f.month
 AND m.region = f.region;

-- Monthly LMP decomposition (energy vs congestion vs losses)
CREATE OR REPLACE VIEW v_lmp_components_monthly AS
SELECT
  region,
  date_trunc('month', date) AS month,
  AVG(avg_price_usd_mwh)          AS price_usd_mwh,
  AVG(energy_cost_usd_mwh)        AS energy_usd_mwh,
  AVG(congestion_cost_usd_mwh)    AS congestion_usd_mwh,
  AVG(losses_cost_usd_mwh)        AS losses_usd_mwh
FROM market_daily
GROUP BY 1,2;

-- Renewable share vs curtailment by month + scenario
CREATE OR REPLACE VIEW v_renew_share_curtailment AS
SELECT
  region,
  scenario,
  date_trunc('month', date) AS month,
  AVG(renewable_share_pct)  AS avg_renew_share_pct,
  SUM(curtailment_mwh)      AS curtailment_mwh_month
FROM market_daily
GROUP BY 1,2,3;

-- Optional: Export views to CSV (uncomment to run)
-- COPY (SELECT * FROM v_price_drivers_daily)     TO 'outputs/v_price_drivers_daily.csv' WITH (HEADER, DELIMITER ',');
-- COPY (SELECT * FROM v_lmp_components_monthly)  TO 'outputs/v_lmp_components_monthly.csv' WITH (HEADER, DELIMITER ',');
-- COPY (SELECT * FROM v_renew_share_curtailment) TO 'outputs/v_renew_share_curtailment.csv' WITH (HEADER, DELIMITER ',');
