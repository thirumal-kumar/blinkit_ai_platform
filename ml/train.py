import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score, confusion_matrix
import joblib

DATA_PATH = "ml/delivery_features.csv"
MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(MODEL_DIR, "delay_risk_model.pkl")


def train_model():
    print("🔹 Loading feature dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Rows loaded: {len(df)}")

    X = df[
        [
            "order_hour",
            "order_dayofweek",
            "is_weekend",
            "is_peak_hour",
            "sla_slack_min",
        ]
    ]
    y = df["delay_risk"]

    print("🔹 Train / test split...")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    print("🔹 Training multinomial Logistic Regression...")
    model = LogisticRegression(
        max_iter=2000,
        multi_class="multinomial",
        solver="lbfgs",
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    print("🔹 Evaluating model...")
    y_pred = model.predict(X_test)

    macro_f1 = f1_score(y_test, y_pred, average="macro")
    print(f"\n✅ Macro F1 Score: {macro_f1:.3f}\n")

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("🔹 Saving model...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"\n✅ Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
