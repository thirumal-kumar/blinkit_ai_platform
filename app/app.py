import streamlit as st
from sqlalchemy import text
from utils.db import get_engine

st.set_page_config(
    page_title="Blinkit Decision Platform",
    layout="wide"
)

st.title("🧠 AI-Powered Blinkit Business Decision Platform")

st.markdown("""
**Phase:** Analytics Dashboard  
**Step:** Database Connectivity Test
""")

try:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
    st.success("✅ Database connection successful.")
except Exception as e:
    st.error("❌ Database connection failed.")
    st.exception(e)
