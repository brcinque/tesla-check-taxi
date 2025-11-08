# Tesla Robotaxi Monitor - Data Sources Implementation Guide

This document maps the comprehensive sources from `input/sources.txt` to the monitoring system implementation.

---

## ✅ Implemented Data Sources

### 1. **News Sentiment Analysis** 
**Source Reference:** sources.txt #6 - Crowdsourced & Real-World Data  
**Implementation:** `fetch_tesla_news()` in `real_data_monitor.py`

- **API:** News API (https://newsapi.org/)
- **Frequency:** Real-time (30-day rolling window)
- **Indicators Used:** News Sentiment, Safety Incidents, Regulatory Sentiment
- **Data Points:**
  - Article count and sentiment scoring
  - Regulatory mentions (NHTSA, investigations, recalls)
  - Safety mentions (crashes, accidents, deaths)
  - Recent headlines

**Setup:**
```bash
# Get free API key from https://newsapi.org/
cp config_template.py config.py
# Add your key to config.py:
NEWS_API_KEY = "your_key_here"
```

---

### 2. **SEC Insider Trading** ⚡ NEW!
**Source Reference:** sources.txt #8 - Financial Market Signals  
**Implementation:** `fetch_sec_insider_trading()` in `real_data_monitor.py`

- **API:** SEC Edgar API (free, no key required)
- **Frequency:** Real-time (90-day rolling window)
- **Indicators Used:** Insider Selling
- **Data Points:**
  - Form 4 filing count (last 90 days)
  - Activity level (HIGH/MODERATE/LOW)
  - Filing dates and patterns

**No Setup Required:** Works out of the box!

---

### 3. **NHTSA Safety Data** ⚡ NEW!
**Source Reference:** sources.txt #1 - Regulatory & Safety Data (Most Critical)  
**Implementation:** `fetch_nhtsa_investigations()` in `real_data_monitor.py`

- **API:** NHTSA ODI API (free, no key required)
- **Frequency:** Real-time
- **Indicators Used:** Regulatory Sentiment, Safety Incidents
- **Data Points:**
  - Vehicles tracked by NHTSA
  - Investigation status

**No Setup Required:** Works out of the box!

**Note:** Full NHTSA investigation details require manual checking at https://www.nhtsa.gov/

---

### 4. **Competitor Progress Tracking** ⚡ NEW!
**Source Reference:** sources.txt #5 - Competitive Intelligence  
**Implementation:** `fetch_competitor_progress()` in `real_data_monitor.py`

- **Source:** Industry reports & company disclosures
- **Frequency:** Updated as data becomes available
- **Indicators Used:** Competitor Progress
- **Companies Tracked:**
  - Waymo (4 cities, 150K+ weekly rides)
  - Baidu Apollo (11 cities, 60K+ weekly rides)
  - Cruise (suspended)
  - Tesla (0 cities, testing only)

**No Setup Required:** Uses publicly available data!

---

### 5. **Red Flag Scorecard** ⚡ NEW!
**Source Reference:** sources.txt #222-236 - RED FLAG SCORECARD  
**Implementation:** `calculate_red_flag_score()` in `real_data_monitor.py`

**Point System (Exit at 10+ points in 12 months):**
- ❌ NHTSA formal investigation: 3 points
- ❌ Fatal accident (FSD at fault): 5 points  
- ❌ Major regulatory denial: 4 points
- ✅ **Timeline pushback >1 year:** 2 points (ACTIVE)
- ✅ **Waymo expands to 10+ cities while Tesla <3:** 3 points (ACTIVE)
- ❌ Peer-reviewed safety study (negative): 5 points
- ❌ Class action wins: 3 points
- ❌ FSD version stagnation 6+ months: 2 points
- ❌ Key executive departures: 3 points each
- ❌ Guidehouse ranking drop below #5: 4 points

**Current Score:** 5/10 (MONITORING status)

---

## 🔄 Planned/Manual Data Sources

These sources from sources.txt require manual monitoring or future API integration:

### **California DMV Autonomous Vehicle Reports**
**Reference:** sources.txt #1 lines 20-27  
**URL:** https://www.dmv.ca.gov/portal/vehicle-industry-services/autonomous-vehicles/  
**Frequency:** Quarterly/Annually  
**Manual Action:** Check disengagement reports

### **Consumer Reports**
**Reference:** sources.txt #3 lines 64-68  
**URL:** https://www.consumerreports.org/  
**Frequency:** Semi-annually  
**Manual Action:** Review FSD testing results

### **Tesla Earnings Calls**
**Reference:** sources.txt #2 lines 39-50  
**URL:** https://ir.tesla.com/  
**Frequency:** Quarterly  
**Manual Action:** Listen for robotaxi timeline mentions

### **Guidehouse Insights AV Leaderboard**
**Reference:** sources.txt #4 lines 86-89  
**URL:** Guidehouse Insights reports (paid)  
**Frequency:** Annually (Q1)  
**Manual Action:** Check Tesla's ranking

### **YouTube FSD Test Channels**
**Reference:** sources.txt #6 lines 145-154  
**Channels:**
- AI DRIVR
- Whole Mars Catalog  
- Chuck Cook

**Frequency:** Monthly spot checks  
**Manual Action:** Watch recent test videos for failure patterns

---

## 📊 Data Source Status Dashboard

| Data Source | Status | API | Frequency | Cost |
|-------------|--------|-----|-----------|------|
| News Sentiment | ✅ Live | News API | Real-time | Free* |
| SEC Insider Trading | ✅ Live | SEC Edgar | Real-time | Free |
| NHTSA Safety | ✅ Live | NHTSA ODI | Real-time | Free |
| Competitor Progress | ✅ Static | Manual | Updated | Free |
| Red Flag Score | ✅ Active | Calculated | Real-time | Free |
| CA DMV Reports | 📅 Manual | None | Quarterly | Free |
| Consumer Reports | 📅 Manual | None | Semi-annual | Subscription |
| Tesla Earnings | 📅 Manual | None | Quarterly | Free |
| Guidehouse Ranking | 📅 Manual | None | Annual | Paid Report |
| YouTube Channels | 📅 Manual | None | Monthly | Free |

*News API: 100 requests/day on free tier

---

## 🚀 Quick Start Guide

### Minimum Setup (Works Immediately)
```bash
python3 tesla_robotaxi_monitor.py
```
**Gets you:**
- ✅ SEC insider trading data
- ✅ NHTSA safety checks
- ✅ Competitor progress tracking
- ✅ Red flag scoring
- ❌ Static news sentiment (no real-time)

### Enhanced Setup (Recommended)
```bash
# 1. Get News API key from https://newsapi.org/
# 2. Configure it
cp config_template.py config.py
nano config.py  # Add NEWS_API_KEY

# 3. Run monitor
python3 tesla_robotaxi_monitor.py
```
**Gets you:**
- ✅ Everything from Minimum Setup
- ✅ **Real-time news sentiment analysis**
- ✅ **Safety incident tracking from news**
- ✅ **Regulatory mention monitoring**

---

## 📈 Monitoring Schedule (from sources.txt)

### **Monthly Check (30 minutes)**
1. ✅ NHTSA data - Automated in system
2. ✅ Insider trading - Automated in system  
3. ✅ News sentiment - Automated (with API key)
4. 📅 Tesla subreddit/Twitter - Manual check
5. 📅 YouTube FSD channels - Watch 2-3 videos

### **Quarterly Deep Dive (2-3 hours)**
1. 📅 Tesla earnings call - Listen for timeline changes
2. 📅 Analyst reports - Read 2-3 objective sources
3. ✅ Competitive progress - Partially automated
4. 📅 DMV/regulatory filings - Check for new data
5. 📅 Academic research - Search for new studies

### **Annual Assessment**
1. 📅 Guidehouse AV leaderboard - Check Tesla's rank
2. 📅 Year-over-year FSD progress - Manual assessment
3. 📅 Regulatory environment - Review trends
4. ✅ Competitive landscape - Dashboard comparison

---

## 🎯 How Data Flows Through the System

```
┌─────────────────────────────────────────────┐
│         Real-Time Data Sources              │
├─────────────────────────────────────────────┤
│ • News API (with key)                       │
│ • SEC Edgar API (free)                      │
│ • NHTSA ODI API (free)                      │
│ • Competitor data (manual updates)          │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│      real_data_monitor.py                   │
│  (Fetches & processes raw data)             │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│    tesla_robotaxi_monitor.py                │
│  (Integrates data into 8 indicators)        │
├─────────────────────────────────────────────┤
│ 1. Regulatory Sentiment  ← NHTSA            │
│ 2. Safety Incidents      ← News + NHTSA     │
│ 3. Timeline Slippage     ← Static (manual)  │
│ 4. Competitor Progress   ← Competitor data  │
│ 5. Insider Selling       ← SEC Edgar        │
│ 6. News Sentiment        ← News API         │
│ 7. Technical Progress    ← Static (manual)  │
│ 8. Market Confidence     ← Static (manual)  │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│            Output                           │
├─────────────────────────────────────────────┤
│ • Dashboard (PNG)                           │
│ • Detailed Report (TXT)                     │
│ • Historical Data (JSON)                    │
└─────────────────────────────────────────────┘
```

---

## 🔮 Future Enhancements

Based on sources.txt, these could be added:

1. **YouTube API Integration** - Automated FSD test video analysis
2. **Reddit Sentiment Scraping** - r/SelfDrivingCars & r/TeslaMotors
3. **PACER Integration** - Track Tesla lawsuits automatically
4. **Options Market Data** - Put/call ratio tracking (requires trading platform)
5. **Tesla IR Scraper** - Parse earnings call transcripts for keywords
6. **CDS Pricing** - Track Tesla bond insurance costs

---

## 📚 Expert Sources to Follow (from sources.txt)

**Bearish but Data-Driven:**
- Gordon Johnson (GLJ Research) - @GordonJohnson19
- Toni Sacconaghi (Bernstein) - Via Bloomberg/CNBC

**Bullish but Honest:**
- Adam Jonas (Morgan Stanley) - Via research notes
- Dan Ives (Wedbush) - @DivesTech

**Independent/Academic:**
- Brad Templeton (Forbes) - brad.com/av
- Phil Koopman (CMU) - @PhilKoopman
- Missy Cummings (George Mason) - @missy_cummings

---

## ⚠️ Important Notes

1. **API Rate Limits:** News API free tier = 100 requests/day (1 run = 1 request)
2. **SEC API:** Requires proper User-Agent header (implemented)
3. **NHTSA API:** Can be slow/unreliable, has graceful fallback
4. **Data Accuracy:** Real-time data is current; static data needs manual updates
5. **No Financial Advice:** This is a monitoring tool, not investment advice

---

## 🆓 Free Access to Premium Sources

**See `FREE_ACCESS_GUIDE.md` for complete details!**

Quick tips for accessing paywalled sources ethically:

### Public Library (FREE)
Get a library card and access:
- Wall Street Journal
- Financial Times  
- Bloomberg
- Morningstar

### Your Brokerage (FREE)
Most accounts include:
- Professional analyst reports
- Morningstar, Argus, CFRA
- Reuters news feeds

### Government Sources (FREE)
- SEC Edgar (already automated!)
- NHTSA (already automated!)
- CA DMV reports

**Read `FREE_ACCESS_GUIDE.md` for full walkthrough!**

---

## 🔄 Keeping Data Current

### Automated (Every Run)
- News sentiment (last 30 days)
- SEC filings (last 90 days)
- NHTSA vehicle tracking
- Red flag scoring

### Manual Updates Needed
Update these in `real_data_monitor.py` as new information becomes available:

```python
# In fetch_competitor_progress()
competitors = {
    'Waymo': {'cities': 4, ...},  # Update when Waymo expands
    'Baidu Apollo': {'cities': 11, ...},  # Update quarterly
    ...
}

# In calculate_red_flag_score()
red_flags = {
    'nhtsa_investigation': {'points': 3, 'active': False},  # Update on news
    ...
}
```

---

**Last Updated:** November 8, 2025  
**Source Document:** input/sources.txt  
**Implementation:** v2.0 - Real-time data integration

