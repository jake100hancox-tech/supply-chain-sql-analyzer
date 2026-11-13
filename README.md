# Supply Chain & Fulfillment Bottleneck Analyzer

An interactive SQL and Python analytics dashboard designed to evaluate multi-warehouse order fulfillment, carrier SLA performance, and freight spend across 5,000+ simulated logistics records.

🔗 **[Launch Live Interactive Dashboard](https://streamlit.app)**

### Key Features
* **Multi-Table SQL Querying (`SQLite`):** Joins `orders` and `carriers` tables using `JOIN`, `CASE WHEN`, `GROUP BY`, and aggregate functions to calculate late-delivery rates, average fulfillment variance, and carrier freight costs.
* **Dynamic Warehouse Filtering:** Allows real-time filtering across distribution hubs (`LA_Hub`, `Memphis_MEM1`, `Dallas_DC`, `Newark_FC`) with live KPI updates.
* **Visual SLA Diagnostics (`Matplotlib` & `Pandas`):** Generates automated bar charts comparing SLA miss rates across distribution centers, plus an expandable SQL inspector for reviewing underlying queries.

### Tech Stack
* **Languages:** Python, SQL (SQLite)
* **Libraries:** Pandas, NumPy, Matplotlib, Streamlit
