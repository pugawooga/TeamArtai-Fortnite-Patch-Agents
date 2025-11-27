import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise Exception("OPENROUTER_API_KEY not found. Check your .env file.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

# ---------------------------------------------------------
# SYSTEM PROMPT (FANDOM ONLY)
# ---------------------------------------------------------

SYSTEM_PROMPT_FANDOM = """
You are an expert Fortnite Battle Royale analyst.

Your job is to fetch the MOST RECENT **Fortnite Battle Royale patch notes**
from the FANDOM wiki:

    https://fortnite.fandom.com/

STRICT RULES:
- MUST be Battle Royale ONLY (BR)
- MUST NOT include: Save the World, Creative, LEGO, Rocket Racing, Festival
- MUST return the newest season, mini-season, or hotfix
- MUST extract the *entire* patch notes text from the page
- MUST use FANDOM only — no Reddit, no blogs, no leaks, no Epic site

ADDITIONAL REQUIREMENTS:
- EXPAND ALL collapsible sections on the Fandom page (such as Loot Pool, Weapons, Map Changes, Gameplay Adjustments)
- If the page hides content behind a “Click to Expand”, you MUST extract the full hidden text
- For Loot Pools, MUST list all weapons/items exactly as shown in the expanded view
- Do NOT summarize — extract FULL text exactly as seen after expansion
- Include everything under Battle Royale-specific sections, even if collapsed

ADDITIONAL RULES:
- YOU MUST EXPAND ALL COLLAPSIBLE SECTIONS on the Fandom page, including:
    - Current Loot Pool
    - Vaulted/Unvaulted Weapons
    - Map Changes
    - Bug Fixes
    - Detailed Patch Notes Sections
- You must not infer or guess ANYTHING.
- If a section is empty or missing, write: “No information provided in patch notes.”
- You must NOT summarize. Extract the EXACT raw text as shown on the page.
- Do not add external information from outside the Fandom page.
- Do not assume loot pool changes unless explicitly listed.
- Return the full text of the patch notes **after expanding all sections**.

EXPECTED RETURN FORMAT (valid JSON):

{
  "patch_title": "",
  "patch_url": "",
  "full_text": "",
  "source": "fandom"
}
"""


# ---------------------------------------------------------
# FETCH LATEST FANDOM PATCH NOTES
# ---------------------------------------------------------

def fetch_latest_patch_notes_fandom():
    print("🔎 Fetching MOST RECENT Fandom Battle Royale patch notes...\n")

    response = client.chat.completions.create(
        model="x-ai/grok-4-fast",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_FANDOM},
            {
                "role": "user",
                "content": (
                    "Find the newest Fortnite BATTLE ROYALE patch notes on "
                    "https://fortnite.fandom.com/. Extract full text."
                )
            }
        ],
        extra_body={
            "tools": [{"type": "web_search"}],
            "reasoning": {"enabled": True}
        }
    )

    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
        return data
    except json.JSONDecodeError:
        raise Exception("❌ LLM did not return valid JSON. Output:\n\n" + raw)

# ---------------------------------------------------------
# SAVE PATCH NOTES AS JSON
# ---------------------------------------------------------

def save_patch_notes(data):
    title = data["patch_title"]
    safe_title = title.replace(" ", "_").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")

    outdir = "data/raw_patch_notes"
    os.makedirs(outdir, exist_ok=True)

    filepath = f"{outdir}/{date_str}_{safe_title}.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"📁 Saved patch notes to: {filepath}")
    return filepath

# ---------------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------------

def fetch_and_save_latest_patch():
    print("🚀 Starting FANDOM-ONLY patch fetcher...\n")

    data = fetch_latest_patch_notes_fandom()
    filepath = save_patch_notes(data)

    print("\n🎉 PATCH NOTES FETCHED SUCCESSFULLY!")
    print("➡ Title:", data["patch_title"])
    print("➡ URL:", data["patch_url"])
    print("➡ Source:", data["source"])

    return data, filepath


if __name__ == "__main__":
    fetch_and_save_latest_patch()
