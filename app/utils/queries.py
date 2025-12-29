import os
import pandas as pd
from sqlalchemy import text
from app.utils.db import get_engine, is_cloud

DATA_PATH = "data/raw"

# -------------------------------
# MARKETING ROAS
# -------------------------------
def get_daily_roas():
    if is_cloud():
        orders = pd.read_csv(f"{DATA_PATH}/blinkit_orders.csv", parse_dates=["order_date"])
        marketing = pd.read_csv(f"{DATA_PATH}/blinkit_marketing_performance.csv", parse_dates=["date"])

        daily_revenue = (
            orders.groupby(orders["order_date"].dt.date)["order_total"]
            .sum()
            .reset_index(name="total_revenue")
        )

        daily_spend = (
            marketing.groupby(marketing["date"].dt.date)["spend"]
            .sum()
            .reset_index(name="total_spend")
        )

        df = pd.merge(daily_revenue, daily_spend, on="date", how="inner")
        df["roas"] = df["total_revenue"] / df["total_spend"]
        return df

    engine = get_engine()
    query = text("""
        WITH daily_revenue AS (
            SELECT DATE(order_date) AS day, SUM(order_total) AS revenue
            FROM raw_orders
            GROUP BY DATE(order_date)
        ),
        daily_spend AS (
            SELECT date AS day, SUM(spend) AS spend
            FROM raw_marketing
            GROUP BY date
        )
        SELECT r.day, r.revenue, s.spend, (r.revenue / s.spend) AS roas
        FROM daily_revenue r
        JOIN daily_spend s ON r.day = s.day
        ORDER BY r.day;
    """)

    with engine.connect() as conn:
        return pd.read_sql(query, conn)


# -------------------------------
# DELIVERY OPERATIONS
# -------------------------------
def get_delivery_operations():
    if is_cloud():
        df = pd.read_csv(f"{DATA_PATH}/blinkit_orders.csv", parse_dates=[
            "order_date", "promised_delivery_time", "actual_delivery_time"
        ])

        df["is_late"] = df["actual_delivery_time"] > df["promised_delivery_time"]
        df["delay_minutes"] = (
            (df["actual_delivery_time"] - df["promised_delivery_time"])
            .dt.total_seconds() / 60
        ).clip(lower=0)

        return df

    engine = get_engine()
    query = text("""
        SELECT
            order_id,
            order_date,
            promised_delivery_time,
            actual_delivery_time,
            CASE
                WHEN actual_delivery_time > promised_delivery_time THEN 1
                ELSE 0
            END AS is_late,
            EXTRACT(EPOCH FROM (actual_delivery_time - promised_delivery_time))/60 AS delay_minutes
        FROM raw_orders;
    """)

    with engine.connect() as conn:
        return pd.read_sql(query, conn)
