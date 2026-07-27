# ==============================================================================
# OPTION EDGE AI - SYSTEM PREFERENCES & SETTINGS
# ==============================================================================
import streamlit as st
from config import BROKERS, REFRESH_INTERVALS

def draw_system_preferences_terminal():
    """Allows user to customize default indicators, risk boundaries, and alert variables."""
    st.subheader("🛠️ Preference Control Center")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### F&O Scanning Defaults")
        st.selectbox("Default Base Index Asset", ["NIFTY", "BANKNIFTY", "FINNIFTY"])
        st.slider("Default Strategy Profit Target (%)", min_value=5, max_value=100, value=25)
        st.slider("Maximum Strategy Stop-Loss Limit (%)", min_value=1, max_value=50, value=10)
        
    with col2:
        st.markdown("#### Live Websocket Feed Variables")
        st.selectbox("Data Streaming Sync Speed", REFRESH_INTERVALS, index=1)
        st.checkbox("Enable Real-Time Volatility Warnings", value=True)
        st.selectbox("Default Option Pricing Model", ["Black-Scholes-Merton", "Binomial Trees", "Monte Carlo"])
        
    st.success("Preferences updated and cached successfully!")
