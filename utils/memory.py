import chromadb
import json
import os
from datetime import datetime

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./aria_memory")
collection = client.get_or_create_collection(name="company_reports")

def save_report(company_name: str, ticker: str, report_data: dict):
    """Save a company report to ChromaDB memory."""
    try:
        doc_id = f"{ticker.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        document = json.dumps(report_data)
        
        collection.upsert(
            ids=[ticker.upper()],
            documents=[document],
            metadatas=[{
                "company_name": company_name,
                "ticker": ticker.upper(),
                "timestamp": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
                "stock_price": str(report_data.get("stock_price", "N/A")),
                "sentiment": report_data.get("sentiment", "N/A"),
                "sentiment_score": str(report_data.get("sentiment_score", "N/A"))
            }]
        )
        print(f"[Memory] Saved report for {ticker}")
    except Exception as e:
        print(f"[Memory] Error saving report: {e}")

def get_last_report(ticker: str):
    """Retrieve the last report for a company."""
    try:
        results = collection.get(
            ids=[ticker.upper()],
            include=["metadatas", "documents"]
        )
        
        if results and results["ids"]:
            metadata = results["metadatas"][0]
            return metadata
        return None
    except Exception as e:
        print(f"[Memory] Error retrieving report: {e}")
        return None