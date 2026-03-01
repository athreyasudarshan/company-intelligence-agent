from duckduckgo_search import DDGS
from schemas.company_schema import NewsItem
from typing import List

def search_company_news(company_name: str, max_results: int = 10) -> List[NewsItem]:
    try:
        news_items = []
        
        with DDGS() as ddgs:
            results = ddgs.news(
                keywords=f"{company_name} company news",
                max_results=max_results
            )
            
            for result in results:
                news_items.append(NewsItem(
                    title=result.get("title", ""),
                    summary=result.get("body", ""),
                    url=result.get("url", "")
                ))
        
        return news_items
    
    except Exception as e:
        print(f"Error fetching news for {company_name}: {e}")
        return []