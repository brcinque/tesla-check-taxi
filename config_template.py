# Tesla Robotaxi Monitor Configuration
# Copy this to config.py and add your API keys

# News API (get free key from https://newsapi.org/)
NEWS_API_KEY = "your_news_api_key_here"

# Finnhub API for financial market data (https://finnhub.io/)
FINNHUB_API_KEY = "your_finnhub_api_key_here"

# Alpha Vantage for stock data (free from https://www.alphavantage.co/)
ALPHA_VANTAGE_KEY = "your_alpha_vantage_key_here"

# Search terms for monitoring
SEARCH_TERMS = {
    'tesla_fsd': [
        'Tesla Full Self-Driving',
        'Tesla FSD',
        'Tesla Autopilot',
        'Tesla robotaxi',
        'Tesla autonomous'
    ],
    'accidents': [
        'Tesla crash',
        'Tesla accident FSD',
        'Tesla Autopilot crash'
    ],
    'regulatory': [
        'NHTSA Tesla investigation',
        'Tesla regulatory approval',
        'Tesla autonomous permit'
    ],
    'competition': [
        'Waymo robotaxi',
        'Cruise autonomous',
        'Baidu Apollo robotaxi'
    ]
}

# Risk thresholds
RISK_THRESHOLDS = {
    'low': 30,
    'moderate': 50,
    'high': 70,
    'critical': 85
}

# Data sources
DATA_SOURCES = {
    'nhtsa_api': 'https://api.nhtsa.gov/complaints/complaintsByVehicle',
    'sec_filings': 'https://www.sec.gov/cgi-bin/browse-edgar',
    'tesla_safety_reports': 'https://www.tesla.com/VehicleSafetyReport'
}

# Update frequency (in days)
UPDATE_FREQUENCY = 7

# Historical data storage
HISTORICAL_DATA_FILE = 'tesla_robotaxi_history.json'
