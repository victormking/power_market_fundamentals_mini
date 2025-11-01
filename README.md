# ⚡ Power Market Fundamentals  
*A mini energy forecasting and capacity expansion analytics project inspired by Clearway Energy.*

---

### 🧭 Overview
This project simulates a **Power Market Fundamentals Analyst workflow** — analyzing how fuel prices, renewable share, and policy scenarios affect market electricity prices and curtailment across U.S. regional grids (CAISO, ERCOT, NYISO, PJM, SPP).

It demonstrates:
- **SQL data engineering** (creating analytical views)
- **Python modeling** (EDA + scenario adjustments)
- **Visualization** (Tableau dashboard)
- **Market storytelling** (policy & demand implications)

**Stack:** DuckDB · SQL · Python · Pandas · Matplotlib · Tableau  
**Focus:** Energy economics, capacity expansion, and scenario-based forecasting

---

### ⚙️ Quickstart (Run in 60 Seconds)

# Clone repository
git clone https://github.com/victormking/power_market_fundamentals_mini.git
cd power_market_fundamentals_mini

# Load into DuckDB
.open power_market.duckdb
.read sql/01_setup.sql
.read sql/02_views.sql
.read sql/03_questions.sql

# Optional: view outputs
SELECT * FROM v_price_drivers_daily LIMIT 5;
🧩 Mini-Data Schema Overview
Table	Description
market_daily_fundamentals	Daily demand, generation mix, and LMP components
fuel_prices_monthly	Regional fuel prices (gas, coal, oil)
capacity_expansion_plan	Annual capacity additions by technology and region
v_price_drivers_daily	Joined table linking fuel prices with daily LMPs
v_renew_share_curtailment	Aggregated renewable share vs curtailment
v_lmp_components_monthly	LMP energy, congestion, and loss decomposition

🎯 Project Objectives
Quantify how renewable penetration affects curtailment and price stability

Identify fuel price sensitivity and policy impacts across markets

Demonstrate scalable ETL + forecasting workflows

Visualize results for energy fundamentals & planning teams

🧱 Data Engineering (Stage 1 – SQL Views)
View	Purpose	Output
v_price_drivers_daily	Merge daily demand, generation, and fuel prices	/outputs/v_price_drivers_daily.csv
v_lmp_components_monthly	Aggregate energy, congestion, and loss components	/outputs/v_lmp_components_monthly.csv
v_renew_share_curtailment	Compute renewable share vs total curtailment	/outputs/v_renew_share_curtailment.csv

🧮 Analytical Workflow (Stage 2 – Python)
Script	Description
01_EDA.py	Exploratory data analysis, correlation heatmaps, distribution plots
02_scenario_analysis.py	Applies scenarios (Carbon_Tax, Demand_Growth, Renewable_Push, Storage_Focus)
outputs/charts/	Generated figures for curtailment vs renewables and scenario deltas

📊 Visualization (Stage 3 – Tableau)
File: /tableau/energy_scenarios_dashboard.twbx
View Live: Tableau Public – Power Market Fundamentals Dashboard ← (replace this with your actual link)

Dashboard Sections:
Avg Price Δ vs Baseline ($/MWh) — Heatmap by Region × Scenario

Renewables & Curtailment Share (%) — Scatter with per-region linear regressions

KPI Card: Summary of average price shifts across markets

📈 Key Insights
Demand Growth scenario increases average power prices most significantly (up to +$1/MWh).

Carbon Tax dampens prices in coal-heavy regions (ERCOT, PJM).

Renewable Push increases curtailment rate, emphasizing need for Storage Focus to balance grid utilization.

Trendlines (R² > 0.9) show strong positive correlation between renewable share and curtailment volume.

📁 Repository Structure
bash
Copy code
power_market_fundamentals_mini/
├── data/                         # synthetic input data
├── sql/                          # 3-stage SQL scripts
├── scripts/                      # Python EDA & scenario code
├── notebooks/                    # optional Jupyter exploration
├── outputs/                      # CSVs, charts, and QA exports
├── tableau/                      # packaged .twbx dashboard
├── HOW_TO_RUN.txt
└── power_market.duckdb
🧾 Deliverables
Component	Description
DuckDB Warehouse	All queries reproducible in SQL
Scenario Forecasts	4 simulated market futures
Tableau Dashboard	Executive-ready visualization
README Report	Full documentation of pipeline and results
