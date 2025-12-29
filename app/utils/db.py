# app/utils/db.py

import os
from sqlalchemy import create_engine


def is_cloud() -> bool:
    """
    Detect Streamlit Community Cloud environment.
    """
    return os.getenv("STREAMLIT_CLOUD", "").lower() == "true"


def get_engine():
    """
    Return SQLAlchemy engine ONLY for local execution.
    Database access is intentionally disabled on Streamlit Cloud.
    """
    if is_cloud():
        raise RuntimeError(
            "PostgreSQL access is disabled on Streamlit Community Cloud"
        )

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL environment variable not set"
        )

    return create_engine(db_url)
