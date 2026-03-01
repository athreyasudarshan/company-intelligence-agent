from tools.search_tool import search_company_news
from schemas.company_schema import NewsItem
from typing import List

def run_news_agent(company_name: str) -> List[NewsItem]:
    """
    Agent that fetches recent news for a given company.
    """
    print(f"[News Agent] Searching news for {company_name}...")
    news_items = search_company_news(company_name)
    print(f"[News Agent] Found {len(news_items)} articles for {company_name}")
    return news_items