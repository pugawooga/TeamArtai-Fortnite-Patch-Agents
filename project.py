import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load the variables from .env
load_dotenv()

# 2. Initialize the client using the secure variable
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"), # matches the name in your .env file
)

try:
    print("Sending request to Grok 4.1 Fast...")
    
    completion = client.chat.completions.create(
        model="x-ai/grok-4.1-fast",
        messages=[
            {
                "role": "user", 
                "content": "Search X for the latest 'Minecraft' news and summarize what people are saying."
            }
        ],
        extra_body={
            "tools": [
                {
                    "type": "x_search",
                    "enable_image_understanding": True
                }
            ],
            "reasoning": {
                "enabled": True
            }
        }
    )

    print("\nResponse:")
    print(completion.choices[0].message.content)

except Exception as e:
    print(f"An error occurred: {e}")