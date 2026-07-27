# ==============================================================================
# OPTION EDGE AI - TRADINGVIEW CHARTS WIDGET
# ==============================================================================
import streamlit as st

def embed_tradingview_advanced_chart(symbol: str):
    """
    Embed an official, live, fully interactive TradingView Advanced Charts Widget
    with all technical overlays, drawing indicators, and multiple timeframes enabled.
    """
    st.components.v1.html(f"""
    <div class="tradingview-widget-container" style="height:550px;width:100%;">
      <div id="tradingview_chart_frame" style="height:100%;width:100%;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "BSE:{symbol}",
        "interval": "D",
        "timezone": "Asia/Kolkata",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart_frame"
      }});
      </script>
    </div>
    """, height=560, scrolling=False)
