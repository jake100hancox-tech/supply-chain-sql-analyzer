import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Supply Chain SQL Analyzer", layout="wide")
st.title("Supply Chain & Fulfillment Bottleneck Analyzer")
st.write("Interactive SQL + Python Logistics & SLA Performance Dashboard")

# 1. Generate realistic supply chain tables (5,000 orders + carrier lookup table)
np.random.seed(42)
n_orders = 5000

orders_df = pd.DataFrame({
    "order_id": range(1, n_orders + 1),
    "warehouse": np.random.choice(["LA_Hub", "Memphis_MEM1", "Dallas_DC", "Newark_FC"], n_orders),
    "carrier_id": np.random.choice([1, 2, 3], n_orders, p=[0.45, 0.35, 0.20]),
    "shipping_mode": np.random.choice(["Same Day", "First Class", "Standard"], n_orders, p=[0.15, 0.35, 0.50]),
    "scheduled_days": np.random.choice([1, 3, 5], n_orders, p=[0.15, 0.35, 0.50]),
    "actual_days": np.random.choice([1, 2, 3, 4, 5, 7], n_orders, p=[0.12, 0.28, 0.20, 0.22, 0.12, 0.06])
})

carriers_df = pd.DataFrame({
    "carrier_id":,
    "carrier_name": ["Apex Freight", "Pacific Express", "Continental Air"],
    "cost_per_shipment": [12.50, 18.00, 24.75]
})

# 2. Load both tables into an in-memory SQLite database
conn = sqlite3.connect(":memory:")
orders_df.to_sql("orders", conn, index=False, if_exists="replace")
carriers_df.to_sql("carriers", conn, index=False, if_exists="replace")

# 3. Interactive Sidebar Filter
selected_hub = st.sidebar.selectbox(
    "Filter by Distribution Center",
    ["All Warehouses", "LA_Hub", "Memphis_MEM1", "Dallas_DC", "Newark_FC"]
)

where_clause = "" if selected_hub == "All Warehouses" else f"WHERE o.warehouse = '{selected_hub}'"

# 4. SQL Query using JOIN, CASE WHEN, and Aggregations
query = f"""
SELECT 
    o.warehouse AS Warehouse,
    c.carrier_name AS Carrier,
    o.shipping_mode AS Shipping_Mode,
    COUNT(o.order_id) AS Total_Orders,
    ROUND(AVG(o.actual_days - o.scheduled_days), 2) AS Avg_Variance_Days,
    ROUND(100.0 * SUM(CASE WHEN o.actual_days > o.scheduled_days THEN 1 ELSE 0 END) / COUNT(*), 1) AS Late_Order_Pct,
    ROUND(SUM(c.cost_per_shipment), 2) AS Total_Freight_Cost
FROM orders o
JOIN carriers c ON o.carrier_id = c.carrier_id
{where_clause}
GROUP BY o.warehouse, c.carrier_name, o.shipping_mode
ORDER BY Late_Order_Pct DESC;
"""

sql_results = pd.read_sql_query(query, conn)

# 5. Display Top KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders Analyzed", f"{sql_results['Total_Orders'].sum():,}")
col2.metric("Average Late Delivery Rate", f"{sql_results['Late_Order_Pct'].mean():.1f}%")
col3.metric("Total Freight Spend", f"${sql_results['Total_Freight_Cost'].sum():,.2f}")

# 6. Display SQL Table Output
st.subheader("1. SQL Query Output: Carrier & Hub SLA Breakdown")
st.dataframe(sql_results, use_container_width=True)

# 7. Matplotlib Visualization
st.subheader("2. Late Delivery Percentage by Warehouse")
hub_summary = pd.read_sql_query("""
    SELECT 
        warehouse, 
        ROUND(100.0 * SUM(CASE WHEN actual_days > scheduled_days THEN 1 ELSE 0 END) / COUNT(*), 1) AS late_pct
    FROM orders
    GROUP BY warehouse
    ORDER BY late_pct DESC;
""", conn)

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(hub_summary["warehouse"], hub_summary["late_pct"], color="#2b5c8f")
ax.set_ylabel("Late Orders (%)")
ax.set_title("SLA Miss Rate Across Distribution Centers")
ax.set_ylim(0, max(hub_summary["late_pct"]) + 10)
st.pyplot(fig)

# 8. Show the underlying SQL query so recruiters can inspect your SQL skills
with st.expander("View Underlying SQL Query"):
    st.code(query, language="sql")
