# rag/retriever.py

import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

EMBED_DIR = "data/embeddings"


def _embedding_client():
    return AzureOpenAIEmbeddings(
        azure_endpoint=os.getenv("AZURE_OPENAI_BASE"),
        azure_deployment=os.getenv("AZURE_EMBED_DEPLOYMENT"),
        api_version=os.getenv("AZURE_EMBED_VERSION"),
        openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    )


def load_faiss():
    if not os.path.exists(EMBED_DIR):
        raise Exception("❌ No FAISS index found. Run rag.embedding first.")
    return FAISS.load_local(EMBED_DIR, _embedding_client(), allow_dangerous_deserialization=True)


def retrieve(query: str, k: int = 5):
    vectordb = load_faiss()
    docs = vectordb.similarity_search(query, k=k)
    # summarizer wants plain strings, labeler can reconstruct Document if needed
    return [d.page_content for d in docs]
