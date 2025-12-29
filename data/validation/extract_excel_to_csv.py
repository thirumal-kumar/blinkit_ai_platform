import pandas as pd
from loguru import logger
from pathlib import Path

logger.add("logs/phase1_validation.log", rotation="1 MB")

EXCEL_PATH = "data/raw/Blinkit.xlsx"
OUTPUT_DIR = Path("data/raw")

SHEETS_TO_EXTRACT = {
    "blinkit_orders": "blinkit_orders.csv",
    "blinkit_marketing_performance": "blinkit_marketing_performance.csv",
    "blinkit_customer_feedback": "blinkit_customer_feedback.csv",
}

def extract_sheets():
    for sheet, output_file in SHEETS_TO_EXTRACT.items():
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)
        output_path = OUTPUT_DIR / output_file
        df.to_csv(output_path, index=False)
        logger.info(f"Extracted {sheet} → {output_path} ({len(df)} rows)")

if __name__ == "__main__":
    extract_sheets()
