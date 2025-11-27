# rag/embedding.py

import os
import json
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from rag.chunk import clean_text, chunk_text

load_dotenv()

RAW_DIR = "data/raw_patch_notes"
EMBED_DIR = "data/embeddings"


def build_embeddings():
    print("🔧 Loading latest patch note...")

    files = sorted(os.listdir(RAW_DIR))
    if not files:
        raise Exception("❌ No patch files found. Run fetcher first.")

    latest = files[-1]

    with open(os.path.join(RAW_DIR, latest), "r", encoding="utf-8") as f:
        data = json.load(f)

    if "full_text" not in data:
        raise Exception("❌ Patch JSON missing 'full_text' field.")

    text = clean_text(data["full_text"])
    chunks = chunk_text(text)

    print(f"📄 Chunks generated: {len(chunks)}")

    # ---- OpenRouter-compatible embeddings ----
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-large",
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    print("🔢 Generating embeddings...")

    vectordb = FAISS.from_texts(chunks, embeddings)
    vectordb.save_local(EMBED_DIR)

    print("✅ Embeddings stored in data/embeddings/")


if __name__ == "__main__":
    build_embeddings()
