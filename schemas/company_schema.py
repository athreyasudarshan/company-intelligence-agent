from pydantic import BaseModel
from typing import List, Optional

class FinancialData(BaseModel):
    stock_price: Optional[float] = None
    market_cap: Optional[str] = None
    pe_ratio: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    revenue: Optional[str] = None
    sector: Optional[str] = None

class NewsItem(BaseModel):
    title: str
    summary: Optional[str] = None
    url: Optional[str] = None

class SentimentData(BaseModel):
    overall: str
    score: float
    positive_count: int
    neutral_count: int
    negative_count: int

class CompanyReport(BaseModel):
    company_name: str
    ticker: Optional[str] = None
    financials: Optional[FinancialData] = None
    news: Optional[List[NewsItem]] = None
    sentiment: Optional[SentimentData] = None
    analyst_summary: Optional[str] = None
    last_report: Optional[dict] = None

class ComparisonReport(BaseModel):
    companies: List[CompanyReport]
    comparison_narrative: Optional[str] = None
    
    