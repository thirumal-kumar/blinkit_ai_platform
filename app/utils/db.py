from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

DB_CONFIG = {
    "user": "blinkit_user",
    "password": "blinkit_pass",
    "host": "localhost",
    "port": 5432,
    "database": "blinkit_dw"
}

def get_engine() -> Engine:
    url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(url, pool_pre_ping=True)
