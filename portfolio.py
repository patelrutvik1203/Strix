# ==============================================================================
# OPTION EDGE AI - PORTFOLIO JOURNAL TRACKING
# ==============================================================================
import streamlit as st

def render_portfolio_and_margins(broker_client):
    """
    Renders synchronized Demat cash balances, active holdings,
    and open options positions directly from active broker session.
    """
    if not broker_client or not broker_client.connected:
        st.markdown("""
        <div style='background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239, 68, 68, 0.2); padding:16px; border-radius:12px; margin-bottom:20px; text-align:center;'>
            <h4 style='color:#ef4444; margin:0; font-size:1.1rem; font-weight:800;'>🔴 Live Broker Sync Disconnected</h4>
            <span style='font-size:0.8rem; color:#94a3b8;'>Please authenticate with your broker API in the sidebar to sync holdings and margins.</span>
        </div>
        """, unsafe_allow_html=True)
        return False
        
    # Live margins
    margins = broker_client.fetch_margins()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Demat Cash", f"₹{margins['total_cash']:,}")
    with col2:
        st.metric("Utilized F&O Margin", f"₹{margins['utilized_margin']:,}")
    with col3:
        st.metric("Available Write Margin", f"₹{margins['available_margin']:,}")
        
    st.markdown("---")
    st.markdown("### 📊 Synchronized Demat Holdings")
    holdings = broker_client.fetch_holdings()
    st.dataframe(holdings, use_container_width=True)
    
    st.markdown("### ⛓️ Open Derivatives Positions")
    positions = broker_client.fetch_positions()
    st.dataframe(positions, use_container_width=True)
    return True
