import streamlit as st
import datetime
import random

# Core module imports for premium clean architecture
import config
from utils import logger
from broker_manager import BrokerManager
from market_data import MarketDataEngine
from option_chain import build_option_chain_dataframe
from scanner import SignalScanner
from heatmap import render_treemap_heatmap
from dashboard import draw_indices_dashboard
from signals import generate_ai_trade_recommendation
from strategy_builder import render_strategy_payoff_plotly
from charts import embed_tradingview_advanced_chart
from alerts import dispatch_live_alert
from portfolio import render_portfolio_and_margins
from settings import draw_system_preferences_terminal

# ==============================================================================
# 1. STATE INITIALIZATIONS & BOOTSTRAP
# ==============================================================================

if "broker_manager" not in st.session_state:
    st.session_state.broker_manager = BrokerManager()

if "data_engine" not in st.session_state:
    st.session_state.data_engine = MarketDataEngine(st.session_state.broker_manager)

if "scanner_engine" not in st.session_state:
    st.session_state.scanner_engine = SignalScanner()

if "custom_scans" not in st.session_state:
    st.session_state.custom_scans = []

# Fetch live index coordinates
indices = st.session_state.data_engine.fetch_index_quotes()

# Fallback spot prices if the feed is disconnected
spot = indices["nifty"]["value"] if indices.get("status") == "LIVE" else 24250.60
strike_interval = 50

# ==============================================================================
# SIDEBAR CONTROLLER (BROKER MANAGER & AUTHENTICATION)
# ==============================================================================

st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 20px;'>
    <h2 style='color:#3b82f6; font-weight:900; margin-bottom:0; font-size:1.6rem;'>OPTION EDGE AI</h2>
    <span style='color:#10b981; font-weight:700; font-size:0.75rem; letter-spacing:1.5px; uppercase;'>Quant Scanner & Analytics</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🔌 Broker Manager API Gateway")
broker_name = st.sidebar.selectbox("Select Broker API", options=config.BROKERS, index=0)

# Retrieve selected broker client object
client = st.session_state.broker_manager.set_active_broker(broker_name)

# Display authorization metrics
st.sidebar.text_input("Broker Client Code", value="Smart_5P_123456")
st.sidebar.text_input("Broker App password/token", type="password", value="secure_token_9988")

if not client.connected:
    if st.sidebar.button("🔌 Authenticate Session Key"):
        res = client.login("Smart_5P_123456", "secure_token_9988")
        st.sidebar.success(res["message"])
        st.rerun()
else:
    st.sidebar.success(f"🟢 Connected to {client.name}")
    if st.sidebar.button("🔌 Disconnect Session"):
        client.connected = False
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("🎯 Navigation Menu")
menu = st.sidebar.radio(
    "Go To Screen",
    options=[
        "📊 Bloomberg Style Dashboard",
        "🗺️ Live Animated Stock Heat Map",
        "🟢 Sector Rotation (RRG Map)",
        "⛓️ Professional Option Chain",
        "📈 Open Interest Analysis",
        "🎯 Max Pain Calculator",
        "📐 Option Strategy Payoff Builder",
        "💻 TradingView Charts Terminal",
        "🤖 AI Scanner & Performance Audit",
        "🎛️ Custom Scanner Builder",
        "🧭 Swing & Positional Finder",
        "🔔 Alert Configuration Engine",
        "📂 Portfolio & 5paisa/IIFL Connect",
        "🔁 Trade Replay Mode",
        "💬 Option Edge AI Chatbot",
        "🚀 Historical Strategy Backtesting",
        "⚙️ Preferential Settings"
    ]
)

# ==============================================================================
# STICKY HEADER TICK BAR (INDEX VISUALIZATION)
# ==============================================================================

# Draw top KPI metrics cards using dashboard module
has_feed = draw_indices_dashboard(indices)

# ==============================================================================
# MODULE SCREEN DISPLAY ROUTER
# ==============================================================================

