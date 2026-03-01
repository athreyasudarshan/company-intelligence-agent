import streamlit as st
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graph.pipeline import build_pipeline

st.set_page_config(
    page_title="ARIA — Company Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080B0F !important;
    color: #E8EAF0 !important;
    font-family: 'Space Mono', monospace !important;
}

[data-testid="stAppViewContainer"] {
    background: 
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,200,120,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(0,140,255,0.06) 0%, transparent 60%),
        #080B0F !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: transparent !important;
    display: none !important;
}

section[data-testid="stSidebar"] { display: none; }

/* ── MAIN CONTAINER ── */
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1400px !important;
}

/* ── HIDE STREAMLIT ELEMENTS ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── MASTHEAD ── */
.masthead {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid rgba(0,200,120,0.2);
    margin-bottom: 2.5rem;
}

.masthead-left {}

.masthead-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.6rem;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    line-height: 1;
}

.masthead-logo span {
    color: #00C878;
}

.masthead-tagline {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #4A5568;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.masthead-right {
    text-align: right;
}

.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #00C878;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: 1px solid rgba(0,200,120,0.3);
    padding: 0.3rem 0.7rem;
    border-radius: 2px;
}

.live-dot {
    width: 6px;
    height: 6px;
    background: #00C878;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
}

/* ── INPUT PANEL ── */
.input-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.input-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00C878, #0088FF, transparent);
}

.panel-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #00C878;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* ── STREAMLIT INPUT OVERRIDES ── */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 2px !important;
    color: #E8EAF0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    padding: 0.6rem 0.8rem !important;
    transition: border-color 0.2s !important;
}

[data-testid="stTextInput"] input {
    background: #1A1F2E !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 2px !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #00C878 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    padding: 0.6rem 0.8rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #2D3748 !important;
    -webkit-text-fill-color: #2D3748 !important;
    opacity: 1 !important;
}

[data-testid="stTextInput"] label {
    color: #4A5568 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: #00C878 !important;
    color: #080B0F !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #00E090 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0,200,120,0.25) !important;
}

/* ── DIVIDER ── */
.section-divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0 1.5rem;
}

.section-divider-line {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.06);
}

.section-divider-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #2D3748;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── COMPANY CARD ── */
.company-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 4px;
    padding: 1.6rem;
    position: relative;
    overflow: hidden;
    height: 100%;
    transition: border-color 0.3s;
}

.company-card:hover {
    border-color: rgba(0,200,120,0.2);
}

.company-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,200,120,0.3), transparent);
}

.card-ticker {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    color: #FFFFFF;
    line-height: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #4A5568;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.2rem;
    margin-bottom: 1.2rem;
}

.card-price {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 2.2rem;
    color: #00C878;
    line-height: 1;
    margin-bottom: 0.2rem;
}

.card-price-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: #2D3748;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── METRIC ROWS ── */
.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.metric-row:last-child { border-bottom: none; }

.metric-key {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #4A5568;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.metric-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #A0AEC0;
    font-weight: 700;
    text-align: right;
    max-width: 60%;
    word-break: break-word;
}

/* ── SENTIMENT BADGE ── */
.sentiment-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.8rem;
    border-radius: 2px;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 700;
    margin: 1rem 0;
}

.sentiment-positive { background: rgba(0,200,120,0.1); color: #00C878; border: 1px solid rgba(0,200,120,0.3); }
.sentiment-neutral { background: rgba(255,200,0,0.1); color: #FFC800; border: 1px solid rgba(255,200,0,0.3); }
.sentiment-negative { background: rgba(255,60,60,0.1); color: #FF3C3C; border: 1px solid rgba(255,60,60,0.3); }

/* ── ANALYST SUMMARY ── */
.analyst-block {
    background: rgba(0,200,120,0.03);
    border-left: 2px solid rgba(0,200,120,0.4);
    padding: 0.8rem 1rem;
    margin-top: 1rem;
    border-radius: 0 2px 2px 0;
}

.analyst-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    color: #00C878;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}

.analyst-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #718096;
    line-height: 1.7;
}

/* ── COMPARISON PANEL ── */
.comparison-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 4px;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    margin-top: 1rem;
}

.comparison-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0088FF, #00C878);
}

.comparison-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #0088FF;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.comparison-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #A0AEC0;
    line-height: 1.9;
}

/* ── NEWS SECTION ── */
.news-item {
    padding: 0.8rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.news-item:last-child { border-bottom: none; }

.news-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #CBD5E0;
    line-height: 1.5;
    margin-bottom: 0.2rem;
}

