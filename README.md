# 🇮🇳 YojanaGPT — India's AI-Powered Government Scheme Navigator

> **Discover every government scheme you're eligible for. In your language. Step by step.**

India has **700+ government schemes** — subsidies, scholarships, pensions, loans, insurance, housing. Billions of rupees go unclaimed every year because people don't know what they qualify for. **YojanaGPT fixes that.**

A citizen answers a few simple questions. Behind the scenes, a **multi-agent AI system** matches them against every relevant scheme, explains eligibility in plain language, tells them what documents to gather, and walks them through how to apply.

---

## ✨ Features

- **35+ Real Government Schemes** — PM-KISAN, Ayushman Bharat, MGNREGA, scholarships, MUDRA loans, and more — all with complete eligibility rules, document lists, and application steps
- **Multi-Agent Architecture** — 4 specialized AI agents (Profile Builder, Eligibility Matcher, Document Advisor, Application Guide) orchestrated via LangGraph
- **Smart Matching** — Hybrid approach: rule-based pre-filtering + RAG vector search + LLM reasoning for accurate eligibility assessment
- **Multilingual** — Supports Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, and English
- **100% Free LLM Backend** — Works with Groq (free tier), Ollama (local), or Google Gemini (free tier) — zero API costs
- **PDF Reports** — Generate a professional downloadable report of matched schemes with document checklists
- **Two Input Modes** — Quick form entry or conversational chat with the AI
- **Document Guidance** — For every matched scheme, know exactly which documents you need, where to get them, and common pitfalls
- **Application Walkthroughs** — Step-by-step instructions assuming zero technical knowledge

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│                  Streamlit / React UI             │
│         (Form Input + Chat + Results Display)     │
└───────────────────┬──────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │  LangGraph Orchestrator │
        │  (State Machine + Routing) │
        └───┬──────┬──────┬──────┬┘
            │      │      │      │
     ┌──────▼┐ ┌──▼───┐ ┌▼────┐ ┌▼──────┐
     │Profile│ │Match │ │Docs │ │Apply  │
     │Builder│ │Engine│ │Advisor│ │Guide  │
     └──────┘ └──┬───┘ └─────┘ └───────┘
                 │
         ┌───────▼────────┐
         │  ChromaDB (RAG) │
         │  + Rule Engine   │
         └───────┬────────┘
                 │
     ┌───────────▼───────────┐
     │  Free LLM Backends    │
     │  Groq │ Ollama │ Gemini│
     └───────────────────────┘
```

### Agent Details

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Profile Builder** | Gathers citizen info via adaptive conversation or form | User responses | Structured JSON profile |
| **Eligibility Matcher** | Matches profile against 35+ schemes using hybrid rule+RAG+LLM | Profile + Scheme DB | Ranked matches with confidence scores |
| **Document Advisor** | Maps required documents with procurement guidance | Profile + Matched schemes | Categorized document lists |
| **Application Guide** | Generates step-by-step application instructions | Profile + Scheme details | Detailed walkthrough |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/yojanagpt.git
cd yojanagpt
pip install -r requirements.txt
```

### 2. Configure (60 seconds)

```bash
cp .env.example .env
# Edit .env and add your FREE API key (pick one):
# - GROQ_API_KEY from https://console.groq.com (recommended)
# - GEMINI_API_KEY from https://aistudio.google.com/apikey
# - Or just install Ollama for local inference
```

### 3. Run

```bash
# Launch the web UI
streamlit run streamlit_app.py

# Or run CLI demo (no API key needed)
python run.py --demo

# Run system tests
python run.py --test
```

---

## 🧪 Demo Without API Key

The rule-based matching engine works without any API key:

```bash
python run.py --demo
```

This runs 3 sample citizen profiles (farmer, student, widow) through the matching engine and shows all eligible schemes.

---

## Public Deployment

If you want other people to use YojanaGPT, sharing the GitHub repo is not enough. You need to deploy the Streamlit app and add one API key at the app level.

### Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Create a new app from this repo
4. Set the main file path to `streamlit_app.py`
5. In app settings, add one of these secrets:

```toml
GROQ_API_KEY = "your_groq_api_key"
# or
GEMINI_API_KEY = "your_gemini_api_key"
```

You can copy the format from [.streamlit/secrets.toml.example](./.streamlit/secrets.toml.example).

### What works without a deployed API key

- Form-based scheme matching still works in rule-based mode
- Chat mode is disabled
- Detailed AI-written guides are disabled

That means visitors can still get useful results, but for the best public demo you should deploy with `GROQ_API_KEY` or `GEMINI_API_KEY`.

---

## 📊 Scheme Coverage

| Category | Schemes | Examples |
|----------|---------|----------|
| Agriculture | 3 | PM-KISAN, Fasal Bima, Kisan Credit Card |
| Education | 5 | Pre/Post Matric Scholarships (SC, OBC, Minority), PM Vidyalaxmi |
| Women & Child | 4 | Matru Vandana, Sukanya Samriddhi, Ujjwala, Free Silai Machine |
| Health | 3 | Ayushman Bharat, PMSBY, PMJJBY |
| Housing | 2 | PMAY-Gramin, PMAY-Urban |
| Employment | 5 | MGNREGA, PMKVY, MUDRA, Stand Up India, PM SVANidhi |
| Pension | 4 | Atal Pension, PM-SYM, Old Age Pension, Vaya Vandana |
| Other | 9+ | DigiLocker, NAPS, PM-DAKSH, Saubhagya, Van Dhan, etc. |

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Orchestration** | LangGraph | State machine for multi-agent workflow |
| **Vector Store** | ChromaDB | Lightweight, embedded, no server needed |
| **LLM** | Groq / Ollama / Gemini | All free-tier — zero cost forever |
| **UI** | Streamlit (MVP) → React (production) | Fast iteration → polished product |
| **PDF** | FPDF2 | Lightweight PDF generation |
| **Data** | Custom Python DB | 35+ schemes with full structured data |

---

## 📁 Project Structure

```
yojanagpt/
├── agents/
│   ├── agents.py          # All 4 agent implementations
│   └── orchestrator.py    # LangGraph multi-agent orchestrator
├── config/
│   └── settings.py        # All configuration, prompts, constants
├── data/
│   └── schemes_database.py # 35+ government schemes with full details
├── knowledge_base/
│   └── vector_store.py    # ChromaDB vector store with smart chunking
├── ui/
│   └── streamlit_app.py   # Production Streamlit interface
├── utils/
│   ├── llm_client.py      # Unified multi-provider LLM client
│   └── pdf_generator.py   # PDF report generator
├── run.py                 # CLI runner (demo, test, launch)
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🤝 Contributing

This is an open-source project aimed at helping every Indian citizen access their rights. Contributions welcome:

- **Add more schemes** — State-specific schemes are especially needed
- **Improve Hindi/regional language prompts**
- **Build the React frontend**
- **Add WhatsApp bot integration**
- **Improve scraper for live scheme updates from myScheme.gov.in**

---

## ⚠️ Disclaimer

YojanaGPT is for **informational purposes only**. Eligibility assessments are AI-generated and may not be 100% accurate. Always verify at official government portals before applying. Scheme details are subject to change by the government. This project is not affiliated with any government body.

---

## 📜 License

MIT License — use it, fork it, build on it. Just help people.

---

*Built with ❤️ for 1.4 billion Indians who deserve to know their rights.*
