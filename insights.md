# 💡 Power Market Fundamentals — Insights & Recommendations  

### Key Highlights
- ⚡ 5-year synthetic dataset modeled on U.S. ISO regions  
- 🔋 Storage growth drives ~45 % reduction in intraday DART spread volatility  
- 🌬️ Curtailment still region-specific (esp. wind-dominant zones)  
- 🧮 Natural-gas correlation weakening (r ≈ 0.8 → 0.5) signaling decoupling from fuel fundamentals  
- 📊 Interactive Tableau dashboard enables scenario & region cross-analysis  

---

## 1. Project Overview  
This project simulates regional market behavior across multiple renewable-energy scenarios to mirror the analytical work of the **Power Market Fundamentals Analyst** role at Clearway Energy (Denver, CO).  

The objective was to demonstrate:
- Market-trend quantification across renewables, storage, and gas linkage  
- Construction of a fundamentals-based KPI framework  
- Integration of ETL, statistical analysis, and visualization for energy-market decision-support  

---

## 2. Dataset & Methodology  
**Structure:** 5 years × 5 regions × 3 scenarios (≈ 75 records × 5 metrics).  
Data were generated and cleaned using Python (`pandas`, `numpy`) to emulate market fundamentals.  

**Core Metrics**
| Variable | Description | Unit |
|:---|:---|:---|
| `price_delta_vs_baseline` | Price Δ vs baseline scenario | $/MWh |
| `curtailment_share_delta` | Curtailment Δ (renewables curtailed) | % |
| `dart_spread_vs_storage` | Day-Ahead Real-Time spread adjusted for storage penetration | $/MWh |
| `natgas_price_correlation` | Pearson r between regional price & Henry Hub | r |
| `renewables_share` | Renewables as % of total supply | % |

Outputs were validated for numerical consistency and exported to Tableau for visualization.

---

## 3. Exploratory Findings  

### A. Price Δ vs Baseline ($/MWh)  
- High-storage regions show + $3 – $5 /MWh average Δ relative to baseline.  
- Balanced-mix regions exhibit lowest variance → greater price predictability.  

### B. Curtailment Share Δ (%)  
- Peak curtailment > 10 % in wind-heavy regions during shoulder seasons.  
- Gradual decline (~ –2 pp per year) suggests dispatch efficiency gains.  

### C. DART Spread vs Storage Focus ($/MWh)  
- Moderate negative correlation (r ≈ –0.45) → battery penetration flattens intraday price spreads.  
- Markets with > 30 % storage capacity show notable reduction in price volatility.  

### D. Natural Gas Correlation (r)  
- Strong coupling 2019 – 2021 (r ≈ 0.8).  
- By 2024 decouples to r ≈ 0.5 as renewable penetration rises and policy shifts occur.  

---

## 4. Insights & Recommendations  

### 1️⃣ Grid Stability Improvement  
> **Insight:** Storage integration reduces price volatility and curtailment variance.  
> **Recommendation:** Prioritize 4–8 h battery installations in wind-dominant markets to capture peak-off-peak spread compression benefits.  

### 2️⃣ Curtailment Management  
> **Insight:** Curtailment remains localized.  
> **Recommendation:** Deploy region-specific forecasting and dispatch algorithms for Texas & Midwest ISOs to target wind spillage events.  

### 3️⃣ Forecasting Model Integration  
> **Insight:** Curtailment and storage penetration are significant exogenous variables for capacity-expansion and price models.  
> **Recommendation:** Include these factors in long-term elasticity models and short-term price forecasts.  

### 4️⃣ Market Positioning & Hedging  
> **Insight:** Decoupling from gas reduces traditional hedge efficiency.  
> **Recommendation:** Re-evaluate hedge ratios and add renewable penetration indices as cross-hedge instruments.  

---

## 5. Visualization Summary  
All interactive visuals are available in the [🔗 Tableau Dashboard](https://public.tableau.com/app/profile/victor.king4961/vizzes):  
- Dynamic region & scenario slicers  
- Trendline analysis for price Δ and curtailment share  
- Scatter relationships for storage vs spread and gas correlation  

*(When filters change, KPIs update dynamically to reflect regional fundamental shifts.)*

---

## 6. Appendix  
**Repository:** [Power Market Fundamentals Mini](https://github.com/victormking/power_market_fundamentals_mini)  
**ETL Pipeline:** `etl_pipeline.py` (creates clean CSV & summary stats)  
**Visualization Workbook:** `/visuals/PowerMarketFundamentals.twbx`  
**Environment:** Python 3.11  |  Tableau Public 2024  |  GitHub Desktop  

---

> 🧭 This project showcases end-to-end data analysis, market modeling, and visual storytelling for renewable-energy market analytics roles — bridging economic research and data science for power market forecasting.