.news-summary {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #4A5568;
    line-height: 1.6;
}

/* ── AGENT STATUS ── */
.agent-status {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.5rem 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #4A5568;
}

.agent-status-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #00C878;
    animation: pulse 1s infinite;
}

/* ── STREAMLIT OVERRIDES ── */
[data-testid="stMetric"] {
    background: transparent !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.6rem !important;
    color: #4A5568 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    color: #E8EAF0 !important;
}

div[data-testid="column"] {
    padding: 0 0.5rem !important;
}

.stAlert {
    background: rgba(255,60,60,0.05) !important;
    border: 1px solid rgba(255,60,60,0.2) !important;
    border-radius: 2px !important;
    color: #FC8181 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}

.stSpinner > div {
    border-top-color: #00C878 !important;
}

/* ── PLOTLY CHART CONTAINER ── */
[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 4px !important;
    padding: 0.5rem !important;
}

/* ── SCORE BAR ── */
.score-bar-container {
    margin: 0.8rem 0;
}

.score-bar-label {
    display: flex;
    justify-content: space-between;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #4A5568;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}

.score-bar-track {
    height: 4px;
    background: rgba(255,255,255,0.06);
    border-radius: 2px;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s ease;
}

.score-bar-green { background: linear-gradient(90deg, #00C878, #00E090); }
.score-bar-blue { background: linear-gradient(90deg, #0088FF, #00B4FF); }
.score-bar-red { background: linear-gradient(90deg, #FF3C3C, #FF6B6B); }

</style>
""", unsafe_allow_html=True)

# ── MASTHEAD ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-left">
        <div class="masthead-logo">AR<span>I</span>A</div>
        <div class="masthead-tagline" style="font-family:Syne,sans-serif; font-weight:600; font-size:0.85rem; background: linear-gradient(90deg, #00C878, #A0AEC0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:0.05em;">Agentic Research & Intelligence Analyst</div>
    </div>
    <div class="masthead-right">
        <div class="live-badge">
            <div class="live-dot"></div>
            Live Market Data
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUT PANEL ─────────────────────────────────────────────────────────────
st.markdown('''<div class="input-panel">
    <div class="panel-label">◈ Intelligence Query</div>
    <div style="font-family:Syne,sans-serif; font-weight:600; font-size:1rem; background: linear-gradient(90deg, #00C878, #A0AEC0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-top:0.6rem; line-height:1.7; letter-spacing:0.02em;">
        AI-powered company intelligence, delivered by autonomous agents.
    </div>
</div>''', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([2, 2, 2, 1])

with col1:
    company1 = st.text_input("Company 1", placeholder="e.g Apple", key="c1")
    ticker1 = st.text_input("Ticker 1", placeholder="e.g AAPL", key="t1")

with col2:
    company2 = st.text_input("Company 2", placeholder="e.g Microsoft", key="c2")
    ticker2 = st.text_input("Ticker 2", placeholder="e.g MSFT", key="t2")

with col3:
    company3 = st.text_input("Company 3 (optional)", placeholder="e.g Google", key="c3")
    ticker3 = st.text_input("Ticker 3 (optional)", placeholder="e.g GOOGL", key="t3")

with col4:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("⬡ Run Analysis", type="primary")

# ── ANALYSIS ────────────────────────────────────────────────────────────────
if analyze_btn:

    companies = []
    if company1 and ticker1:
        companies.append({"name": company1, "ticker": ticker1.upper()})
    if company2 and ticker2:
        companies.append({"name": company2, "ticker": ticker2.upper()})
    if company3 and ticker3:
        companies.append({"name": company3, "ticker": ticker3.upper()})

    if len(companies) < 2:
        st.error("⚠ Minimum two companies required for comparative analysis.")
    else:
        # Agent status display
        status_placeholder = st.empty()
        agents = ["Financials Agent", "News Agent", "Sentiment Agent", "Report Agent", "Comparison Agent"]
        
        with st.spinner(""):
            for i, agent in enumerate(agents):
                status_placeholder.markdown(f"""
                <div style="padding:1rem; background:rgba(0,200,120,0.03); border:1px solid rgba(0,200,120,0.1); border-radius:4px;">
                    <div class="panel-label" style="margin-bottom:0.8rem;">◈ Agent Pipeline Running</div>
                    {''.join([f'<div class="agent-status"><div class="agent-status-dot" style="background:{"#00C878" if j < i else "#2D3748"};animation:{"none" if j < i else "pulse 1s infinite"}"></div>{a} {"— done" if j < i else "— processing..." if j == i else ""}</div>' for j, a in enumerate(agents)])}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.3)

            pipeline = build_pipeline()
            result = pipeline.invoke({
                "companies": companies,
                "company_reports": [],
                "comparison_report": None
            })

        status_placeholder.empty()

        # ── SECTION DIVIDER ──
        st.markdown("""
        <div class="section-divider">
            <div class="section-divider-line"></div>
            <div class="section-divider-label">◈ Company Intelligence Reports</div>
            <div class="section-divider-line"></div>
        </div>
        """, unsafe_allow_html=True)

        # ── COMPANY CARDS ──
        import plotly.graph_objects as go

        card_cols = st.columns(len(result["company_reports"]))

        for i, report in enumerate(result["company_reports"]):
            with card_cols[i]:
                f = report.financials
                s = report.sentiment

                sentiment_class = {
                    "Positive": "sentiment-positive",
                    "Neutral": "sentiment-neutral",
                    "Negative": "sentiment-negative"
                }.get(s.overall if s else "Neutral", "sentiment-neutral")

                sentiment_icon = {
                    "Positive": "▲",
                    "Neutral": "◆",
                    "Negative": "▼"
                }.get(s.overall if s else "Neutral", "◆")

                score_pct = int((s.score if s else 0.5) * 100)

                card_html = f'<div class="company-card">'
                card_html += f'<div class="card-ticker">{report.ticker}</div>'
                card_html += f'<div class="card-name">{report.company_name}</div>'
                card_html += f'<div class="card-price">${f.stock_price if f and f.stock_price else "—"}</div>'
                card_html += f'<div class="card-price-label">Current Price (USD)</div>'
                card_html = f'<div class="company-card">'
                card_html += f'<div class="card-ticker">{report.ticker}</div>'
                card_html += f'<div class="card-name">{report.company_name}</div>'
                card_html += f'<div class="card-price">${f.stock_price if f and f.stock_price else "—"}</div>'
                card_html += f'<div class="card-price-label">Current Price (USD)</div>'

                # Memory badge
                if report.last_report:
                    last_price = report.last_report.get("stock_price", "N/A")
                    last_sentiment = report.last_report.get("sentiment", "N/A")
                    last_time = report.last_report.get("timestamp", "N/A")
                    
                    try:
                        price_change = ""
                        if last_price and last_price != "N/A" and report.financials and report.financials.stock_price:
                            diff = round(report.financials.stock_price - float(last_price), 2)
                            if diff > 0:
                                price_change = f'<span style="color:#00C878">▲ ${diff} since last analysis</span>'
                            elif diff < 0:
                                price_change = f'<span style="color:#FF3C3C">▼ ${abs(diff)} since last analysis</span>'
                            else:
                                price_change = f'<span style="color:#718096">No price change</span>'
                    except:
                        price_change = ""

                    card_html += f'''<div style="background:rgba(0,200,120,0.05);border:1px solid rgba(0,200,120,0.15);border-radius:2px;padding:0.6rem 0.8rem;margin-bottom:1rem;font-family:Space Mono,monospace;font-size:0.62rem;color:#4A5568;">
                        <span style="color:#00C878;letter-spacing:0.1em;">◈ LAST ANALYZED</span> {last_time}<br>
                        <span style="color:#718096;">Previous sentiment: {last_sentiment} · {price_change}</span>
                    </div>'''

                if f:
                    for label, val in [
                        ("Market Cap", f.market_cap or "—"),
                        ("P/E Ratio", str(round(f.pe_ratio, 1)) if f.pe_ratio else "—"),
                        ("52W High", f"${f.week_52_high}" if f.week_52_high else "—"),
                        ("52W Low", f"${f.week_52_low}" if f.week_52_low else "—"),
                        ("Revenue", f.revenue or "—"),
                        ("Sector", f.sector or "—"),
                    ]:
                        card_html += f'<div class="metric-row"><span class="metric-key">{label}</span><span class="metric-val">{val}</span></div>'

                card_html += f'<div class="sentiment-badge {sentiment_class}" style="margin-top:1rem">{sentiment_icon} {s.overall if s else "Neutral"} · {score_pct}%</div>'
                card_html += f'<div class="score-bar-container"><div class="score-bar-label"><span>Sentiment Score</span><span>{score_pct}/100</span></div><div class="score-bar-track"><div class="score-bar-fill score-bar-green" style="width:{score_pct}%"></div></div></div>'

                safe_analyst = (report.analyst_summary or "—").replace("<", "&lt;").replace(">", "&gt;")
                card_html += f'<div class="analyst-block"><div class="analyst-label">◈ AI Analyst</div><div class="analyst-text">{safe_analyst}</div></div>'

                card_html += '<div style="margin-top:1.2rem"><div class="panel-label" style="margin-bottom:0.6rem">Recent Headlines</div>'
                if report.news:
                    for item in report.news[:3]:
                        safe_title = (item.title or "").replace("<", "&lt;").replace(">", "&gt;")
                        safe_sum = (item.summary or "")[:120].replace("<", "&lt;").replace(">", "&gt;")
                        url = item.url or "#"
                        card_html += f'<div class="news-item"><div class="news-title"><a href="{url}" target="_blank" style="color:#CBD5E0;text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:1px;">{safe_title}</a></div><div class="news-summary">{safe_sum}...</div></div>'
                card_html += '</div></div>'

                st.markdown(card_html, unsafe_allow_html=True)

        # ── CHARTS ──
        st.markdown("""
        <div class="section-divider">
            <div class="section-divider-line"></div>
            <div class="section-divider-label">◈ Visual Analytics</div>
            <div class="section-divider-line"></div>
        </div>
        """, unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns([1, 1])

        with chart_col1:
            names = [r.company_name for r in result["company_reports"]]
            prices = [r.financials.stock_price if r.financials and r.financials.stock_price else 0 for r in result["company_reports"]]
            colors = ["#00C878", "#0088FF", "#FF8C00"]

            fig1 = go.Figure(go.Bar(
                x=names,
                y=prices,
                marker=dict(
                    color=colors[:len(names)],
                    opacity=0.85,
                    line=dict(width=0)
                ),
                text=[f"${p}" for p in prices],
                textposition="outside",
                textfont=dict(family="Space Mono", size=11, color="#A0AEC0")
            ))

            fig1.update_layout(
                title=dict(text="STOCK PRICE COMPARISON", font=dict(family="Space Mono", size=10, color="#4A5568"), x=0.02),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Space Mono", color="#4A5568"),
                xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=10, color="#718096"), linecolor="rgba(255,255,255,0.06)"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickfont=dict(family="Space Mono", size=9, color="#4A5568"), linecolor="rgba(255,255,255,0.06)"),
                margin=dict(t=40, b=20, l=10, r=10),
                height=300
            )
            st.plotly_chart(fig1, use_container_width=True)

        with chart_col2:
            fig2 = go.Figure()
            for j, report in enumerate(result["company_reports"]):
                if report.sentiment:
                    s = report.sentiment
                    fig2.add_trace(go.Bar(
                        name=report.company_name,
                        x=["Positive", "Neutral", "Negative"],
                        y=[s.positive_count, s.neutral_count, s.negative_count],
                        marker=dict(color=colors[j], opacity=0.85, line=dict(width=0))
                    ))

            fig2.update_layout(
                title=dict(text="SENTIMENT BREAKDOWN", font=dict(family="Space Mono", size=10, color="#4A5568"), x=0.02),
                barmode="group",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Space Mono", color="#4A5568"),
                xaxis=dict(showgrid=False, tickfont=dict(family="Space Mono", size=10, color="#718096"), linecolor="rgba(255,255,255,0.06)"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickfont=dict(family="Space Mono", size=9, color="#4A5568"), linecolor="rgba(255,255,255,0.06)"),
                legend=dict(font=dict(family="Space Mono", size=9, color="#4A5568"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(t=40, b=20, l=10, r=10),
                height=300
            )
            st.plotly_chart(fig2, use_container_width=True)

        # ── COMPARISON NARRATIVE ──
        st.markdown("""
        <div class="section-divider">
            <div class="section-divider-line"></div>
            <div class="section-divider-label">◈ Comparative Intelligence</div>
            <div class="section-divider-line"></div>
        </div>
        """, unsafe_allow_html=True)

        if result["comparison_report"]:
            st.markdown(f"""
            <div class="comparison-panel">
                <div class="comparison-label">◈ AI Comparative Analysis — {" vs ".join([r.company_name for r in result["company_reports"]])}</div>
                <div class="comparison-text">{result["comparison_report"].comparison_narrative}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── FOOTER ──
        st.markdown("""
        <div style="margin-top:3rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.04); text-align:center;">
            <div style="font-family:'Space Mono',monospace; font-size:0.58rem; color:#2D3748; letter-spacing:0.15em; text-transform:uppercase;">
                ARIA · Multi-Agent Company Intelligence · Powered by LangGraph + Groq + LLaMA 3
            </div>
        </div>
        """, unsafe_allow_html=True)