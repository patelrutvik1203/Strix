# ==============================================================================
# OPTION EDGE AI - OPTION CHAIN BUILDER
# ==============================================================================
import math
import pandas as pd
from utils import bsm_greeks, calculate_implied_volatility

def build_option_chain_dataframe(spot: float, strike_interval: int, window_strikes: int = 8, r: float = 0.07, T: float = 10.0/365.0) -> pd.DataFrame:
    """
    Build a structured options chain around the current underlying spot price.
    Calculates intrinsic value, time value, and full Black-Scholes Greeks dynamically.
    """
    atm_strike = round(spot / strike_interval) * strike_interval
    strikes = [atm_strike + i * strike_interval for i in range(-window_strikes, window_strikes + 1)]
    
    chain_rows = []
    for K in strikes:
        # Volatility smile calculation
        dist_pct = abs(K - spot) / spot
        sigma = 0.12 + 0.5 * (dist_pct ** 2)
        
        call_greeks = bsm_greeks(spot, K, T, r, sigma, "call")
        put_greeks = bsm_greeks(spot, K, T, r, sigma, "put")
        
        call_price = call_greeks["price"]
        put_price = put_greeks["price"]
        
        # Intrinsic & Time Value calculations
        call_intrinsic = max(spot - K, 0.0)
        call_time = max(call_price - call_intrinsic, 0.0)
        
        put_intrinsic = max(K - spot, 0.0)
        put_time = max(put_price - put_intrinsic, 0.0)
        
        # Simulated Open interest
        call_oi = int(120000 * math.exp(-abs(K - spot)/150))
        put_oi = int(115000 * math.exp(-abs(K - spot)/150))
        
        chain_rows.append({
            "Call OI": call_oi,
            "Call LTP": round(call_price, 2),
            "Call Delta": round(call_greeks["delta"], 3),
            "Call Gamma": round(call_greeks["gamma"], 4),
            "Call Theta": round(call_greeks["theta"], 2),
            "Call Vega": round(call_greeks["vega"], 2),
            "Call Intrinsic": round(call_intrinsic, 2),
            "Call Time Value": round(call_time, 2),
            "Strike Price": K,
            "Put Intrinsic": round(put_intrinsic, 2),
            "Put Time Value": round(put_time, 2),
            "Put LTP": round(put_price, 2),
            "Put Delta": round(put_greeks["delta"], 3),
            "Put Gamma": round(put_greeks["gamma"], 4),
            "Put Theta": round(put_greeks["theta"], 2),
            "Put Vega": round(put_greeks["vega"], 2),
            "Put OI": put_oi
        })
        
    return pd.DataFrame(chain_rows)
