# ARIA — Agentic Research & Intelligence Analyst

> AI-powered company intelligence, delivered by autonomous agents.

ARIA is a multi-agent company intelligence system built with LangGraph, Groq, and LLaMA 3. Enter up to 3 companies and ARIA deploys a pipeline of autonomous AI agents to research financials, analyze news sentiment, and deliver a side-by-side comparative intelligence report — in seconds.

---

## How It Works

ARIA orchestrates 5 specialized agents in a LangGraph pipeline:

1. **Financials Agent** — fetches real-time stock price, market cap, P/E ratio, revenue, and 52-week range via yfinance
2. **News Agent** — retrieves recent news articles using DuckDuckGo Search
3. **Sentiment Agent** — - Finance-grade sentiment analysis using FinBERT — a NLP model trained specifically on financial news
4. **Report Agent** — synthesizes all data into a professional analyst summary using LLaMA 3 via Groq
5. **Comparison Agent** — generates a side-by-side comparative analysis across all companies

---

## Features

- Multi-agent orchestration with LangGraph state management
- Parallel company processing — analyze up to 3 companies simultaneously
- Real-time financial data via yfinance
- NLP sentiment analysis using HuggingFace DistilBERT
- AI-generated analyst summaries and comparative reports via LLaMA 3
- Clickable news headlines linking to original sources
- Interactive charts — stock price comparison and sentiment breakdown
- Persistent agent memory with ChromaDB — tracks previous analyses and shows price movement and sentiment shifts since last search
- Bloomberg Terminal-inspired dark UI built with Streamlit

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM | LLaMA 3 via Groq  |
| Financial Data | yfinance |
| News Search | DuckDuckGo Search |
| Sentiment Analysis | FinBERT (ProsusAI) — Finance-specific NLP model |
| Frontend | Streamlit + Plotly |
| Data Validation | Pydantic |
| Memory & Storage | ChromaDB — Persistent vector store for agent memory |


---

## Installation
```bash
git clone https://github.com/athreyasudarshan/company-intelligence-agent
cd company-intelligence-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add your Groq API key to `.env`:
```
GROQ_API_KEY=your_key_here
```

Run the app:
```bash
streamlit run ui/app.py
```

---

## Project Structure
```
company-intelligence-agent/
├── agents/
│   ├── news_agent.py
│   ├── financials_agent.py
│   ├── sentiment_agent.py
│   ├── report_agent.py
│   └── comparison_agent.py
├── graph/
│   └── pipeline.py
├── tools/
│   ├── search_tool.py
│   └── finance_tool.py
├── schemas/
│   └── company_schema.py
├── ui/
│   └── app.py
└── README.md
```

---

Built by Athreya Sudarshan Srikanth