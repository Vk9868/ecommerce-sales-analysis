# 🛒 E-Commerce Sales Analytics & Forecasting

An end-to-end data analytics project combining **SQL, Python, statistical analysis, and machine learning** to extract business insights from 2 years of e-commerce data — covering sales performance, customer segmentation, lifetime value, and revenue forecasting.

---

## 📌 Project Overview

| Item | Detail |
|------|--------|
| **Domain** | E-Commerce / Retail Analytics |
| **Tools** | Python, SQL (SQLite), Pandas, Scikit-learn, Matplotlib, Seaborn |
| **Techniques** | EDA, RFM Segmentation, CLV Modeling, Cohort Analysis, ML Forecasting |
| **Dataset** | 3,000 orders · 500 customers · 37 products · 24 months |
| **Total Revenue Analyzed** | ₹3.56 Crore |
| **Charts Produced** | 17 visualizations |

---

## 🎯 Business Questions Answered

**Descriptive Analytics**
1. What is the overall revenue, profit margin, and AOV?
2. Which categories, products, and cities drive the most revenue?
3. What are the seasonal patterns in the business?

**Customer Analytics**
4. Which customers are most valuable? (RFM Segmentation)
5. What is each customer's projected lifetime value? (CLV)
6. How well does the business retain customers over time? (Cohort Analysis)

**Predictive Analytics**
7. Can we forecast next 6 months of revenue using ML?
8. What factors most influence monthly sales?

---

## 📁 Project Structure
ecommerce_v2/

│

├── data/

│   ├── generate_data.py          # Synthetic data generator

│   ├── customers.csv / products.csv / orders.csv / order_items.csv

│   ├── rfm_scores.csv            # RFM output

│   ├── clv_data.csv              # CLV output

│   └── ecommerce.db              # SQLite database

│

├── sql/

│   ├── analysis_queries.sql      # 10 foundational business queries

│   └── advanced_queries.sql      # RFM, CLV, cohort & window functions

│

├── outputs/                      # 17 PNG charts

│   ├── 01_kpi_dashboard.png            08_order_patterns.png

│   ├── 02_monthly_revenue.png          09_rfm_segments.png

│   ├── 03_category_performance.png     10_rfm_scatter.png

│   ├── 04_segment_analysis.png         11_clv_analysis.png

│   ├── 05_city_revenue.png             12_rfm_heatmap.png

│   ├── 06_top_products.png             13_revenue_trend.png

│   ├── 07_payment_methods.png          14_model_comparison.png

│   │                                   15_sales_forecast.png

│   │                                   16_feature_importance.png

│   │                                   17_cohort_retention.png

│

├── reports/

│   ├── comprehensive_insights_report.txt

│   └── sales_forecast_2025.csv

│

├── analysis_part0_eda.py         # KPIs, trends, category/city breakdown

├── analysis_part1_rfm_clv.py     # RFM segmentation + CLV modeling

├── analysis_part2_forecasting.py # ML forecasting + cohort retention

├── run_all.py                    # Runs the entire pipeline in one command

└── README.md

---

## 🔍 Key Findings

### Sales Performance
- **Electronics** is the top category by revenue; **Smartphones** is the #1 product
- **Q4 (Oct–Dec)** drives ~35% of annual revenue — a clear festive seasonality effect
- **Delhi** leads all cities in total revenue contribution

### Customer Segmentation (RFM)
- **Champions** (99 customers, ~20% of base) generate the highest revenue per customer (₹1.59L avg) — disproportionate value from a small group
- **Lost** customers (96 people) represent a major win-back opportunity worth an estimated ₹9.4L in recoverable revenue
- **At Risk + Can't Lose Them** (89 customers) need urgent retention campaigns before churning permanently

### Customer Lifetime Value
- Average 1-year CLV: **₹32,193** | Average 3-year CLV: **₹82,092**
- Top "Champion" customers have CLV **5x above average** — justifies premium retention spend

### Forecasting
- Built and compared **3 ML models** (Linear Regression, Random Forest, Gradient Boosting)
- Best model (Gradient Boosting): **R² = 0.292**, MAE ≈ ₹1.76L
- Forecasted **₹76.9 Lakh** in revenue for the next 6 months
- Transparently documented model limitations rather than over-fitting with leaky features

### Retention
- Cohort analysis shows steep month-1 drop-off — signals a largely one-time-purchase customer base
- Recommends nurture email sequences and loyalty incentives to drive repeat purchases

---

## 🛠️ How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

### Run Everything (Recommended)
```bash
python run_all.py
```

### Or Run Each Part Individually
```bash
python data/generate_data.py           # Step 0: Generate dataset
python analysis_part0_eda.py            # Step 1: EDA & business KPIs
python analysis_part1_rfm_clv.py        # Step 2: RFM + CLV analysis
python analysis_part2_forecasting.py    # Step 3: ML forecasting + cohorts
```

All charts save to `outputs/`, reports save to `reports/`.

---

## 🧠 Technical Highlights

**SQL**
- Multi-table JOINs across customers, orders, products, order_items
- CTEs (`WITH` clauses) for RFM and CLV calculations
- Window functions: `RANK()`, `NTILE()`, `LAG()`, cumulative `SUM() OVER()`
- Cohort retention logic using `JULIANDAY()` date arithmetic

**Python / Statistics**
- RFM quintile scoring (`pd.qcut`) with custom segment labeling logic
- CLV estimation using average order value × purchase frequency
- Cohort retention matrix built with `groupby` + `pivot_table`

**Machine Learning**
- Compared Linear Regression, Random Forest, and Gradient Boosting
- Train/test split respecting time-series order (no shuffling)
- Feature importance analysis to explain model decisions
- Deliberately avoided data leakage (lag features) that would have produced a misleadingly perfect R² — documented this decision

**Visualization**
- 17 custom-styled charts: KPI cards, trend lines, heatmaps, scatter plots, pie charts, and forecast bands with confidence intervals

---

## 💡 Business Recommendations

1. **Launch a win-back campaign** for the 96 "Lost" customers (~₹9.4L recoverable)
2. **Build a VIP loyalty tier** for the 99 "Champions" driving ~45% of revenue
3. **Increase Q4 ad spend** starting September to capture festive demand
4. **Add post-purchase nurture emails** (Day 7 / Day 30) to fix the steep retention drop-off
5. **Re-engage At Risk customers** before they fully churn
6. **Collect richer data** (weekly granularity, marketing spend, promo calendar) to improve forecast accuracy in the next iteration

---

## 📖 What I Learned

- How to translate raw transactional data into segmented, actionable customer insights using the RFM framework
- How to build and honestly evaluate ML forecasting models — including recognizing and avoiding data leakage
- How to communicate technical limitations clearly in a business report rather than overselling model performance
- End-to-end project structuring: data generation → SQL → Python → visualization → written business recommendations

---

## 👤 Author

**Vikas Kumar**
Aspiring Data Analyst | Python · SQL · Machine Learning · Data Visualization
📧 vikasmamta08@gmail.com | 💻 github.com/Vk9868
