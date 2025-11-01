# ⚡ Power Market Fundamentals  
*A mini-project in energy forecasting, capacity expansion, and market fundamentals
---

### 🔍 Executive Summary

This project simulates the workflow of a **Power Market Fundamentals Analyst**, connecting market data, fuel prices, and renewable generation to understand how regional energy systems evolve under policy and demand scenarios.  

It demonstrates **SQL data engineering**, **Python modeling**, and **Tableau visualization** to support insights for long-term capacity planning.

**Tools:** DuckDB · SQL · Python (pandas, matplotlib) · Tableau  
**Skills:** Energy economics · Forecasting · Scenario modeling · Data storytelling  

---

### 🧭 Motivation

As energy systems decarbonize, analysts must forecast how renewables, storage, and fuel prices interact to shape market fundamentals.  
This project mirrors the workflow behind that analysis — transforming messy regional data into interpretable insights for forecasting and capacity planning.

---

## ⚙️ Project Highlights

- Built a **DuckDB warehouse** with 3 analytical SQL views for price, curtailment, and capacity trends.  
- Modeled 4 market **policy scenarios** (`Carbon_Tax`, `Demand_Growth`, `Renewable_Push`, `Storage_Focus`).  
- Created a **Tableau dashboard** combining price deltas and curtailment vs. renewables correlations.  
- Derived insights linking **fuel price volatility** and **renewable integration** to curtailment dynamics.

---

## 🧩 Dataset Schema Overview

| Table | Description |
|:------|:-------------|
| **market_daily_fundamentals** | Daily generation mix, demand, and LMPs |
| **fuel_prices_monthly** | Natural gas, coal, and oil benchmark prices |
| **capacity_expansion_plan** | Capacity additions by region and technology |
| **v_price_drivers_daily** | Joined view linking market data and fuel prices |
| **v_renew_share_curtailment** | Monthly renewable share vs. curtailment |
| **v_lmp_components_monthly** | Aggregated energy, congestion, and loss components |

**Schema Sketch**
fuel_prices_monthly
│
▼
market_daily_fundamentals ───▶ v_price_drivers_daily
│ │
├──────────────▶ v_lmp_components_monthly
└──────────────▶ v_renew_share_curtailment

yaml
Copy code

---

## 🧱 Stage 1 — Data Engineering (SQL)

| View | Purpose | Output |
|:------|:----------|:--------|
| `v_price_drivers_daily` | Combines daily market & fuel data for regression inputs | `/outputs/v_price_drivers_daily.csv` |
| `v_lmp_components_monthly` | Decomposes LMPs by congestion/loss | `/outputs/v_lmp_components_monthly.csv` |
| `v_renew_share_curtailment` | Aggregates renewable share vs. curtailment | `/outputs/v_renew_share_curtailment.csv` |

✅ **SQL Concepts Used:**  
Joins · CTEs · Window functions · Conditional aggregation · Date truncation · CAST/ROUND  

---

## 🧮 Stage 2 — Analytical Modeling (Python)

| Script | Task |
|:--------|:-----|
| `01_EDA.py` | Summary statistics, correlation matrix, and time series plots |
| `02_scenario_analysis.py` | Calculates deltas by region & scenario |
| `outputs/charts/` | Stores generated trendlines and policy comparisons |

🧰 **Python Libraries:** pandas · numpy · matplotlib · duckdb  

---

## 📊 Stage 3 — Visualization (Tableau)

**File:** `/tableau/energy_scenarios_dashboard.twbx`  
**View Live:** [🔗 Tableau Public Dashboard](https://public.tableau.com/app/profile/victor.king4961/viz/PowerMarketFundamentalsDashboard)

#### Dashboard Components
- **Avg Price Δ vs Baseline ($/MWh)** – Heatmap comparing regional scenario impacts  
- **Renewables & Curtailment Share (%)** – Scatter with per-region regressions  
- **Dynamic KPI Cards** – Summaries of price and curtailment deltas  

---

## 📈 Key Insights

1. **Demand Growth** scenario yields the highest overall price uplift (+$1/MWh).  
2. **Carbon Tax** reduces fossil-fuel-driven regions’ average LMPs by 3–6%.  
3. **Renewable Push** without adequate storage increases curtailment, signaling integration limits.  
4. **Storage Focus** smooths variability, decreasing volatility across high-renewable markets.

📘 See the full Stage 3 Insights Report → [insights/insights.md](insights/insights.md)

---

## 📁 Repository Structure

power_market_fundamentals_mini/
├── data/ # Input CSVs
├── sql/ # Setup + analytical SQL views
├── scripts/ # Python analytics
├── notebooks/ # Optional exploratory notebooks
├── outputs/ # CSVs + generated charts
├── tableau/ # Packaged Tableau workbook
├── HOW_TO_RUN.txt # Quick instructions
└── power_market.duckdb # Local data warehouse

yaml
Copy code

---

## 🧾 Deliverables

| Artifact | Description |
|:----------|:-------------|
| **DuckDB Warehouse** | Reproducible SQL & analytics views |
| **Scenario Outputs** | Policy & demand forecasting scenarios |
| **Tableau Dashboard** | Interactive visualization for executives |
| **README Report** | End-to-end project documentation |

---

## 🔗 Related Projects

| Project | Focus |
|:---------|:-------|
| [Credit Union Growth Analytics](https://github.com/victormking/credit_union_growth) | B2C member segmentation & campaign ROI |
| [ETL Pipeline Project](https://github.com/victormking/etl_pipeline) | Python data cleaning & transformation framework |
| [Splash Sports Betting Analysis](https://github.com/victormking/splash_sports_analysis) | Probabilistic modeling for sports markets |

---

## 👤 Author

**Victor King**  
M.S. Sport Analytics · Syracuse University (2025)  
B.S. Business Administration (Marketing & Analytics) · SUNY Oswego  

🌐 [Portfolio](https://victormking.github.io/portfolio-site)  
💼 [LinkedIn](https://linkedin.com/in/victormking)  
💻 [GitHub](https://github.com/victormking)

---

> 🗨️ *This repository showcases full-stack analytics: ETL, modeling, and visualization — built for real-world energy market fundamentals analysis.*
