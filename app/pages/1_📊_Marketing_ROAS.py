import streamlit as st
import plotly.graph_objects as go
from utils.queries import get_daily_roas

st.title("📊 Marketing ROI (ROAS) Dashboard")

st.markdown("""
This page shows **daily marketing effectiveness** by comparing:
- 💰 Revenue generated
- 📢 Ad spend
- 📈 Return on Ad Spend (ROAS)
""")

df = get_daily_roas()

# Date filter
min_date = df["day"].min()
max_date = df["day"].max()

start_date, end_date = st.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[(df["day"] >= start_date) & (df["day"] <= end_date)]

# KPI section
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue (₹)", f"{filtered_df['total_revenue'].sum():,.0f}")
col2.metric("Total Ad Spend (₹)", f"{filtered_df['total_spend'].sum():,.0f}")

avg_roas = filtered_df["roas"].mean()
col3.metric("Average ROAS", f"{avg_roas:.2f}" if avg_roas else "N/A")

# Dual-axis chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=filtered_df["day"],
    y=filtered_df["total_spend"],
    name="Ad Spend",
    yaxis="y2",
    marker_color="red",
    opacity=0.6
))

fig.add_trace(go.Scatter(
    x=filtered_df["day"],
    y=filtered_df["total_revenue"],
    name="Revenue",
    mode="lines",
    line=dict(color="green", width=3)
))

fig.update_layout(
    title="Daily Revenue vs Ad Spend",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Revenue (₹)"),
    yaxis2=dict(
        title="Ad Spend (₹)",
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig, use_container_width=True)

# Business alert
if avg_roas and avg_roas < 2.0:
    st.error("⚠️ ROAS below 2.0 — Marketing campaign may be unprofitable.")
else:
    st.success("✅ ROAS is healthy.")
