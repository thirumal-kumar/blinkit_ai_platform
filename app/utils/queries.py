# app/utils/queries.py

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")


def get_daily_roas():
    """
    Load daily marketing performance for ROAS dashboard.
    """
    df = pd.read_csv(
        DATA_DIR / "blinkit_marketing_performance.csv",
        parse_dates=["date"]
    )

    return df


def get_delivery_operations():
    """
    Load delivery operations data for delivery dashboard.
    """
    df = pd.read_csv(
        DATA_DIR / "blinkit_orders.csv",
        parse_dates=[
            "order_date",
            "promised_delivery_time",
            "actual_delivery_time"
        ]
    )

    return df


def get_delay_features():
    """
    Load ML feature dataset for delay risk scorer.
    """
    df = pd.read_csv("ml/delivery_features.csv")
    return df


def get_feedback_data():
    """
    Load customer feedback for GenAI insights.
    """
    df = pd.read_csv(
        DATA_DIR / "blinkit_customer_feedback.csv",
        parse_dates=["feedback_date"]
    )

    return df
