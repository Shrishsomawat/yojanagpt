# 🇮🇳 YojanaGPT

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://yojanagpt-7kuq3dy6fyzwdtdxynsx9g.streamlit.app/)

**India’s AI-powered government scheme navigator.**  
Find the schemes you may be eligible for, understand why, see required documents, and get step-by-step application help.

## Live Demo

Try it here: [https://yojanagpt-7kuq3dy6fyzwdtdxynsx9g.streamlit.app/](https://yojanagpt-7kuq3dy6fyzwdtdxynsx9g.streamlit.app/)

## Why YojanaGPT

India has hundreds of government schemes for farmers, students, women, workers, senior citizens, and low-income families. Many people never benefit from them because eligibility is confusing and information is scattered.

YojanaGPT helps users:
- discover relevant schemes
- understand eligibility in simple language
- see required documents
- get application guidance

## Features

- **35+ government schemes** across agriculture, education, health, housing, pensions, and employment
- **Multi-agent workflow** for profile building, eligibility matching, document guidance, and application help
- **Hybrid matching** using rule-based filtering, RAG search, and LLM reasoning
- **Multilingual support** for English, Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, and Odia
- **PDF report generation** with matched schemes and document checklist
- **Two input modes**: form mode and conversational chat
- **Free-tier friendly** with Groq, Gemini, or Ollama

## How It Works

1. The user enters their background and needs.
2. YojanaGPT builds a structured profile.
3. The matcher checks relevant schemes from the database.
4. The app explains likely eligibility, required documents, and application steps.
5. The user can download a PDF report.

## Architecture

- **Profile Builder Agent**: collects and structures user information
- **Eligibility Matcher Agent**: finds and ranks relevant schemes
- **Document Advisor Agent**: lists likely required documents
- **Application Guide Agent**: provides step-by-step guidance
- **ChromaDB**: powers semantic retrieval for scheme relevance
- **LangGraph**: orchestrates the multi-agent flow
- **Streamlit**: provides the web interface

## Tech Stack

- Python
- Streamlit
- LangGraph
- ChromaDB
- Groq / Gemini / Ollama
- FPDF2

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/Shrishsomawat/yojanagpt.git
cd yojanagpt
pip install -r requirements.txt
