import streamlit as st

st.title("🚦 Delivery Delay Risk Scorer")

st.markdown("""
This tool provides a **rule-based delivery delay risk score** using
operational heuristics derived from historical data.

> ⚠️ This is an **explainable risk scorer**, not a black-box ML predictor.
""")

# -----------------------------
# User Inputs
# -----------------------------
order_hour = st.slider("Order Hour (0–23)", 0, 23, 18)
day_of_week = st.selectbox(
    "Day of Week",
    options=[
        ("Monday", 0),
        ("Tuesday", 1),
        ("Wednesday", 2),
        ("Thursday", 3),
        ("Friday", 4),
        ("Saturday", 5),
        ("Sunday", 6),
    ],
    format_func=lambda x: x[0],
)
sla_slack = st.number_input(
    "SLA Slack (minutes between order & promised delivery)",
    min_value=0,
    max_value=120,
    value=15,
)

day_idx = day_of_week[1]

# -----------------------------
# Risk Scoring Logic
# -----------------------------
risk_score = 0
reasons = []

# Peak hour
if order_hour in [12, 13, 18, 19, 20, 21]:
    risk_score += 30
    reasons.append("Peak-hour operational load")

# Weekend
if day_idx in [5, 6]:
    risk_score += 15
    reasons.append("Weekend delivery stress")

# SLA tightness
if sla_slack < 15:
    risk_score += 30
    reasons.append("Very tight SLA")
elif sla_slack <= 30:
    risk_score += 15
    reasons.append("Moderately tight SLA")

# Late-prone hours
if order_hour in [18, 19, 20, 21, 22]:
    risk_score += 15
    reasons.append("Historically delay-prone hour")

risk_score = min(risk_score, 100)

# -----------------------------
# Risk Interpretation
# -----------------------------
if risk_score <= 30:
    risk_level = "🟢 Low Risk"
elif risk_score <= 60:
    risk_level = "🟡 Medium Risk"
else:
    risk_level = "🔴 High Risk"

# -----------------------------
# Output
# -----------------------------
st.markdown("## 📊 Risk Assessment")
st.metric("Delay Risk Score", f"{risk_score} / 100")
st.markdown(f"### Risk Level: **{risk_level}**")

if reasons:
    st.markdown("#### Contributing Factors:")
    for r in reasons:
        st.write(f"- {r}")
else:
    st.write("No significant risk factors detected.")

st.info(
    "This score is designed to assist operational decision-making "
    "and should be used alongside human judgment."
)
