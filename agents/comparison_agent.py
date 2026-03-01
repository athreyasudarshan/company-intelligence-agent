from langchain_groq import ChatGroq
from schemas.company_schema import CompanyReport, ComparisonReport
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def run_comparison_agent(company_reports: List[CompanyReport]) -> ComparisonReport:
    
    print(f"[Comparison Agent] Comparing {len(company_reports)} companies...")

    companies_text = ""
    for report in company_reports:
        companies_text += f"""
        Company: {report.company_name} ({report.ticker})
        - Stock Price: {report.financials.stock_price if report.financials else 'N/A'}
        - Market Cap: {report.financials.market_cap if report.financials else 'N/A'}
        - P/E Ratio: {report.financials.pe_ratio if report.financials else 'N/A'}
        - Revenue: {report.financials.revenue if report.financials else 'N/A'}
        - Sentiment: {report.sentiment.overall if report.sentiment else 'N/A'} (score: {report.sentiment.score if report.sentiment else 'N/A'})
        - Analyst Summary: {report.analyst_summary}
        ---
        """

    prompt = f"""
    You are a senior financial analyst. Compare the following companies and provide a 
    detailed comparative analysis (4-5 sentences) highlighting:
    - Which company has stronger financials
    - Which has better market sentiment
    - Key differences between them
    - Which looks more promising and why

    {companies_text}

    Write a professional comparative analysis.
    """

    response = llm.invoke(prompt)

    return ComparisonReport(
        companies=company_reports,
        comparison_narrative=response.content
    )