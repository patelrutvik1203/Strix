# ==============================================================================
# OPTION EDGE AI - OPTIONS STRATEGY BUILDER
# ==============================================================================
import pandas as pd
from utils import calculate_strategy_payoff

try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def render_strategy_payoff_plotly(legs: list, spot: float, min_val: float, max_val: float):
    """
    Generate an interactive, vector-sharp Strategy Payoff Curve
    complete with underlying spot lines and breakeven annotations.
    """
    import numpy as np
    
    # Range of prices
    price_range = np.linspace(min_val, max_val, 100).tolist()
    payoff_results = calculate_strategy_payoff(legs, price_range)
    
    curve_df = pd.DataFrame(payoff_results["payoff_data"])
    
    if HAS_PLOTLY:
        fig = go.Figure()
        
        # Add curve trace
        fig.add_trace(go.Scatter(
            x=curve_df['underlying_price'],
            y=curve_df['pnl'],
            mode='lines',
            name='Net Strategy Payoff',
            line=dict(color='#10b981', width=3),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.05)'
        ))
        
        # Crosshair lines
        fig.add_shape(type="line", x0=spot, y0=min(curve_df['pnl']), x1=spot, y1=max(curve_df['pnl']), line=dict(color="#3b82f6", dash="dot"))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Underlying Price (₹)", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Profit / Loss (₹)", gridcolor="rgba(255,255,255,0.05)"),
            font=dict(color="#ffffff"),
            margin=dict(l=40, r=20, t=30, b=40)
        )
        return fig, payoff_results
        
    return None, payoff_results
