# ==============================================================================
# OPTION EDGE AI - CONFIGURATION ENGINE
# ==============================================================================
import os

# Application Settings
APP_NAME = "OPTION EDGE AI"
THEME_DEFAULT = "dark"

# Default Indices and Symbols
DEFAULT_INDEX = "NIFTY"
DEFAULT_EXPIRY = "2026-07-30"

# Broker Configurations (Configured via env or sidebar settings)
BROKERS = ["Angel One SmartAPI", "Upstox API", "Zerodha Kite Connect", "Shoonya API", "5Paisa API"]

# Refresh Intervals (seconds)
REFRESH_INTERVALS = [1, 5, 15, 30]

# Math Core Settings
RISK_FREE_RATE = 0.07  # 7% standard rate in India
DAYS_IN_YEAR = 365.0
