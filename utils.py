# ==============================================================================
# OPTION EDGE AI - QUANT MATH & UTILITIES (FAIL-SAFE)
# ==============================================================================
import math
import logging

# Set up clean logging configurations
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("OptionEdgeAI")

def norm_cdf(x: float) -> float:
    """Cumulative standard normal distribution N(x) using high-precision math.erf."""
    try:
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))
    except (ValueError, ZeroDivisionError, OverflowError):
        return 0.0 if x < 0 else 1.0

def norm_pdf(x: float) -> float:
    """Probability density function of standard normal distribution N'(x)."""
    try:
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * (x ** 2))
    except OverflowError:
        return 0.0

def bsm_greeks(S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call") -> dict:
    """Calculate Black-Scholes-Merton option price and Greeks (Delta, Gamma, Theta, Vega, Rho)."""
    T = max(T, 0.00001)
    sigma = max(sigma, 0.0001)
    
    try:
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
    except (ValueError, ZeroDivisionError, OverflowError):
        d1 = 0.0
        d2 = 0.0
    
    N_d1 = norm_cdf(d1)
    N_d2 = norm_cdf(d2)
    n_prime_d1 = norm_pdf(d1)
    
    if option_type.lower() == "call":
        price = S * N_d1 - K * math.exp(-r * T) * N_d2
        delta = N_d1
        theta = - (S * n_prime_d1 * sigma) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * N_d2
        rho = K * T * math.exp(-r * T) * N_d2
    else:
        price = K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
        delta = N_d1 - 1.0
        theta = - (S * n_prime_d1 * sigma) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm_cdf(-d2)
        rho = -K * T * math.exp(-r * T) * norm_cdf(-d2)
        
    gamma = n_prime_d1 / (S * sigma * math.sqrt(T))
    vega = S * math.sqrt(T) * n_prime_d1
    
    return {
        "price": float(price),
        "delta": float(delta),
        "gamma": float(gamma),
        "theta": float(theta / 365.0),
        "vega": float(vega / 100.0),
        "rho": float(rho / 100.0)
    }

def calculate_implied_volatility(market_price: float, S: float, K: float, T: float, r: float, option_type: str = "call", max_iter: int = 100, tolerance: float = 0.0001) -> float:
    """Calculate Implied Volatility using Newton-Raphson numerical optimization."""
    sigma = 0.20 # Guess
    for _ in range(max_iter):
        greeks = bsm_greeks(S, K, T, r, sigma, option_type)
        diff = greeks["price"] - market_price
        if abs(diff) < tolerance:
            return float(sigma)
        vega = greeks["vega"] * 100.0
        if vega < 0.0001:
            sigma += 0.05
            continue
        sigma -= diff / vega
        if sigma <= 0.001: sigma = 0.001
        if sigma > 3.0: sigma = 3.0
    return float(sigma)

def calculate_max_pain(strikes: list, call_oi: list, put_oi: list) -> dict:
    """Calculate Expiry Max Pain strike targets using pure Python."""
    data_list = sorted(
        [{"strike": s, "call_oi": c, "put_oi": p} for s, c, p in zip(strikes, call_oi, put_oi)],
        key=lambda x: x["strike"]
    )
    total_pains = []
    for target in data_list:
        target_strike = target["strike"]
        call_loss = sum([(target_strike - d["strike"]) * d["call_oi"] for d in data_list if d["strike"] < target_strike])
        put_loss = sum([(d["strike"] - target_strike) * d["put_oi"] for d in data_list if d["strike"] > target_strike])
        total_pains.append({"strike": target_strike, "total_pain": call_loss + put_loss})
        
    min_pain_node = min(total_pains, key=lambda x: x["total_pain"])
    max_pain_strike = min_pain_node["strike"]
    
    sorted_pains = sorted(total_pains, key=lambda x: x["total_pain"])
    best_strikes = [node["strike"] for node in sorted_pains[:3]]
    expected_low = min(best_strikes)
    expected_high = max(best_strikes)
    
    if expected_low == expected_high:
        idx = [d["strike"] for d in data_list].index(max_pain_strike)
        lower_idx = max(0, idx - 2)
        upper_idx = min(len(data_list) - 1, idx + 2)
        expected_low = data_list[lower_idx]["strike"]
        expected_high = data_list[upper_idx]["strike"]
        
    return {
        "max_pain": float(max_pain_strike),
        "expected_range_low": float(expected_low),
        "expected_range_high": float(expected_high),
        "pain_chart_data": total_pains
    }

def calculate_strategy_payoff(legs: list, price_range: list) -> dict:
    """Calculate option combination payoff profile values."""
    payoff_curve = []
    for s_t in price_range:
        total_pnl = 0.0
        for leg in legs:
            strike = leg['strike']
            premium = leg['premium']
            qty = leg['qty']
            is_call = leg['type'].lower() == 'call'
            is_buy = leg['side'].lower() == 'buy'
            
            if is_call:
                gross_payoff = max(s_t - strike, 0.0)
            else:
                gross_payoff = max(strike - s_t, 0.0)
                
            if is_buy:
                net_payoff = (gross_payoff - premium) * qty
            else:
                net_payoff = (premium - gross_payoff) * qty
                
            total_pnl += net_payoff
            
        payoff_curve.append({
            "underlying_price": float(s_t),
            "pnl": float(total_pnl)
        })
        
    pnls = [p['pnl'] for p in payoff_curve]
    max_profit = max(pnls)
    max_loss = min(pnls)
    
    breakevens = []
    for i in range(len(payoff_curve) - 1):
        p1, p2 = payoff_curve[i], payoff_curve[i+1]
        if (p1['pnl'] < 0 and p2['pnl'] >= 0) or (p1['pnl'] >= 0 and p2['pnl'] < 0):
            slope = (p2['pnl'] - p1['pnl']) / (p2['underlying_price'] - p1['underlying_price'])
            if slope != 0:
                zero_x = p1['underlying_price'] - (p1['pnl'] / slope)
                breakevens.append(round(float(zero_x), 2))
                
    is_max_profit_inf = max_profit == pnls[0] or max_profit == pnls[-1] and max_profit > 1000
    is_max_loss_inf = max_loss == pnls[0] or max_loss == pnls[-1] and max_loss < -1000
    
    return {
        "payoff_data": payoff_curve,
        "max_profit": "Unlimited" if is_max_profit_inf else float(max_profit),
        "max_loss": "Unlimited" if is_max_loss_inf else float(max_loss),
        "risk_reward": "N/A" if is_max_loss_inf or is_max_profit_inf else abs(round(float(max_profit / max_loss), 2)) if max_loss != 0 else "N/A",
        "breakevens": breakevens
    }

def calculate_sharpe_ratio(returns: list, risk_free_rate: float = 0.07) -> float:
    """Calculate the Sharpe Ratio of returns."""
    if len(returns) < 2: return 0.0
    mean_ret = sum(returns) / len(returns)
    excess_ret = mean_ret - (risk_free_rate / 252.0)
    variance = sum([(r - mean_ret)**2 for r in returns]) / (len(returns) - 1)
    std_dev = math.sqrt(variance)
    return float(excess_ret / std_dev * math.sqrt(252.0)) if std_dev > 0 else 0.0

def calculate_sortino_ratio(returns: list, risk_free_rate: float = 0.07) -> float:
    """Calculate the Sortino Ratio of returns focusing on downside deviation."""
    if len(returns) < 2: return 0.0
    mean_ret = sum(returns) / len(returns)
    excess_ret = mean_ret - (risk_free_rate / 252.0)
    downside_returns = [r for r in returns if r < 0]
    if len(downside_returns) < 2: return 0.0
    downside_variance = sum([r**2 for r in downside_returns]) / len(downside_returns)
    downside_dev = math.sqrt(downside_variance)
    return float(excess_ret / downside_dev * math.sqrt(252.0)) if downside_dev > 0 else 0.0
