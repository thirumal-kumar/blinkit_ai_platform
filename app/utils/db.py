import os
from sqlalchemy import create_engine

def is_cloud():
    return os.getenv("STREAMLIT_CLOUD", "false").lower() == "true"

def get_engine():
    if is_cloud():
        # Cloud mode → NO DATABASE
        return None

    # Local PostgreSQL connection
    DB_USER = "blinkit_user"
    DB_PASS = "blinkit_pass"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "blinkit_dw"

    conn_str = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return create_engine(conn_str)
