# utils/azure_client.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_INFERENCE_BASE = os.getenv("AZURE_INFERENCE_BASE")  # example: https://aistudio-apim-ai-gateway02.azure-api.net/MIS372T/v1
AZURE_CHAT_VERSION   = os.getenv("AZURE_CHAT_VERSION")
AZURE_CHAT_MODEL     = os.getenv("AZURE_CHAT_MODEL")

AZURE_API_KEY        = os.getenv("AZURE_API_KEY")  # Subscription key


def azure_chat_completion(messages, model=AZURE_CHAT_MODEL):
    """
    Calls Azure chat completion endpoint through MIS372T APIM.
    """

    url = f"{AZURE_INFERENCE_BASE}/chat/completions?api-version={AZURE_CHAT_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": AZURE_API_KEY
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 800,
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)

    # Show nice error in console
    if response.status_code != 200:
        print(f"❌ Azure Error: {response.text}")
        response.raise_for_status()

    return response.json()
