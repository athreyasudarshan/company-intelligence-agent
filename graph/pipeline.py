from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
from schemas.company_schema import CompanyReport, ComparisonReport
from agents.news_agent import run_news_agent
from agents.financials_agent import run_financials_agent
from agents.sentiment_agent import analyze_sentiment
from agents.report_agent import run_report_agent
from utils.memory import save_report, get_last_report
from agents.comparison_agent import run_comparison_agent

# Define the state
class AgentState(TypedDict):
    companies: List[dict]  # list of {"name": ..., "ticker": ...}
    company_reports: List[CompanyReport]
    comparison_report: Optional[ComparisonReport]

# Node: process each company
def process_companies(state: AgentState) -> AgentState:
    reports = []

    for company in state["companies"]:
        name = company["name"]
        ticker = company["ticker"]

        # Check memory for previous report
        last_report = get_last_report(ticker)
        if last_report:
            print(f"[Memory] Found previous report for {ticker} from {last_report['timestamp']}")

        # Run all agents for this company
        news = run_news_agent(name)
        financials = run_financials_agent(ticker)
        sentiment = analyze_sentiment(news)
        report = run_report_agent(name, ticker, financials, news, sentiment)

        # Save to memory
        save_report(name, ticker, {
            "stock_price": financials.stock_price,
            "sentiment": sentiment.overall,
            "sentiment_score": sentiment.score,
        })

        # Attach previous report to current report
        report.last_report = last_report
        reports.append(report)

    return {**state, "company_reports": reports}
# Node: compare companies
def compare_companies(state: AgentState) -> AgentState:
    comparison = run_comparison_agent(state["company_reports"])
    return {**state, "comparison_report": comparison}

# Build the graph
def build_pipeline():
    graph = StateGraph(AgentState)

    graph.add_node("process_companies", process_companies)
    graph.add_node("compare_companies", compare_companies)

    graph.set_entry_point("process_companies")
    graph.add_edge("process_companies", "compare_companies")
    graph.add_edge("compare_companies", END)

    return graph.compile()