# agents/agent_summarizer.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.azure_client import azure_chat_completion

load_dotenv()

RAW_DIR = "data/raw_patch_notes"
SUM_DIR = "data/summarized_patch_notes"


# ---------------------------------------------------------
# Load newest fetched patch file
# ---------------------------------------------------------
def load_latest_patch():
    files = sorted(os.listdir(RAW_DIR))
    if not files:
        raise Exception("❌ No patch notes found. Run agent_fetcher first.")

    latest = files[-1]
    with open(os.path.join(RAW_DIR, latest), "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------
# Save summarized patch notes
# ---------------------------------------------------------
def save_summary(patch_title, summary_text):
    os.makedirs(SUM_DIR, exist_ok=True)

    safe_title = patch_title.replace(" ", "_").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")

    filename = f"{date_str}_{safe_title}_SUMMARY.txt"
    path = os.path.join(SUM_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"📁 Summary saved to: {path}")
    return path


# ---------------------------------------------------------
# Summarizer (STRICT — NO INFERENCE)
# ---------------------------------------------------------
def summarize_patch():
    patch = load_latest_patch()

    # Works for your new fetcher (OpenRouter version)
    if "full_text" in patch:
        full_text = patch["full_text"]
    # Works for your HTML scraper version
    elif "full_raw_text" in patch:
        full_text = patch["full_raw_text"]
    else:
        raise Exception("❌ Patch JSON missing full_text or full_raw_text")

    patch_title = patch.get("patch_title", "Unknown_Patch")

    prompt = f"""
You are a **STRICT Fortnite Battle Royale patch note summarizer.**

RULES:
- Use ONLY the text in PATCH TEXT.
- DO NOT infer or guess loot pool, weapons, map changes, mechanics, or anything else.
- If a section is missing, write EXACTLY: "No information provided."
- You must NOT add outside knowledge.
- You must NOT fabricate items or weapons.

Produce this format:

**Fortnite Patch Summary**

### 📝 Overview
- (Summarize ONLY what appears.)

### 🗺️ Map Changes
- If none appear → "No information provided."

### 🔫 Weapons / Loot Pool
- List ONLY weapons or loot items explicitly appearing in PATCH TEXT.
- If none appear → "No information provided."

### 🎮 Gameplay Changes
- Only list explicit changes.
- If none appear → "No information provided."

### 👕 Cosmetics & Collabs
- Only list what appears.
- If none appear → "No information provided."

### 📅 Quests & Events
- Only list what appears.

### ⚡ TLDR
- 1–2 sentences, using only actual text.

--- PATCH TEXT ---
{full_text}
"""

    response = azure_chat_completion(
        model=os.getenv("AZURE_CHAT_MODEL"),
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response["choices"][0]["message"]["content"]

    # Save result
    save_summary(patch_title, summary)

    return summary


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------
if __name__ == "__main__":
    print("\n🚀 Running Summarizer Agent...\n")
    output = summarize_patch()
    print("\n--- SUMMARY OUTPUT ---\n")
    print(output)
