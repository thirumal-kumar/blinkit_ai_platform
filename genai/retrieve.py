import sys
from pathlib import Path
import os
import pickle

# ---------------------------------------------------
# Ensure project root on path
# ---------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTORSTORE_DIR = "genai/vectorstore"
INDEX_PATH = os.path.join(VECTORSTORE_DIR, "feedback.index")
META_PATH = os.path.join(VECTORSTORE_DIR, "feedback_meta.pkl")


class FeedbackRetriever:
    def __init__(self):
        print("🔹 Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("🔹 Loading FAISS index...")
        self.index = faiss.read_index(INDEX_PATH)

        print("🔹 Loading metadata...")
        with open(META_PATH, "rb") as f:
            self.metadata = pickle.load(f)

        assert self.index.ntotal == len(
            self.metadata
        ), "Index and metadata size mismatch"

        print(f"✅ Retriever ready with {self.index.ntotal} records")

    def retrieve(self, query, top_k=5):
        print(f"\n🔎 Query: {query}")

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        )

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            item = self.metadata[idx]
            results.append(
                {
                    "rank": rank + 1,
                    "score": float(scores[0][rank]),
                    "feedback_id": item["feedback_id"],
                    "sentiment": item["sentiment"],
                    "rating": item["rating"],
                    "category": item["feedback_category"],
                    "text": item["feedback_text"],
                }
            )

        return results


if __name__ == "__main__":
    retriever = FeedbackRetriever()

    test_queries = [
        "late delivery complaints",
        "customers unhappy with delivery time",
        "poor service and delays",
        "great experience fast delivery",
    ]

    for q in test_queries:
        results = retriever.retrieve(q, top_k=3)
        for r in results:
            print(
                f"[{r['rank']}] (score={r['score']:.3f}, sentiment={r['sentiment']})"
            )
            print(f"    {r['text']}\n")
