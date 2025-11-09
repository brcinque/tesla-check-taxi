# Tesla Robotaxi Failure Indicator System

Real-time monitoring system tracking Tesla's robotaxi progress with 12+ data sources, comprehensive risk analysis, and automated journey tracking against milestone goals.

![Dashboard Example](docs/dashboard-example.png)

## Quick Start

```bash
python3 tesla_robotaxi_monitor.py
```

Outputs (saved to `output/` directory):
- `tesla_robotaxi_dashboard.png` - Visual dashboard
- `tesla_robotaxi_report.txt` - Detailed report
- `tesla_robotaxi_history.json` - Historical tracking data

## Current Assessment: **53.6% Failure Risk** ⚠️

### Key Red Flags:
- **Executive Departures: 0.0/100** ⚠️
- **Competitor Progress: 25.0/100** 🚨 Tesla 5+ years behind (REAL DATA)
- **Timeline Slippage: 37.5/100** 🚨 10 years of missed promises
- **Insider Selling: 40.0/100** ⚠️ Heavy executive sales (SEC EDGAR TRACKING)

## 9 Indicators Tracked

| Indicator | Weight | Current Score |
|-----------|--------|---------------|
| Regulatory Sentiment | 20% | 55.0/100 |
| Safety Incidents | 20% | 45.0/100 |
| Timeline Slippage | 15% | 37.5/100 🚨 |
| Competitor Progress | 10% | 25.0/100 🚨 |
| Insider Selling | 10% | 40.0/100 |
| News Sentiment | 10% | 53.0/100 |
| Technical Progress | 10% | 60.0/100 |
| Market Confidence | 5% | 59.8/100 |
| Executive Departures | 0% | Red Flag Indicator |

## Decision Framework

### 🚫 EXIT TRIGGERS (Consider Selling)
- Failure Risk > 75% for 2+ checks
- Major safety incident with regulatory crackdown
- Stock falls below $300
- Musk announces indefinite delay

### ⏸️ HOLD TRIGGERS (Maintain)
- Failure Risk < 50%
- Regulatory approvals received
- Unsupervised operation launches

### ✅ ADD TRIGGERS (Increase Position)
- Failure Risk < 30%
- Commercial service launches
- Multiple city approvals

## Usage Recommendations

- **Weekly** if actively monitoring
- **Monthly** for long-term holders
- **Immediately** after major news

## Project Structure

```
tesla-check/
├── tesla_robotaxi_monitor.py  # Main monitoring script (enhanced with real data)
├── real_data_monitor.py       # Real-time data fetching (5 sources)
├── config_template.py         # Configuration template
├── requirements.txt           # Python dependencies
├── DATA_SOURCES_GUIDE.md      # Comprehensive data sources documentation
├── FREE_ACCESS_GUIDE.md       # How to access premium sources for free! 🆓
├── input/                     # Input data directory
│   ├── sources.txt            # Data source framework & references
│   └── crowd-source.txt       # Free access methods & ethical workarounds
└── output/                    # Generated reports and charts
    ├── tesla_robotaxi_dashboard.png
    ├── tesla_robotaxi_report.txt
    └── tesla_robotaxi_history.json
```

## Features

✅ **Smart File Management** - Outputs saved to organized directories  
✅ **Historical Tracking** - Tracks scores over time with persistence  
✅ **Real-Time Data Integration** - Multiple live data sources:
  - 📰 News API (Tesla robotaxi news & sentiment)
  - 💼 SEC Edgar (Insider trading filings - no key required!)
  - 🚨 NHTSA (Safety data - no key required!)
  - 🏁 Competitor Progress (Waymo, Baidu, Cruise tracking)
  - 🚩 Red Flag Scorecard (Exit criteria monitoring)
✅ **Error Handling** - Graceful failure recovery  
✅ **Configuration Support** - Customizable thresholds and data sources  
✅ **Comprehensive Source Framework** - Based on industry best practices

## Installation

```bash
pip install -r requirements.txt
python3 tesla_robotaxi_monitor.py
```

## Optional: Real-Time Data Integration

For real-time news sentiment analysis:

1. Copy `config_template.py` to `config.py`
2. Add your News API key from https://newsapi.org/
3. Run the monitor - it will automatically use real data when available

## The Reality Check

**Today (Nov 2025):**
- Tesla: 0 robotaxi cities, supervised only
- Waymo: 4 cities, 150K+ weekly rides, fully driverless
- Baidu: 11 cities (China), 60K+ weekly rides
- Timeline: 10 years of missed promises

**The 50/50 bet:** Current valuation assumes equal chance of success/failure.

---

## 📡 Live Data Sources

**Works Out of the Box (No API Key Required):**
- 💼 SEC Edgar - Real-time insider trading filings
- 🚨 NHTSA - Vehicle safety tracking
- 🏁 Competitor Progress - Waymo, Baidu, Cruise data
- 🚩 Red Flag Scorecard - Exit criteria monitoring

**Enhanced with News API (Free Tier Available):**
- 📰 Tesla news sentiment (last 30 days)
- 🔥 Safety incident tracking from news
- 📋 Regulatory mention monitoring

See `DATA_SOURCES_GUIDE.md` for complete source documentation.

**💰 Want Professional Research for FREE?**  
Check `FREE_ACCESS_GUIDE.md` for ethical ways to access paywalled content:
- Library access (WSJ, FT, Bloomberg - FREE!)
- Brokerage research (professional reports - FREE!)
- Academic sources (peer-reviewed studies - FREE!)
- 95% complete system for $0-50/year

---

## ⚠️ Disclaimer

**NOT FINANCIAL ADVICE** - This is an educational research tool and personal monitoring system. It is not intended as investment advice, and users should conduct their own research and consult qualified professionals before making any financial decisions.

**Data Sources** - All data is aggregated from publicly available sources including government agencies (NHTSA, SEC, CPUC), financial APIs, and news services. Data accuracy depends on source reliability and API availability. Users should independently verify information before relying on it.

**Analysis & Opinion** - Risk assessments, scores, and commentary represent the tool creator's analysis and opinion based on available data. They are not statements of fact and should not be considered definitive predictions.

**No Affiliation** - This project is not affiliated with, endorsed by, or connected to Tesla, Inc., or any other company mentioned. Company and product names are used for factual reference and comparison purposes only.

**Open Source** - Code is provided as-is under MIT License. Users are responsible for their own use of this tool and any decisions made based on its output.
