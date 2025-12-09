Fortnite Patch Notes AI System

MIS 372T – Final Project
_________________________________________________________________________________________________________________________________

Project Overview

This project builds an AI-powered system that transforms raw Fortnite Battle Royale patch notes into creator-ready content using Retrieval-Augmented Generation (RAG) and Supervised Fine-Tuning (SFT).

__________________________________________________________________________________________________________________________________
System Techniques

Technique 1: Retrieval-Augmented Generation (RAG)

Used to ensure factual accuracy when summarizing Fortnite patch notes by grounding the model in real data from Fortnite Fandom.

Components:

Fetcher Agent – Scrapes official Fortnite Battle Royale patch notes from Fortnite Fandom (including expandable sections like Loot Pool).

Embedding Pipeline – Chunks and embeds patch notes into a FAISS vector store.

Summarizer Agent – Uses Azure OpenAI + retrieved context to produce strict, non-hallucinated summaries.

Technique 2: Supervised Fine-Tuning (SFT)

Used to generate creator-style scripts in the voice and tone of popular Fortnite YouTubers / TikTok creators.

What SFT Does:

Trains a model on curated short-form video scripts

Outputs engaging, high-energy narration scripts

Includes a pipeline that generates AI videos reading the script using the fine-tuned tone

NOTE:
SFT is trained and run in Google Colab to leverage GPU resources. The VS Code project interfaces with its outputs but does not train the model locally. 
The Video generator also limits language involving weapons, so parts of our script were cut off/not talked about
__________________________________________________________________________________________________________________________________
High Level System Architecture 

fortnite-patchnotes-agents/
│
├── agents/
│   ├── agent_fetcher.py        # Scrapes Fortnite Fandom pages (real HTML)
│   ├── agent_summarizer.py     # Strict summary generator (no inference)
│
├── rag/
│   ├── chunk.py                # Text cleaning + chunking
│   ├── embedding.py            # FAISS embedding builder
│   └── retriever.py            # Similarity search
│
├── utils/
│   ├── azure_client.py         # Azure OpenAI chat helper
│   └── text_cleaning.py        # Shared cleaning logic
│
├── data/
│   ├── raw_patch_notes/        # Raw scraped patch notes (JSON)
│   ├── embeddings/             # FAISS index files
│   └── summarized_patch_notes/ # Saved summaries (JSON / TXT)
│
├── sft/
│   └── MIS372_AI_FinalProject_SFT_Script.ipynb  # Colab notebook (SFT + AI video)
│
├── requirements.txt
├── .env.example
└── README.md

__________________________________________________________________________________________________________________________________
Getting Started (VS Code Setup)

1️. Clone the Repository
git clone <your-repo-url>
cd Fortnite_Patch_Agents

2️. Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux

3️. Install Dependencies
pip install -r requirements.txt


If needed manually:

pip install requests beautifulsoup4 lxml python-dotenv langchain langchain-community langchain-openai faiss-cpu openai

__________________________________________________________________________________________________________________________________
Environment Variables (.env)

Create a .env file in the project root:

# Azure OpenAI (Summarizer + Embeddings)
AZURE_OPENAI_BASE=your_azure_base_url
AZURE_OPENAI_API_KEY=your_key
AZURE_CHAT_MODEL=gpt-4.1-nano
AZURE_EMBED_DEPLOYMENT=text-embedding-3-small
AZURE_EMBED_VERSION=2023-05-15

# (Optional) OpenRouter (earlier experiments)
OPENROUTER_API_KEY=your_key
__________________________________________________________________________________________________________________________________
How to Run the Project (RAG Pipeline)


Step 1 – Fetch Latest Patch Notes
python -m agents.agent_fetcher


Step 2 – Build Embeddings
python -m rag.embedding


Step 3 – Generate Summary
python -m agents.agent_summarizer

Step 4 - Run Supervised Fine-Tuning (SFT) – Colab Only

__________________________________________________________________________________________________________________________________
Why Colab?

GPU required for training

Faster iteration

Free / low-cost compute

How to Use the SFT Pipeline

Open the provided Google Colab notebook

Upload or connect the curated script dataset

Run training cells (SFT)

Generate:

Creator-style scripts

AI-generated videos reading the scripts

📁 Outputs can be:

Downloaded locally

Or referenced in VS for demos