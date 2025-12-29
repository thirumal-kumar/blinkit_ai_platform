import pandas as pd
from loguru import logger

logger.add("logs/phase1_validation.log", rotation="1 MB")

EXCEL_PATH = "data/raw/Blinkit.xlsx"

def inspect_excel(path):
    xls = pd.ExcelFile(path)
    sheets = xls.sheet_names

    logger.info(f"Excel file detected: {path}")
    logger.info(f"Sheets found: {sheets}")

    for sheet in sheets:
        df = pd.read_excel(path, sheet_name=sheet)
        logger.info(f"--- Sheet: {sheet} ---")
        logger.info(f"Rows: {len(df)}")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info(f"Preview:\n{df.head(3)}")

if __name__ == "__main__":
    inspect_excel(EXCEL_PATH)
