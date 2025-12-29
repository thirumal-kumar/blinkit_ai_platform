from dotenv import load_dotenv
load_dotenv()

import sys
from pathlib import Path
import os

print("🔹 Starting LLM prompt construction...")

# ---------------------------------------------------
# Ensure project root is on Python path
# ---------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from genai.retrieve import FeedbackRetriever
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

SYSTEM_PROMPT = """
You are a business analytics assistant for Blinkit.

Answer the user's question ONLY using the customer feedback provided.
Do NOT make assumptions beyond the given feedback.
If the feedback is insufficient, say so clearly.

Your answer should be concise, factual, and business-oriented.
"""


def build_prompt(question, retrieved_items):
    context_blocks = []
    for i, item in enumerate(retrieved_items, start=1):
        block = f"""
Feedback {i}:
Sentiment: {item['sentiment']}
Rating: {item['rating']}
Text: {item['text']}
"""
        context_blocks.append(block)

    context = "\n".join(context_blocks)

    prompt = f"""
{SYSTEM_PROMPT}

Customer Feedback Context:
{context}

Question:
{question}

Answer:
"""
    return prompt


def main():
    print("🔹 Initializing retriever...")
    retriever = FeedbackRetriever()

    question = "Why are customers complaining about delivery delays?"
    print(f"🔹 Question: {question}")

    retrieved = retriever.retrieve(question, top_k=5)
    print(f"🔹 Retrieved {len(retrieved)} feedback items")

    prompt = build_prompt(question, retrieved)

    print("\n📄 GENERATED PROMPT (FOR LLM):\n")
    print(prompt)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("❌ Prompt construction failed")
        raise
