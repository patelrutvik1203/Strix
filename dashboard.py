# ==============================================================================
# OPTION EDGE AI - MARKET DASHBOARD WIDGETS
# ==============================================================================
import streamlit as st

def draw_indices_dashboard(indices_dict: dict):
    """Draws sleek glassmorphic indices metrics cards at the top of the screen."""
    if not indices_dict or indices_dict.get("status") == "DISCONNECTED":
        st.markdown("""
        <div style='background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239, 68, 68, 0.2); padding:16px; border-radius:12px; margin-bottom:20px; text-align:center;'>
            <h3 style='color:#ef4444; margin:0; font-size:1.2rem; font-weight:800;'>🔴 Live Data Disconnected</h3>
            <span style='font-size:0.8rem; color:#94a3b8;'>Please check active broker connection in the sidebar or retry.</span>
        </div>
        """, unsafe_allow_html=True)
        return False
        
    nifty = indices_dict["nifty"]
    banknifty = indices_dict["banknifty"]
    vix = indices_dict["vix"]
    timestamp = indices_dict["timestamp"]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <span style='color:#94a3b8; font-size:0.75rem; font-weight:bold;'>NIFTY 50 (SPOT)</span>
            <h3 style='margin:4px 0; font-size:1.3rem; font-weight:900; color:#10b981;'>₹{nifty['value']:.2f}</h3>
            <span style='color:#10b981; font-size:0.7rem;'>+{nifty['change']:.2f} (+{nifty['pchange']:.2f}%)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <span style='color:#94a3b8; font-size:0.75rem; font-weight:bold;'>NIFTY BANK (SPOT)</span>
            <h3 style='margin:4px 0; font-size:1.3rem; font-weight:900; color:#ef4444;'>₹{banknifty['value']:.2f}</h3>
            <span style='color:#ef4444; font-size:0.7rem;'>{banknifty['change']:.2f} ({banknifty['pchange']:.2f}%)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class='metric-card'>
            <span style='color:#94a3b8; font-size:0.75rem; font-weight:bold;'>INDIA VIX</span>
            <h3 style='margin:4px 0; font-size:1.3rem; font-weight:900; color:#3b82f6;'>{vix['value']:.2f}</h3>
            <span style='color:#3b82f6; font-size:0.7rem;'>+{vix['pchange']}%</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class='metric-card'>
            <span style='color:#94a3b8; font-size:0.75rem; font-weight:bold;'>FEED SYNCHRONIZATION</span>
            <h3 style='margin:4px 0; font-size:1.3rem; font-weight:900; color:#10b981;'>🟢 ACTIVE</h3>
            <span style='color:#94a3b8; font-size:0.7rem;'>Last Update: {timestamp}</span>
        </div>
        """, unsafe_allow_html=True)
        
    return True
