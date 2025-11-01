
-- 01_setup.sql
-- Create DuckDB tables from CSVs (run from project root inside DuckDB CLI)
-- Example:
--   .open power_market.duckdb
--   .read sql/01_setup.sql

ATTACH 'power_market.duckdb' AS db;
USE db;

-- Create or replace base tables
CREATE OR REPLACE TABLE market_daily AS
SELECT * FROM read_csv_auto('data/market_daily_fundamentals.csv');

CREATE OR REPLACE TABLE fuel_prices_monthly AS
SELECT * FROM read_csv_auto('data/fuel_prices_monthly.csv');

CREATE OR REPLACE TABLE capacity_plan AS
SELECT * FROM read_csv_auto('data/capacity_expansion_plan.csv');

-- Index-like helpers (DuckDB will optimize scans automatically, but we keep keys explicit)
-- (No CREATE INDEX in DuckDB yet; we ensure correct types)
ALTER TABLE market_daily ALTER COLUMN date TYPE DATE;
ALTER TABLE fuel_prices_monthly ALTER COLUMN month TYPE DATE;

-- Quick sanity row counts
SELECT 'market_daily' AS table_name, COUNT(*) AS rows FROM market_daily
UNION ALL
SELECT 'fuel_prices_monthly', COUNT(*) FROM fuel_prices_monthly
UNION ALL
SELECT 'capacity_plan', COUNT(*) FROM capacity_plan;
