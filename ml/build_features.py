import sys
from pathlib import Path

# ---------------------------------------------------
# Ensure project root is on Python path
# ---------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
from sqlalchemy import text
from app.utils.db import get_engine

OUTPUT_PATH = "ml/delivery_features.csv"


def build_features():
    print("🔹 Loading data from PostgreSQL...")

    query = text("""
        SELECT
            order_id,
            order_date,
            promised_delivery_time,
            actual_delivery_time
        FROM raw_orders
        WHERE order_date IS NOT NULL
          AND promised_delivery_time IS NOT NULL
          AND actual_delivery_time IS NOT NULL
    """)

    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    print(f"Rows fetched: {len(df)}")

    # ---------------------------------------------------
    # Datetime conversion
    # ---------------------------------------------------
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["promised_delivery_time"] = pd.to_datetime(df["promised_delivery_time"])
    df["actual_delivery_time"] = pd.to_datetime(df["actual_delivery_time"])

    # ---------------------------------------------------
    # Time-based features
    # ---------------------------------------------------
    df["order_hour"] = df["order_date"].dt.hour
    df["order_dayofweek"] = df["order_date"].dt.dayofweek
    df["is_weekend"] = df["order_dayofweek"].isin([5, 6]).astype(int)

    # Peak hour flag (lunch + dinner rush)
    df["is_peak_hour"] = df["order_hour"].isin(
        [12, 13, 18, 19, 20, 21]
    ).astype(int)

    # ---------------------------------------------------
    # SLA slack (minutes between order time and promised delivery)
    # ---------------------------------------------------
    df["sla_slack_min"] = (
        (df["promised_delivery_time"] - df["order_date"])
        .dt.total_seconds() / 60
    ).clip(lower=0)

    # ---------------------------------------------------
    # Actual delay magnitude (minutes)
    # ---------------------------------------------------
    df["delay_minutes"] = (
        (df["actual_delivery_time"] - df["promised_delivery_time"])
        .dt.total_seconds() / 60
    ).clip(lower=0)

    # ---------------------------------------------------
    # Delay risk bucket (TARGET VARIABLE)
    # 0 → On-time
    # 1 → Minor delay (1–10 min)
    # 2 → Moderate delay (10–30 min)
    # 3 → Severe delay (>30 min)
    # ---------------------------------------------------
    def delay_bucket(x):
        if x == 0:
            return 0
        elif x <= 10:
            return 1
        elif x <= 30:
            return 2
        else:
            return 3

    df["delay_risk"] = df["delay_minutes"].apply(delay_bucket)

    # ---------------------------------------------------
    # Final feature set
    # ---------------------------------------------------
    features = df[
        [
            "order_id",
            "order_hour",
            "order_dayofweek",
            "is_weekend",
            "is_peak_hour",
            "sla_slack_min",
            "delay_risk",
        ]
    ]

    features.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Feature dataset saved to {OUTPUT_PATH}")
    print("\nPreview:")
    print(features.head())


if __name__ == "__main__":
    build_features()
