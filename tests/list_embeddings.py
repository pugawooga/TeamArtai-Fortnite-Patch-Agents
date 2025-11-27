from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

models = client.models.list()

print("\n🔍 AVAILABLE EMBEDDING MODELS:\n")
for m in models.data:
    name = m.id.lower()
    if "embed" in name or "embedding" in name or "vector" in name:
        print("➡", m.id)
