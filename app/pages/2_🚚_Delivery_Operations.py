import streamlit as st
import plotly.express as px
from utils.queries import get_delivery_operations

st.title("🚚 Delivery Operations Overview")

st.markdown("""
This page provides **operational visibility** into delivery performance:
- ⏱️ Delivery delays
- ✅ On-time vs late orders
- 📊 Delay distribution
""")

df = get_delivery_operations()

# Create late flag
df["is_late"] = df["delay_minutes"] > 0

# KPI Section
total_orders = len(df)
late_orders = df["is_late"].sum()
late_pct = (late_orders / total_orders) * 100 if total_orders else 0
avg_delay = df[df["is_late"]]["delay_minutes"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Late Deliveries (%)", f"{late_pct:.2f}")
col3.metric("Avg Delay (min)", f"{avg_delay:.1f}" if avg_delay else "0")

# Late vs On-time
status_counts = df["is_late"].value_counts().rename(
    {True: "Late", False: "On-Time"}
)

fig1 = px.pie(
    names=status_counts.index,
    values=status_counts.values,
    title="Delivery Status Distribution"
)
st.plotly_chart(fig1, use_container_width=True)

# Delay distribution
late_df = df[df["is_late"]]

fig2 = px.histogram(
    late_df,
    x="delay_minutes",
    nbins=40,
    title="Distribution of Delivery Delays (minutes)",
    labels={"delay_minutes": "Delay (minutes)"}
)
st.plotly_chart(fig2, use_container_width=True)
