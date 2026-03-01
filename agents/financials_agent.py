from tools.finance_tool import get_financial_data
from schemas.company_schema import FinancialData

def run_financials_agent(ticker: str) -> FinancialData:
    """
    Agent that fetches financial data for a given ticker symbol.
    """
    print(f"[Financials Agent] Fetching data for {ticker}...")
    financial_data = get_financial_data(ticker)
    print(f"[Financials Agent] Done for {ticker}")
    return financial_data