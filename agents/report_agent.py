from langchain_groq import ChatGroq
from schemas.company_schema import CompanyReport, FinancialData, SentimentData, NewsItem
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def run_report_agent(
    company_name: str,
    ticker: str,
    financials: FinancialData,
    news: List[NewsItem],
    sentiment: SentimentData
) -> CompanyReport:
    
    print(f"[Report Agent] Generating report for {company_name}...")

    news_text = "\n".join([f"- {item.title}: {item.summary}" for item in news[:5]])

    prompt = f"""
    You are a professional financial analyst. Based on the following data, write a concise 
    analyst summary (3-4 sentences) for {company_name}.

    Financial Data:
    - Stock Price: {financials.stock_price}
    - Market Cap: {financials.market_cap}
    - P/E Ratio: {financials.pe_ratio}
    - 52 Week High: {financials.week_52_high}
    - 52 Week Low: {financials.week_52_low}
    - Revenue: {financials.revenue}
    - Sector: {financials.sector}

    Recent News:
    {news_text}

    Sentiment: {sentiment.overall} (score: {sentiment.score})

    Write a professional analyst summary highlighting key insights.
    """

    response = llm.invoke(prompt)

    return CompanyReport(
        company_name=company_name,
        ticker=ticker,
        financials=financials,
        news=news,
        sentiment=sentiment,
        analyst_summary=response.content
    )