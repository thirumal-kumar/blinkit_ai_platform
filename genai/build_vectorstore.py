import sys
from pathlib import Path
import os

print("🔹 Starting vector store builder...")

# ---------------------------------------------------
# Ensure project root on path
# ---------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from app.utils.db import get_engine

VECTORSTORE_DIR = "genai/vectorstore"
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "feedback.index")
META_PATH = os.path.join(VECTORSTORE_DIR, "feedback_meta.pkl")


def build_vectorstore():
    print("🔹 Connecting to PostgreSQL...")

    query = text("""
        SELECT
            feedback_id,
            feedback_text,
            sentiment,
            rating,
            feedback_category
        FROM raw_feedback
        WHERE feedback_text IS NOT NULL
    """)

    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    print(f"🔹 Rows fetched from DB: {len(df)}")

    if df.empty:
        raise RuntimeError("No feedback rows found. Cannot build vector store.")

    texts = df["feedback_text"].tolist()

    print("🔹 Loading embedding model (sentence-transformers)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔹 Generating embeddings...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    print(f"🔹 Embeddings shape: {embeddings.shape}")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    print(f"🔹 FAISS index size: {index.ntotal}")

    print("🔹 Saving vector store to disk...")
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    metadata = df[
        ["feedback_id", "sentiment", "rating", "feedback_category", "feedback_text"]
    ].to_dict(orient="records")

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("✅ Vector store built successfully.")
    print(f"📁 Index: {INDEX_PATH}")
    print(f"📁 Metadata: {META_PATH}")


if __name__ == "__main__":
    try:
        build_vectorstore()
    except Exception as e:
        print("❌ Vector store build failed.")
        raise