if has_feed or menu in ["💻 TradingView Charts Terminal", "⚙️ Preferential Settings", "📐 Option Strategy Payoff Builder"]:
    
    # SCREEN: BLOOMBERG DASHBOARD OVERVIEW
    if menu == "📊 Bloomberg Style Dashboard":
        st.subheader("Bloomberg F&O Dashboard Overview")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 📰 Real-Time Live Indian Stock Market News (Updated Live)")
            # Pull RSS News Live
            news_feed = fetcher.fetch_live_rss_news()
            for news in news_feed:
                st.markdown(f"""
                <div class="bloomberg-box">
                    <span style="color:#3b82f6; font-size:0.75rem; font-weight:bold;">{news['date']} | DAILY FEED</span><br>
                    <a href="{news['link']}" target="_blank" style="text-decoration:none; font-size:0.95rem; color:#fff; font-weight:bold;">
                        {news['title']}
                    </a>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown("### 🏦 FII & DII Positionings")
            st.markdown("""
            * **FII Net Cash:** +₹1,240.50 Cr (Bullish Buy)
            * **DII Net Cash:** +₹850.20 Cr (Bullish Buy)
            * **FII Index Longs:** 68.2% (Strong Continuation)
            """)

    # SCREEN: ANIMATED STOCK HEAT MAP
    elif menu == "🗺️ Live Animated Stock Heat Map":
        st.subheader("Interactive Stock Capitalization Heat Map")
        sector_filter = st.selectbox("Group by Sector Filter", options=["All Sectors", "Banking", "IT", "Energy", "FMCG"])
        raw_map_data = fetcher.fetch_live_heat_map_data()
        fig = render_treemap_heatmap(raw_map_data, sector_filter)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Plotly is required to draw heatmaps.")

    # SCREEN: SECTOR ROTATION RRG MAP
    elif menu == "🟢 Sector Rotation (RRG Map)":
        st.subheader("Relative Rotation Graph (RRG) - Industry Rotation Cycles")
        sectors = [
            {"Sector": "Banking", "RS_Ratio": 101.40, "RS_Momentum": 100.80, "Quadrant": "Leading"},
            {"Sector": "IT", "RS_Ratio": 99.20, "RS_Momentum": 101.50, "Quadrant": "Improving"},
            {"Sector": "Pharma", "RS_Ratio": 98.40, "RS_Momentum": 99.10, "Quadrant": "Lagging"},
            {"Sector": "Metal", "RS_Ratio": 100.80, "RS_Momentum": 98.40, "Quadrant": "Weakening"},
            {"Sector": "Auto", "RS_Ratio": 101.90, "RS_Momentum": 101.20, "Quadrant": "Leading"},
            {"Sector": "Energy", "RS_Ratio": 100.50, "RS_Momentum": 100.40, "Quadrant": "Leading"}
        ]
        if HAS_PLOTLY:
            fig = go.Figure()
            fig.add_shape(type="rect", x0=100, y0=100, x1=103, y1=103, fillcolor="rgba(16, 185, 129, 0.03)", line_width=0, layer="below")
            fig.add_shape(type="rect", x0=100, y0=97, x1=103, y1=100, fillcolor="rgba(245, 158, 11, 0.03)", line_width=0, layer="below")
            fig.add_shape(type="rect", x0=97, y0=97, x1=100, y1=100, fillcolor="rgba(239, 68, 68, 0.03)", line_width=0, layer="below")
            fig.add_shape(type="rect", x0=97, y0=100, x1=100, y1=103, fillcolor="rgba(59, 130, 246, 0.03)", line_width=0, layer="below")
            
            fig.add_shape(type="line", x0=100, y0=97, x1=100, y1=103, line=dict(color="rgba(255,255,255,0.15)", dash="dash"))
            fig.add_shape(type="line", x0=97, y0=100, x1=103, y1=100, line=dict(color="rgba(255,255,255,0.15)", dash="dash"))
            
            for sec in sectors:
                color = "#10b981" if sec["Quadrant"] == "Leading" else "#3b82f6" if sec["Quadrant"] == "Improving" else "#ef4444" if sec["Quadrant"] == "Lagging" else "#f59e0b"
                fig.add_trace(go.Scatter(
                    x=[sec["RS_Ratio"]],
                    y=[sec["RS_Momentum"]],
                    mode='markers+text',
                    marker=dict(size=20, color=color, line=dict(color='#fff', width=1)),
                    text=[sec["Sector"]],
                    textposition="top center",
                    textfont=dict(color="#fff", size=10, weight="bold"),
                    hovertemplate=f"<b>{sec['Sector']}</b><br>Strength: %{{x}}<br>Momentum: %{{y}}<extra></extra>"
                ))
            fig.update_layout(
                xaxis_title="Relative Strength (RS-Ratio)",
                yaxis_title="Relative Momentum (RS-Momentum)",
                xaxis=dict(range=[97, 103], showgrid=False, zeroline=False),
                yaxis=dict(range=[97, 103], showgrid=False, zeroline=False),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=500,
                showlegend=False,
                font=dict(color="#ffffff")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            render_table(sectors)

    # SCREEN: OPTIONS CHAIN
    elif menu == "⛓️ Professional Option Chain":
        st.subheader(f"Option Chain for {symbol} (Spot: ₹{spot:.2f})")
        df_chain = build_option_chain_dataframe(spot, strike_interval)
        render_table(df_chain)

    # SCREEN: OPEN INTEREST COMPARISON
    elif menu == "📈 Open Interest Analysis":
        st.subheader("Strike-Wise Open Interest comparison")
        strikes_oi = [round(spot / 50) * 50 + i * 50 for i in range(-5, 6)]
        call_oi = [int(100000 * math.exp(-abs(K - spot)/200)) for K in strikes_oi]
        put_oi = [int(95000 * math.exp(-abs(K - spot)/200)) for K in strikes_oi]
        
        if HAS_PLOTLY:
            fig = go.Figure(data=[
                go.Bar(name='Call OI', x=strikes_oi, y=call_oi, marker_color='#10b981'),
                go.Bar(name='Put OI', x=strikes_oi, y=put_oi, marker_color='#3b82f6')
            ])
            fig.update_layout(
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="Strike Price", gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(title="Open Interest (Contracts)", gridcolor="rgba(255,255,255,0.05)"),
                font=dict(color="#ffffff")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.bar_chart({"Call OI": call_oi, "Put OI": put_oi})

    # SCREEN: MAX PAIN CALCULATOR
    elif menu == "🎯 Max Pain Calculator":
        st.subheader("Expiry Max Pain Strike Price Optimizer")
        strikes_oi = [round(spot / 50) * 50 + i * 50 for i in range(-10, 11)]
        call_oi = [int(100000 * math.exp(-abs(K - spot)/200)) for K in strikes_oi]
        put_oi = [int(95000 * math.exp(-abs(K - spot)/200)) for K in strikes_oi]
        pain_results = calculate_max_pain(strikes_oi, call_oi, put_oi)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Max Pain Strike Price", f"₹{pain_results['max_pain']}")
        with col2:
            st.metric("Expected Bottom Boundary", f"₹{pain_results['expected_range_low']}")
        with col3:
            st.metric("Expected Top Boundary", f"₹{pain_results['expected_range_high']}")

    # SCREEN: OPTION STRATEGY PAYOFF
    elif menu == "📐 Option Strategy Payoff Builder":
        st.subheader("Multi-Leg Options Strategy Payoff Builder")
        strategy_preset = st.selectbox("Strategy Preset", ["Straddle", "Iron Condor"])
        atm_strike = round(spot / 50) * 50
        
        if strategy_preset == "Straddle":
            legs = [
                {'strike': atm_strike, 'premium': 150.0, 'type': 'call', 'side': 'buy', 'qty': 50},
                {'strike': atm_strike, 'premium': 120.0, 'type': 'put', 'side': 'buy', 'qty': 50}
            ]
        else:
            legs = [
                {'strike': atm_strike - 100, 'premium': 45.0, 'type': 'put', 'side': 'buy', 'qty': 50},
                {'strike': atm_strike - 50, 'premium': 95.0, 'type': 'put', 'side': 'sell', 'qty': 50},
                {'strike': atm_strike + 50, 'premium': 105.0, 'type': 'call', 'side': 'sell', 'qty': 50},
                {'strike': atm_strike + 100, 'premium': 50.0, 'type': 'call', 'side': 'buy', 'qty': 50}
            ]
        st.markdown("### Configurations")
        render_table(legs)
        fig, results = render_strategy_payoff_plotly(legs, spot, spot * 0.88, spot * 1.12)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    # SCREEN: TRADINGVIEW WIDGET
    elif menu == "💻 TradingView Charts Terminal":
        st.subheader("TradingView Live Interactive Charting Terminal")
        embed_tradingview_advanced_chart("BHEL")

    # SCREEN: AI QUANT PERFORMANCE SCANNER
    elif menu == "🤖 AI Scanner & Performance Audit":
        st.subheader("Live AI Signals validated against historical performance")
        signals = st.session_state.scanner_engine.scan_market()
        render_table(signals)

    # SCREEN: CUSTOM SCAN BUILDER
    elif menu == "🎛️ Custom Scanner Builder":
        st.subheader("Flexible Custom Options & Technical Scanner Builder")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            metric_opt = st.selectbox("Select Filter Metric", ["Underlying Price (LTP)", "RSI (14)", "EMA (20)"])
        with col_c2:
            operator_opt = st.selectbox("Condition Operator", ["Greater Than (>) ", "Less Than (<)"])
        with col_c3:
            value_opt = st.number_input("Trigger Target Value", value=50)
            
        if st.button("➕ Add Scan Condition"):
            new_cond = {"Metric": metric_opt, "Operator": operator_opt, "Target": value_opt, "Status": "Active"}
            st.session_state.custom_scans.append(new_cond)
            st.success("Condition added successfully!")
            st.rerun()
            
        if st.session_state.custom_scans:
            render_table(st.session_state.custom_scans)

    # SCREEN: SWING FINDER
    elif menu == "🧭 Swing & Positional Finder":
        st.subheader("Positional Swing Trade Signals Scanners")
        # Dynamic Swing recommendations computed on the fly
        try:
            import yfinance as yf
            tickers_list = ["TRENT.NS", "HAL.NS", "BHEL.NS"]
            data_yf = yf.download(tickers_list, period="1d", progress=False)
            swing_positions = []
            for ticker in tickers_list:
                ltp = float(data_yf["Close"][ticker].dropna().iloc[-1])
                swing_positions.append({
                    "Symbol": ticker.replace(".NS", ""),
                    "Signal": "SWING BUY",
                    "Current Price (LTP)": f"₹{ltp:.2f}",
                    "Target 1": f"₹{ltp * 1.045:.2f}",
                    "Stop Loss": f"₹{ltp * 0.965:.2f}"
                })
            render_table(swing_positions)
        except Exception:
            st.warning("Failed to retrieve live prices. Feed disconnected.")

    # SCREEN: ALERT PORTAL
    elif menu == "🔔 Alert Configuration Engine":
        st.subheader("Derivative & Price Alerts Dispatch Center")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            tel_id = st.text_input("Telegram Channel/Chat ID", value="@OptionEdgeAl_Signals")
            tel_token = st.text_input("Telegram Bot API Token", type="password", value="123456:ABC-DEF")
        with col_a2:
            alert_symbol = st.text_input("Alert Target Symbol", value="NIFTY")
            alert_val = st.number_input("Alert Limit Threshold Value", value=24300)
            
            if st.button("Set Live Alert"):
                msg = dispatch_live_alert(tel_id, tel_token, alert_symbol, "Price", alert_val)
                st.success(f"Dispatched test alert payload! msg: {msg}")

    # SCREEN: PORTFOLIO JOURNAL & LIVE BROKER CONNECTIONS
    elif menu == "📂 Portfolio & 5paisa/IIFL Connect":
        st.subheader("My Positions & Direct Execution Terminals")
        render_portfolio_and_margins(client)

    # SCREEN: REPLAY MODE
    elif menu == "🔁 Trade Replay Mode":
        st.subheader("Historical Derivatives Replay Mode")
        st.selectbox("Select Replay Speed", ["1x (Real-time)", "2x Speed", "5x Fast Speed"])
        if st.button("▶ Play Step"):
            st.session_state.replay_tick += 1
            st.rerun()
        st.metric("Replay Time Coordinates", f"09:{15 + st.session_state.replay_tick}:00 IST")

    # SCREEN: AI CHATBOT
    elif menu == "💬 Option Edge AI Chatbot":
        st.subheader("Option Edge AI Assistant & Strategy Generator")
        query = st.text_input("Type your market query or ask for a trade setup:")
        if st.button("Send Message"):
            rec = generate_ai_trade_recommendation(symbol, spot, strike_interval)
            st.write(f"**AI Recommendation Response:**")
            st.write(rec)

    # SCREEN: BACKTESTING SIMULATOR
    elif menu == "🚀 Historical Strategy Backtesting":
        st.subheader("Quant Historical Strategy Backtesting")
        st.button("Execute Backtest Simulator")

    # SCREEN: CONFIG PREFERENCES
    else:
        draw_system_preferences_terminal()

else:
    st.info("Awaiting live stream authorization. Please activate a broker or establish your connection in the sidebar.")
