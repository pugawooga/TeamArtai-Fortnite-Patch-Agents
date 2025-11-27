# rag/chunk.py
import re

def clean_text(text):
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()

def chunk_text(text, chunk_size=1200, overlap=200):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
