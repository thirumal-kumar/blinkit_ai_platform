import sys
from pathlib import Path
import os

import streamlit as st
from dotenv import load_dotenv

# ---------------------------------------------------
# Environment & path setup
# ---------------------------------------------------
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from genai.retrieve import FeedbackRetriever
from openai import OpenAI

# ---------------------------------------------------
# OpenRouter Client
# ---------------------------------------------------
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL_NAME = "meta-llama/llama-3.1-8b-instruct"

SYSTEM_PROMPT = """
You are a business analytics assistant for Blinkit.

Answer the user's question ONLY using the customer feedback provided.
Do NOT make assumptions beyond the given feedback.
If the feedback is insufficient, say so clearly.

Your answer must be concise, factual, and business-oriented.
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

    return f"""
{SYSTEM_PROMPT}

Customer Feedback Context:
{context}

Question:
{question}

Answer:
"""


# ---------------------------------------------------
# Streamlit UI
# ---------------------------------------------------
st.set_page_config(page_title="AI Insights Chat", layout="wide")

st.title("🤖 AI Insights Chat")
st.markdown(
    """
Ask natural-language questions about **customer feedback and delivery issues**.
Responses are **strictly grounded** in actual feedback data.
"""
)

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
question = st.text_input(
    "Ask a question (e.g. *Why are customers unhappy with delivery timing?*)"
)

ask_button = st.button("Ask AI")

# ---------------------------------------------------
# Handle query
# ---------------------------------------------------
if ask_button and question.strip():
    with st.spinner("🔍 Retrieving relevant feedback and generating answer..."):
        retriever = FeedbackRetriever()
        retrieved = retriever.retrieve(question, top_k=5)

        prompt = build_prompt(question, retrieved)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=300,
        )

        answer = response.choices[0].message.content

        st.session_state.chat_history.append(
            {"question": question, "answer": answer}
        )

# ---------------------------------------------------
# Display chat history
# ---------------------------------------------------
if st.session_state.chat_history:
    st.markdown("## 💬 Conversation")
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**You:** {chat['question']}")
        st.markdown(f"**AI:** {chat['answer']}")
        st.markdown("---")

st.info(
    "AI responses are generated using Retrieval-Augmented Generation (RAG) "
    "and are limited to available customer feedback."
)
