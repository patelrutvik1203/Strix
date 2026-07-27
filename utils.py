# ==============================================================================
# OPTION EDGE AI - QUANT MATH & UTILITIES
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
