import yfinance as yf
from schemas.company_schema import FinancialData

def get_financial_data(ticker: str) -> FinancialData:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        market_cap = info.get("marketCap")
        if market_cap:
            if market_cap >= 1_000_000_000_000:
                market_cap_str = f"${market_cap / 1_000_000_000_000:.2f}T"
            elif market_cap >= 1_000_000_000:
                market_cap_str = f"${market_cap / 1_000_000_000:.2f}B"
            else:
                market_cap_str = f"${market_cap / 1_000_000:.2f}M"
        else:
            market_cap_str = None

        revenue = info.get("totalRevenue")
        if revenue:
            if revenue >= 1_000_000_000:
                revenue_str = f"${revenue / 1_000_000_000:.2f}B"
            else:
                revenue_str = f"${revenue / 1_000_000:.2f}M"
        else:
            revenue_str = None

        return FinancialData(
            stock_price=info.get("currentPrice"),
            market_cap=market_cap_str,
            pe_ratio=info.get("trailingPE"),
            week_52_high=info.get("fiftyTwoWeekHigh"),
            week_52_low=info.get("fiftyTwoWeekLow"),
            revenue=revenue_str,
            sector=info.get("sector")
        )

    except Exception as e:
        print(f"Error fetching financial data for {ticker}: {e}")
        return FinancialData()