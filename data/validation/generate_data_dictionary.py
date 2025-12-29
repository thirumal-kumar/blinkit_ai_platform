import pandas as pd
from pathlib import Path

FILES = {
    "Orders": "data/raw/blinkit_orders.csv",
    "Marketing": "data/raw/blinkit_marketing_performance.csv",
    "Feedback": "data/raw/blinkit_customer_feedback.csv",
}

with open("data/validation/data_dictionary.md", "w") as f:
    for name, path in FILES.items():
        df = pd.read_csv(path)
        f.write(f"## {name}\n\n")
        for col in df.columns:
            f.write(f"- **{col}**: {df[col].dtype}\n")
        f.write("\n")
