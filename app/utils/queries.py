from sqlalchemy import text
import pandas as pd
from utils.db import get_engine

def get_daily_roas():
    query = text("""
        WITH daily_revenue AS (
            SELECT
                DATE(order_date) AS day,
                SUM(order_total) AS total_revenue
            FROM raw_orders
            GROUP BY DATE(order_date)
        ),
        daily_spend AS (
            SELECT
                date AS day,
                SUM(spend) AS total_spend
            FROM raw_marketing
            GROUP BY date
        )
        SELECT
            COALESCE(r.day, s.day) AS day,
            COALESCE(r.total_revenue, 0) AS total_revenue,
            COALESCE(s.total_spend, 0) AS total_spend,
            CASE
                WHEN COALESCE(s.total_spend, 0) = 0 THEN NULL
                ELSE ROUND(r.total_revenue / s.total_spend, 2)
            END AS roas
        FROM daily_revenue r
        FULL OUTER JOIN daily_spend s
        ON r.day = s.day
        ORDER BY day
    """)

    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

def get_delivery_operations():
    query = text("""
        SELECT
            order_id,
            DATE(order_date) AS order_day,
            promised_delivery_time,
            actual_delivery_time,
            delivery_status,
            EXTRACT(EPOCH FROM (actual_delivery_time - promised_delivery_time))/60
                AS delay_minutes
        FROM raw_orders
        WHERE actual_delivery_time IS NOT NULL
          AND promised_delivery_time IS NOT NULL
    """)

    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df
