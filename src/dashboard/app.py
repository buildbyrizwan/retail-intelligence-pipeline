import sys
from pathlib import Path

# Add project root directory to Python's module search path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from src.utils.db import get_engine

# Page setup
st.set_page_config(
    page_title="Retail Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Intelligence Executive Dashboard")
st.markdown("Real-time transactional analytics powered by PostgreSQL and DBT.")

engine = get_engine()

# Fetch analytics data
@st.cache_data(ttl=60)
def load_data():
    with engine.connect() as conn:
        fct_orders = pd.read_sql(
            text("SELECT * FROM public_analytics.fct_orders ORDER BY order_date;"),
            conn
        )
        dim_customers = pd.read_sql(
            text("SELECT * FROM public_analytics.dim_customers;"),
            conn
        )
    return fct_orders, dim_customers

try:
    fct_orders, dim_customers = load_data()

    # --- KPI METRICS ---
    total_revenue = fct_orders["total_amount"].sum()
    total_orders = len(fct_orders)
    total_customers = len(dim_customers)
    avg_order_value = fct_orders["total_amount"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Active Customers", f"{total_customers:,}")
    col4.metric("Avg Order Value", f"${avg_order_value:.2f}")

    st.divider()

    # --- CHARTS SECTION ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Daily Revenue Trend")
        daily_revenue = (
            fct_orders.groupby("order_date")["total_amount"]
            .sum()
            .reset_index()
        )
        fig_trend = px.line(
            daily_revenue,
            x="order_date",
            y="total_amount",
            labels={"order_date": "Date", "total_amount": "Revenue ($)"},
            template="plotly_white"
        )
        fig_trend.update_traces(line_color="#2563EB", line_width=2.5)
        st.plotly_chart(fig_trend, use_container_width=True)

    with chart_col2:
        st.subheader("Revenue by Category")
        category_revenue = (
            fct_orders.groupby("category")["total_amount"]
            .sum()
            .reset_index()
            .sort_values(by="total_amount", ascending=False)
        )
        fig_cat = px.bar(
            category_revenue,
            x="category",
            y="total_amount",
            color="category",
            labels={"category": "Product Category", "total_amount": "Revenue ($)"},
            template="plotly_white"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # --- CUSTOMER LIFETIME VALUE & DATA TABLE ---
    st.divider()
    sub_col1, sub_col2 = st.columns([1, 1])

    with sub_col1:
        st.subheader("Customer Lifetime Value (LTV) Distribution")
        fig_hist = px.histogram(
            dim_customers,
            x="lifetime_value",
            nbins=20,
            labels={"lifetime_value": "Lifetime Spend ($)"},
            color_discrete_sequence=["#10B981"],
            template="plotly_white"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with sub_col2:
        st.subheader("Top Customers by Lifetime Value")
        top_customers = dim_customers.sort_values(
            by="lifetime_value", ascending=False
        ).head(10)[["customer_id", "total_orders", "lifetime_value", "avg_order_value"]]
        st.dataframe(top_customers, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Error connecting to analytics tables: {e}")
    st.info("Make sure PostgreSQL is running and `dbt run` has completed successfully.")