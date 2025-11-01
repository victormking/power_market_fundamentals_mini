
-- 03_questions.sql
-- Question-based queries (Q01–Q06) that feed Python + Power BI

USE db;

-- Q01: Record counts by region/scenario
CREATE OR REPLACE VIEW q01_counts AS
SELECT region, scenario, COUNT(*) AS rows
FROM market_daily
GROUP BY 1,2
ORDER BY region, scenario;

-- Q02: Average price & total demand by region over 2023-2025
CREATE OR REPLACE VIEW q02_price_demand AS
SELECT
  region,
  ROUND(AVG(avg_price_usd_mwh), 2)   AS avg_price_usd_mwh,
  ROUND(SUM(total_demand_mwh)/1000000.0, 2) AS total_demand_gwh
FROM market_daily
GROUP BY 1
ORDER BY region;

-- Q05: LMP shares (energy/congestion/losses) by region (monthly)
CREATE OR REPLACE VIEW q05_lmp_shares AS
SELECT
  region, month,
  energy_usd_mwh / NULLIF(price_usd_mwh,0)     AS share_energy,
  congestion_usd_mwh / NULLIF(price_usd_mwh,0) AS share_congestion,
  losses_usd_mwh / NULLIF(price_usd_mwh,0)     AS share_losses
FROM v_lmp_components_monthly;

-- Q06: Renewable share vs curtailment (monthly, by region)
CREATE OR REPLACE VIEW q06_renew_vs_curtail AS
SELECT * FROM v_renew_share_curtailment;
