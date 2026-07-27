# ==============================================================================
# OPTION EDGE AI - HEAT MAP RENDERING WIDGET
# ==============================================================================
import pandas as pd

try:
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

def render_treemap_heatmap(raw_map_data: list, sector_filter: str = "All Sectors"):
    """
    Generate an interactive, vector-sharp Treemap Stock Heat Map.
    Each rectangle is sized by Market Capitalization, colored by daily moves (pchange),
    and categorized by Sector.
    """
    if not raw_map_data:
        return None
        
    filtered_data = raw_map_data
    if sector_filter != "All Sectors":
        filtered_data = [d for d in raw_map_data if d["sector"] == sector_filter]
        
    if HAS_PLOTLY and filtered_data:
        df_map = pd.DataFrame(filtered_data)
        fig = px.treemap(
            df_map,
            path=[px.Constant("Market Sectors"), 'sector', 'symbol'],
            values='mcap',
            color='pchange',
            color_continuous_scale=['#ef4444', '#f87171', '#94a3b8', '#34d399', '#10b981'],
            color_continuous_midpoint=0,
            hover_data=['name', 'ltp', 'pchange']
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#ffffff"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=500
        )
        return fig
    return None
