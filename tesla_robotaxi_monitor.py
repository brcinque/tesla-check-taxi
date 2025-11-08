#!/usr/bin/env python3
"""
Tesla Robotaxi Failure Indicator Dashboard
Monitors multiple signals to assess likelihood of Scenario 2 (robotaxi failure)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, Tuple
import warnings
import os
import json
warnings.filterwarnings('ignore')

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')
INPUT_DIR = os.path.join(SCRIPT_DIR, 'input')

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(INPUT_DIR, exist_ok=True)

# Set visual style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (16, 12)

class TeslaRobotaxiMonitor:
    def __init__(self):
        self.indicators = {
            'regulatory_sentiment': 0,
            'safety_incidents': 0,
            'timeline_slippage': 0,
            'competitor_progress': 0,
            'insider_selling': 0,
            'news_sentiment': 0,
            'technical_progress': 0,
            'market_confidence': 0
        }
        
        self.weights = {
            'regulatory_sentiment': 0.20,
            'safety_incidents': 0.20,
            'timeline_slippage': 0.15,
            'competitor_progress': 0.10,
            'insider_selling': 0.10,
            'news_sentiment': 0.10,
            'technical_progress': 0.10,
            'market_confidence': 0.05,
            'executive_departures': 0.00  # Red flag indicator, not weighted in main score
        }
        
        # Load configuration
        self.config = self._load_config()
        
        # Load historical data
        self.historical_scores = []
        self.dates = []
        self.history_file = os.path.join(OUTPUT_DIR, 'tesla_robotaxi_history.json')
        self._load_historical_data()
    
    def _load_config(self):
        """Load configuration from config.py if available"""
        try:
            import config
            return {
                'news_api_key': getattr(config, 'NEWS_API_KEY', None),
                'finnhub_api_key': getattr(config, 'FINNHUB_API_KEY', None),
                'risk_thresholds': getattr(config, 'RISK_THRESHOLDS', {
                    'low': 30, 'moderate': 50, 'high': 70, 'critical': 85
                })
            }
        except ImportError:
            print("ℹ️  No config.py found - using defaults (create from config_template.py for API features)")
            return {
                'news_api_key': None,
                'finnhub_api_key': None,
                'risk_thresholds': {'low': 30, 'moderate': 50, 'high': 70, 'critical': 85}
            }
    
    def _load_historical_data(self):
        """Load historical data from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.historical_scores = data.get('scores', [])
                    # Convert ISO format strings back to datetime objects
                    self.dates = [datetime.fromisoformat(d) for d in data.get('dates', [])]
                    print(f"✅ Loaded {len(self.historical_scores)} historical data points")
        except Exception as e:
            print(f"⚠️  Could not load historical data: {e}")
            self.historical_scores = []
            self.dates = []
    
    def _save_historical_data(self):
        """Save historical data to file"""
        try:
            data = {
                'scores': self.historical_scores,
                # Convert datetime objects to ISO format strings
                'dates': [d.isoformat() for d in self.dates],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Historical data saved to {os.path.basename(self.history_file)}")
        except Exception as e:
            print(f"⚠️  Could not save historical data: {e}")
        
    def check_regulatory_sentiment(self) -> Tuple[float, str]:
        """Monitor regulatory environment"""
        score = 55
        
        # Try to get real NHTSA data
        try:
            from real_data_monitor import fetch_nhtsa_investigations
            nhtsa_data = fetch_nhtsa_investigations()
            
            if 'error' not in nhtsa_data:
                details = f"""
        Recent Regulatory Signals (REAL DATA):
        • NHTSA: {nhtsa_data.get('vehicles_tracked', 'N/A')} Tesla vehicles tracked
        • Source: {nhtsa_data.get('source', 'Unknown')}
        • Last check: {nhtsa_data.get('check_date', 'Unknown')}
        • California DMV: No new autonomous permits issued to Tesla (NEGATIVE)
        • Texas: Favorable testing environment continues (POSITIVE)
        • Federal: No new framework legislation (NEUTRAL)
        
        Score: {score}/100 (Below 50 is concerning)
        
        Note: {nhtsa_data.get('note', '')}
        """
                return score, details
        except Exception as e:
            print(f"⚠️  Could not fetch NHTSA data: {e}")
        
        # Fallback to default
        details = f"""
        Recent Regulatory Signals:
        • NHTSA: Ongoing investigation into FSD crashes (NEGATIVE)
        • California DMV: No new autonomous permits issued to Tesla (NEGATIVE)
        • Texas: Favorable testing environment continues (POSITIVE)
        • Federal: No new framework legislation (NEUTRAL)
        
        Score: {score}/100 (Below 50 is concerning)
        """
        return score, details
    
    def check_safety_incidents(self) -> Tuple[float, str]:
        """Track safety incidents and accident rates - NOW WITH NHTSA CRASH DATA (TIER 1)"""
        score = 65
        safety_mentions = 0
        
        # Get NHTSA crash data (TIER 1 - Nationwide)
        nhtsa_section = ""
        try:
            from real_data_monitor import fetch_nhtsa_crash_data
            crash_data = fetch_nhtsa_crash_data()
            
            if 'error' not in crash_data:
                companies = crash_data.get('companies', {})
                tesla = companies.get('Tesla', {})
                waymo = companies.get('Waymo', {})
                
                # Adjust score based on crash data
                tesla_crashes = tesla.get('total_crashes', 0)
                tesla_fatalities = tesla.get('fatalities', 0)
                
                if tesla_fatalities > 3:
                    score = max(30, score - 20)
                elif tesla_crashes > 500:
                    score = max(40, score - 15)
                elif tesla_crashes > 100:
                    score = max(50, score - 10)
                
                nhtsa_section = f"""
        
        NHTSA CRASH DATA (TIER 1 - Nationwide, 12 months):
        • Tesla: {tesla_crashes} crashes, {tesla.get('serious_injury', 0)} serious injuries, {tesla_fatalities} fatalities
        • Waymo: {waymo.get('total_crashes', 0)} crashes, {waymo.get('serious_injury', 0)} serious injuries, {waymo.get('fatalities', 0)} fatalities
        • Cruise: {companies.get('Cruise', {}).get('total_crashes', 0)} crashes (permit suspended)
        
        KEY FINDINGS:
        • {crash_data['analysis']['tesla_concerns']}
        • {crash_data['analysis']['severity_comparison']}
        • {crash_data['analysis']['regulatory_action']}
        
        Note: {crash_data.get('note', '')}
        """
        except Exception as e:
            print(f"⚠️  Could not fetch NHTSA crash data: {e}")
        
        # Try to get real news data for safety mentions
        if self.config.get('news_api_key'):
            try:
                from real_data_monitor import fetch_tesla_news
                news_data = fetch_tesla_news(self.config['news_api_key'])
                
                if 'error' not in news_data:
                    safety_mentions = news_data.get('safety_mentions', 0)
                    
                    # Adjust score based on news mentions (less weight since we have NHTSA)
                    if safety_mentions > 15:
                        score = max(30, score - 10)
                    elif safety_mentions > 10:
                        score = max(50, score - 5)
                    
                    details = f"""
        Safety Incident Analysis (REAL DATA - ENHANCED):
        {nhtsa_section}
        
        NEWS MONITORING (Last 30 days):
        • Safety/crash article mentions: {safety_mentions}
        • Monitoring status: {"HIGH CONCERN" if safety_mentions > 10 else "MODERATE" if safety_mentions > 5 else "LOW"}
        
        Score: {score}/100 (Below 60 suggests serious problems)
        """
                    return score, details
            except Exception as e:
                print(f"⚠️  Could not enhance safety data: {e}")
        
        # If we have NHTSA but no news
        if nhtsa_section:
            details = f"""
        Safety Incident Analysis (REAL DATA - NHTSA):
        {nhtsa_section}
        
        Score: {score}/100 (Below 60 suggests serious problems)
        """
            return score, details
        
        # Fallback to default
        details = f"""
        Safety Incident Analysis (Last 6 months):
        • Fatal crashes involving FSD: 2 reported (HIGH CONCERN)
        • Injury crashes: 15 reported (MODERATE)
        • Property damage only: 45+ reported (TRACKING)
        • Rate vs human drivers: Insufficient data (UNKNOWN)
        • High-profile incidents: 1 viral video (PR DAMAGE)
        
        Score: {score}/100 (Below 60 suggests serious problems)
        """
        return score, details
    
    def check_timeline_slippage(self) -> Tuple[float, str]:
        """Track Musk's robotaxi promises vs reality - NOW WITH EARNINGS CALL TRACKING"""
        timeline_history = [
            ("2015", "Full autonomy in 2 years", "MISSED"),
            ("2016", "Autonomous coast-to-coast drive by end of 2017", "MISSED"),
            ("2019", "Robotaxis by 2020", "MISSED"),
            ("2021", "FSD feature complete by end of year", "MISSED"),
            ("2022", "Wide release FSD Beta", "PARTIALLY MET"),
            ("2023", "Unsupervised FSD this year", "MISSED"),
            ("2024", "Robotaxi reveal and 2025 deployment", "DELAYED"),
            ("2025", "Cybercab production 2026/2027", "TBD")
        ]
        
        missed_count = sum(1 for _, _, status in timeline_history if status == "MISSED")
        total_predictions = len(timeline_history)
        
        score = max(0, 100 - (missed_count / total_predictions * 100))
        
        # Try to get earnings call timeline data
        earnings_info = ""
        try:
            from real_data_monitor import fetch_earnings_timeline_data
            if self.config.get('news_api_key'):
                earnings_data = fetch_earnings_timeline_data(self.config['news_api_key'])
                
                if 'error' not in earnings_data:
                    delay_mentions = earnings_data.get('delay_mentions', 0)
                    new_promises = earnings_data.get('new_promises', 0)
                    credibility_concern = earnings_data.get('credibility_concern', False)
                    
                    # Adjust score based on earnings data
                    if credibility_concern:
                        score = max(0, score - 10)
                    if delay_mentions > 3:
                        score = max(0, score - 5)
                    
                    earnings_info = f"""
        
        RECENT EARNINGS CALL TRACKING (Last 120 days):
        • Articles mentioning timeline: {earnings_data.get('total_articles', 0)}
        • Delay mentions: {delay_mentions}
        • New promises made: {new_promises}
        • Credibility concern: {'YES' if credibility_concern else 'NO'}
        """
        except Exception as e:
            print(f"⚠️  Could not fetch earnings data: {e}")
        
        details = f"""
        Timeline Credibility Analysis:
        • Total predictions tracked: {total_predictions}
        • Predictions missed: {missed_count}
        • Current status: "2026/2027 production" (already delayed from 2025)
        • Pattern: Consistent 2-3 year delays on all major milestones
        {earnings_info}
        
        Track Record Score: {score:.1f}/100
        
        🚨 RED FLAG: After 10 years of promises, zero cities with unsupervised robotaxis
        """
        return score, details
    
    def check_competitor_progress(self) -> Tuple[float, str]:
        """Compare Tesla to competitors - NOW WITH DMV DISENGAGEMENT DATA (TIER 2)"""
        score = 25
        
        # Try to get real competitor data
        try:
            from real_data_monitor import fetch_competitor_progress, fetch_ca_dmv_disengagement_data
            comp_data = fetch_competitor_progress()
            dmv_data = fetch_ca_dmv_disengagement_data()
            
            if 'error' not in comp_data:
                competitors = comp_data.get('competitors', {})
                
                # Build DMV section
                dmv_section = ""
                if 'error' not in dmv_data:
                    companies = dmv_data.get('companies', {})
                    dmv_section = f"""
        
        CA DMV DISENGAGEMENT DATA (2023 Report):
        • Waymo: {companies['Waymo']['miles_driven']:,} miles, {companies['Waymo']['disengagements']} disengagements
          → {companies['Waymo']['miles_per_disengagement']:,} miles per disengagement (LEADER)
        • Cruise: {companies['Cruise']['miles_driven']:,} miles, {companies['Cruise']['disengagements']:,} disengagements
          → {companies['Cruise']['miles_per_disengagement']:,} miles per disengagement
        • Tesla: {companies['Tesla']['status']}
          → {companies['Tesla']['note']}
        
        GAP ANALYSIS:
        • {dmv_data['gap_analysis']['waymo_vs_tesla']}
        • {dmv_data['gap_analysis']['safety_gap']}
        • 🚨 {dmv_data['gap_analysis']['concern']}
        """
                
                details = f"""
        Competitive Position Analysis (REAL DATA + DMV):
        
        OPERATIONAL ROBOTAXIS TODAY:
        • Waymo: {competitors['Waymo']['cities']} cities, {competitors['Waymo']['weekly_rides']} weekly rides, {competitors['Waymo']['status']}
        • Baidu Apollo: {competitors['Baidu Apollo']['cities']} cities (China), {competitors['Baidu Apollo']['weekly_rides']} weekly rides, {competitors['Baidu Apollo']['status']}
        • Cruise: {competitors['Cruise']['cities']} cities, {competitors['Cruise']['weekly_rides']} weekly rides, {competitors['Cruise']['status']}
        • Tesla: {competitors['Tesla']['cities']} cities, {competitors['Tesla']['weekly_rides']} weekly rides, {competitors['Tesla']['status']}
        {dmv_section}
        
        Tesla Ranking: {comp_data.get('tesla_rank', 'UNKNOWN')}
        Gap Assessment: {comp_data.get('gap_assessment', 'Unknown')}
        """
                
                # Add CPUC deployment data (TIER 1)
                cpuc_section = ""
                try:
                    from real_data_monitor import fetch_cpuc_deployment_data
                    cpuc_data = fetch_cpuc_deployment_data()
                    
                    if 'error' not in cpuc_data:
                        companies_cpuc = cpuc_data.get('companies', {})
                        waymo_cpuc = companies_cpuc.get('Waymo', {})
                        tesla_cpuc = companies_cpuc.get('Tesla', {})
                        
                        cpuc_section = f"""
        
        CPUC COMMERCIAL DEPLOYMENT (TIER 1 - 2024 Q3):
        • Waymo: {waymo_cpuc.get('commercial_status', 'N/A')} - {waymo_cpuc.get('weekly_rides', 'N/A')} weekly rides
          Fleet: {waymo_cpuc.get('fleet_size', 'N/A')} | Area: {waymo_cpuc.get('service_area', 'N/A')}
        • Tesla: {tesla_cpuc.get('commercial_status', 'N/A')} - {tesla_cpuc.get('weekly_rides', 'N/A')} rides
          {tesla_cpuc.get('notes', '')}
        
        KEY FINDING:
        • {cpuc_data['key_findings']['gap']}
        • {cpuc_data['key_findings']['regulatory']}
        """
                except Exception as e:
                    print(f"⚠️  Could not fetch CPUC deployment data: {e}")
                
                details += cpuc_section + f"""
        
        Score: {score}/100 (Tesla is 5+ years behind in deployment)
        
        🚨 CRITICAL: Competitors have actual robotaxis operating TODAY
        Source: {comp_data.get('source', 'Unknown')} + CA DMV + CPUC
        """
                return score, details
        except Exception as e:
            print(f"⚠️  Could not fetch competitor data: {e}")
        
        # Fallback to default
        details = f"""
        Competitive Position Analysis:
        
        OPERATIONAL ROBOTAXIS TODAY:
        • Waymo: 4 cities, 150K+ weekly rides, FULLY DRIVERLESS
        • Baidu: 11 cities (China), 60K+ weekly rides, FULLY DRIVERLESS
        • Tesla: 0 cities, 0 rides, SUPERVISED ONLY
        
        Score: {score}/100 (Tesla is 5+ years behind in deployment)
        
        🚨 CRITICAL: Competitors have actual robotaxis operating TODAY
        """
        return score, details
    
    def check_insider_selling(self) -> Tuple[float, str]:
        """Monitor insider trading patterns"""
        score = 40
        
        # Try to get real SEC insider trading data
        try:
            from real_data_monitor import fetch_sec_insider_trading
            insider_data = fetch_sec_insider_trading()
            
            if 'error' not in insider_data:
                filings = insider_data.get('insider_filings_90d', 0)
                activity = insider_data.get('activity_level', 'UNKNOWN')
                
                # Adjust score based on filing activity
                if activity == 'HIGH':
                    score = max(25, score - 15)
                elif activity == 'MODERATE':
                    score = max(35, score - 5)
                
                details = f"""
        Insider Trading Analysis (REAL DATA):
        
        • SEC Form 4 filings (last 90 days): {filings}
        • Activity level: {activity}
        • Source: {insider_data.get('source', 'Unknown')}
        • Last check: {insider_data.get('last_check', 'Unknown')}
        
        BACKGROUND:
        • Elon Musk: $10B+ in stock sales (reported)
        • Executive team: Net selling across board
        • No significant insider purchases in 12 months
        
        Score: {score}/100 (Below 50 suggests insiders not confident)
        
        ⚠️ NOTE: Heavy insider selling often precedes negative developments
        📊 Current filing rate: {"CONCERNING" if activity == "HIGH" else "MODERATE" if activity == "MODERATE" else "NORMAL"}
        """
                return score, details
        except Exception as e:
            print(f"⚠️  Could not fetch SEC data: {e}")
        
        # Fallback to default
        details = f"""
        Insider Trading Analysis (Last 6 months):
        
        • Elon Musk: $10B+ in stock sales
        • Executive team: Net selling across board
        • No significant insider purchases in 12 months
        
        Score: {score}/100 (Below 50 suggests insiders not confident)
        
        ⚠️ NOTE: Heavy insider selling often precedes negative developments
        """
        return score, details
    
    def check_news_sentiment(self) -> Tuple[float, str]:
        """Analyze news sentiment"""
        # Try to fetch real data if API key is available
        if self.config.get('news_api_key'):
            try:
                from real_data_monitor import fetch_tesla_news
                news_data = fetch_tesla_news(self.config['news_api_key'])
                
                if 'error' not in news_data:
                    # Convert sentiment to score
                    sentiment_score = news_data.get('sentiment_score', 0)
                    # Normalize to 0-100 scale (assuming sentiment_score ranges from -30 to +30)
                    score = max(0, min(100, 50 + sentiment_score * 1.5))
                    
                    details = f"""
        News Sentiment Analysis (30-day rolling - REAL DATA):
        
        • Total articles analyzed: {news_data.get('total', 0)}
        • Sentiment: {news_data.get('sentiment', 'UNKNOWN')}
        • Raw sentiment score: {sentiment_score}
        
        Recent headlines:
        """
                    for i, article in enumerate(news_data.get('articles', [])[:3], 1):
                        details += f"\n        {i}. {article.get('title', 'N/A')}"
                    
                    details += f"""
        
        Sentiment Score: {score:.0f}/100 (Based on real news data)
        """
                    return score, details
                else:
                    print(f"⚠️  News API error: {news_data['error']}")
            except Exception as e:
                print(f"⚠️  Could not fetch real news data: {e}")
        
        # Fallback to default score if no API key or error
        score = 50
        details = f"""
        News Sentiment Analysis (30-day rolling - DEFAULT):
        
        POSITIVE: FSD improvements, technological optimism
        NEGATIVE: Crash investigations, competitor advances, skepticism
        NEUTRAL: Timeline questions, analytical pieces
        
        Sentiment Score: {score}/100 (Mixed, trending negative)
        
        ℹ️  Add NEWS_API_KEY to config.py for real-time news analysis
        """
        return score, details
    
    def check_technical_progress(self) -> Tuple[float, str]:
        """Evaluate FSD capability improvements"""
        score = 60
        
        details = f"""
        Technical Progress Assessment:
        
        CAPABILITIES TODAY:
        ✓ Highway driving (mostly reliable)
        ✓ Simple intersections (good)
        ✗ Complex urban environments (struggles)
        ✗ Adverse weather (poor)
        ✗ Construction zones (unreliable)
        
        Score: {score}/100 (Progress continuing but slowing)
        
        ⚠️ CONCERN: Improvement rate insufficient to meet 2026-2027 timeline
        """
        return score, details
    
    def check_executive_departures(self) -> Tuple[int, str]:
        """Track executive departures - TIER 1 FEATURE"""
        red_flag_points = 0
        
        # Try to get real executive departure data
        try:
            from real_data_monitor import fetch_executive_departures
            if self.config.get('news_api_key'):
                exec_data = fetch_executive_departures(self.config['news_api_key'])
                
                if 'error' not in exec_data:
                    departures = exec_data.get('potential_departures', 0)
                    recent = exec_data.get('recent_departures', [])
                    
                    # Red flag: 3 points per key executive departure
                    red_flag_points = departures * 3
                    
                    recent_list = "\n".join([f"        • {d['title']}" for d in recent[:3]])
                    
                    details = f"""
        Executive Departure Tracking (Last 90 days):
        
        • Total potential departures detected: {departures}
        • Recent departures (key roles):
{recent_list if recent_list else '        (None detected)'}
        
        RED FLAG POINTS: {red_flag_points} ({departures} departures × 3 points)
        
        {'🚨 WARNING: Key personnel leaving' if departures > 0 else '✅ No major departures detected'}
        Source: News API (Real-time tracking)
        """
                    return red_flag_points, details
        except Exception as e:
            print(f"⚠️  Could not fetch executive departure data: {e}")
        
        # Fallback
        details = """
        Executive Departure Tracking:
        
        • No automated tracking available
        • Add NEWS_API_KEY to config.py for real-time monitoring
        
        RED FLAG POINTS: 0 (Manual tracking required)
        """
        return 0, details
    
    def check_market_confidence(self) -> Tuple[float, str]:
        """Analyze options market and analyst sentiment - NOW WITH PRICE TARGET TRACKING (TIER 2)"""
        score = 55
        
        # Try to get real Finnhub data
        if self.config.get('finnhub_api_key'):
            try:
                from real_data_monitor import fetch_finnhub_data
                finnhub_data = fetch_finnhub_data(self.config['finnhub_api_key'])
                
                if 'error' not in finnhub_data:
                    # Calculate analyst sentiment score
                    strong_buy = finnhub_data.get('analyst_strong_buy', 0)
                    buy = finnhub_data.get('analyst_buy', 0)
                    hold = finnhub_data.get('analyst_hold', 0)
                    sell = finnhub_data.get('analyst_sell', 0)
                    strong_sell = finnhub_data.get('analyst_strong_sell', 0)
                    
                    total = strong_buy + buy + hold + sell + strong_sell
                    if total > 0:
                        # Weight: StrongBuy=1.0, Buy=0.75, Hold=0.5, Sell=0.25, StrongSell=0
                        weighted_score = ((strong_buy * 1.0 + buy * 0.75 + hold * 0.5 + sell * 0.25) / total) * 100
                        score = max(30, min(80, weighted_score))
                    
                    price = finnhub_data.get('current_price', 'N/A')
                    change = finnhub_data.get('percent_change', 'N/A')
                    
                    details = f"""
        Market Confidence Indicators (REAL DATA - Finnhub):
        
        CURRENT PRICE: ${price} ({change:+.2f}% today)
        
        ANALYST RATINGS (Latest):
        • Strong Buy: {strong_buy}
        • Buy: {buy}
        • Hold: {hold}
        • Sell: {sell}
        • Strong Sell: {strong_sell}
        • Total Analysts: {total}
        
        MARKET DATA:
        • Day High: ${finnhub_data.get('high', 'N/A')}
        • Day Low: ${finnhub_data.get('low', 'N/A')}
        • Market Cap: ${finnhub_data.get('market_cap', 'N/A')}B
        • Beta: {finnhub_data.get('beta', 'N/A')}
        • P/E Ratio: {finnhub_data.get('pe_ratio', 'N/A')}
        • 52-Week High: ${finnhub_data.get('price_target_high', 'N/A')}
        • 52-Week Low: ${finnhub_data.get('price_target_low', 'N/A')}
        • Short Interest: {finnhub_data.get('short_percent', 'N/A')}%
        • Next Earnings: {finnhub_data.get('next_earnings', 'N/A')}
        """
                    
                    # Add price target data (TIER 2)
                    price_target_section = ""
                    try:
                        from real_data_monitor import fetch_price_target_tracking
                        if self.config.get('finnhub_api_key'):
                            pt_data = fetch_price_target_tracking(self.config['finnhub_api_key'])
                            
                            if 'error' not in pt_data:
                                # Adjust score based on price target consensus
                                upside = pt_data.get('upside_percent', 0)
                                if upside < -10:  # Trading >10% above target
                                    score = max(30, score - 15)
                                elif upside > 20:  # Trading >20% below target
                                    score = min(80, score + 10)
                                
                                price_target_section = f"""
        
        PRICE TARGET ANALYSIS (TIER 2):
        • Target High: ${pt_data.get('target_high', 'N/A')}
        • Target Mean: ${pt_data.get('target_mean', 'N/A')}
        • Target Low: ${pt_data.get('target_low', 'N/A')}
        • Upside/Downside: {pt_data.get('upside_percent', 0):+.1f}% ({pt_data.get('consensus', 'N/A')})
        • Recent Changes (3mo): {pt_data.get('upgrades_3m', 0)} upgrades, {pt_data.get('downgrades_3m', 0)} downgrades
        • Trend: {pt_data.get('trend_icon', '')} {pt_data.get('trend', 'NEUTRAL')}
        """
                    except Exception as e:
                        print(f"⚠️  Could not fetch price target data: {e}")
                    
                    details += price_target_section
                    details += f"""
        
        Score: {score:.0f}/100 (Based on analysts + price targets + short interest)
        Source: Finnhub API - ENHANCED DATA + TIER 2
        """
                    return score, details
            except Exception as e:
                print(f"⚠️  Could not fetch Finnhub data: {e}")
        
        # Fallback to default
        details = f"""
        Market Confidence Indicators:
        
        ANALYST RATINGS: 45% Buy, 40% Hold, 15% Sell
        AVERAGE PRICE TARGET: $420 (below current)
        OPTIONS MARKET: Elevated volatility, uncertainty priced in
        
        Score: {score}/100 (Market is uncertain, not convinced)
        
        ℹ️  Add FINNHUB_API_KEY to config.py for real-time market data
        """
        return score, details
    
    def calculate_failure_risk_score(self) -> Dict:
        """Calculate overall failure risk score"""
        print("🔍 SCANNING TESLA ROBOTAXI INDICATORS...\n")
        print("="*80)
        
        results = {}
        total_score = 0
        
        checks = [
            ('regulatory_sentiment', self.check_regulatory_sentiment),
            ('safety_incidents', self.check_safety_incidents),
            ('timeline_slippage', self.check_timeline_slippage),
            ('competitor_progress', self.check_competitor_progress),
            ('insider_selling', self.check_insider_selling),
            ('news_sentiment', self.check_news_sentiment),
            ('technical_progress', self.check_technical_progress),
            ('market_confidence', self.check_market_confidence),
            ('executive_departures', self.check_executive_departures)
        ]
        
        for indicator_name, check_func in checks:
            score, details = check_func()
            self.indicators[indicator_name] = score
            weighted_score = score * self.weights[indicator_name]
            total_score += weighted_score
            
            results[indicator_name] = {
                'score': score,
                'weighted_score': weighted_score,
                'weight': self.weights[indicator_name],
                'details': details
            }
            
            print(f"\n📊 {indicator_name.replace('_', ' ').title()}")
            print(f"   Raw Score: {score:.1f}/100")
            print(f"   Weighted: {weighted_score:.2f}")
            print("-"*80)
        
        success_score = total_score
        failure_risk = 100 - success_score
        
        results['overall'] = {
            'success_score': success_score,
            'failure_risk': failure_risk,
            'timestamp': datetime.now()
        }
        
        self.historical_scores.append(success_score)
        self.dates.append(datetime.now())
        
        return results
    
    def visualize_dashboard(self, results: Dict):
        """Create comprehensive visual dashboard"""
        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, :])
        self._plot_overall_gauge(ax1, results['overall'])
        
        ax2 = fig.add_subplot(gs[1, :2])
        self._plot_indicator_breakdown(ax2, results)
        
        ax3 = fig.add_subplot(gs[1, 2])
        self._plot_risk_level(ax3, results['overall']['failure_risk'])
        
        ax4 = fig.add_subplot(gs[2, 0])
        self._plot_weighted_contribution(ax4, results)
        
        ax5 = fig.add_subplot(gs[2, 1:])
        self._plot_time_series(ax5)
        
        # Save dashboard with error handling
        try:
            output_path = os.path.join(OUTPUT_DIR, 'tesla_robotaxi_dashboard.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
            print("\n" + "="*80)
            print(f"📈 DASHBOARD SAVED: {output_path}")
            print("="*80)
        except Exception as e:
            print(f"\n❌ ERROR saving dashboard: {e}")
            print("="*80)
        
        return fig
    
    def _plot_overall_gauge(self, ax, overall_data):
        """Plot main gauge"""
        success_score = overall_data['success_score']
        failure_risk = overall_data['failure_risk']
        
        if success_score >= 70:
            color, status, emoji = 'green', "ON TRACK", "✅"
        elif success_score >= 50:
            color, status, emoji = 'yellow', "CONCERNING", "⚠️"
        elif success_score >= 30:
            color, status, emoji = 'orange', "HIGH RISK", "🔶"
        else:
            color, status, emoji = 'red', "FAILING", "🚨"
        
        ax.barh([0], [success_score], color=color, height=0.5, alpha=0.7)
        ax.barh([0], [100-success_score], left=success_score, color='lightgray', height=0.5, alpha=0.3)
        
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel('Score', fontsize=12, fontweight='bold')
        ax.set_yticks([])
        
        ax.axvline(30, color='red', linestyle='--', alpha=0.5, linewidth=2)
        ax.axvline(50, color='orange', linestyle='--', alpha=0.5, linewidth=2)
        ax.axvline(70, color='green', linestyle='--', alpha=0.5, linewidth=2)
        
        ax.text(success_score/2, 0, f'{emoji}\n{success_score:.1f}', 
               ha='center', va='center', fontsize=24, fontweight='bold')
        
        ax.set_title(f'TESLA ROBOTAXI SUCCESS INDICATOR: {status}\n' +
                    f'Failure Risk: {failure_risk:.1f}% | Success Probability: {success_score:.1f}%',
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.grid(True, alpha=0.3)
    
    def _plot_indicator_breakdown(self, ax, results):
        """Plot individual indicators"""
        indicators = [k for k in results.keys() if k != 'overall']
        scores = [results[k]['score'] for k in indicators]
        colors = ['green' if s >= 70 else 'yellow' if s >= 50 else 'orange' if s >= 30 else 'red' 
                 for s in scores]
        
        y_pos = np.arange(len(indicators))
        bars = ax.barh(y_pos, scores, color=colors, alpha=0.7)
        
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 2, i, f'{score:.0f}', va='center', fontweight='bold')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels([i.replace('_', ' ').title() for i in indicators], fontsize=10)
        ax.set_xlabel('Score (0-100)', fontsize=11, fontweight='bold')
        ax.set_title('Individual Indicator Scores', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 105)
        ax.axvline(50, color='black', linestyle='--', alpha=0.3)
        ax.grid(True, alpha=0.3, axis='x')
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.7, label='Strong (70+)'),
            Patch(facecolor='yellow', alpha=0.7, label='Moderate (50-69)'),
            Patch(facecolor='orange', alpha=0.7, label='Weak (30-49)'),
            Patch(facecolor='red', alpha=0.7, label='Critical (<30)')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
    
    def _plot_risk_level(self, ax, failure_risk):
        """Plot risk gauge"""
        theta = np.linspace(0, np.pi, 100)
        
        ax.fill_between(theta[0:33], 0, 1, color='green', alpha=0.3)
        ax.fill_between(theta[33:66], 0, 1, color='yellow', alpha=0.3)
        ax.fill_between(theta[66:], 0, 1, color='red', alpha=0.3)
        
        risk_angle = np.pi * (1 - failure_risk/100)
        ax.plot([0, np.cos(risk_angle)], [0, np.sin(risk_angle)], 'k-', linewidth=4)
        ax.plot(0, 0, 'ko', markersize=12)
        
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.1, 1.2)
        ax.axis('off')
        ax.set_title(f'Failure Risk Level\n{failure_risk:.0f}%', 
                    fontsize=12, fontweight='bold')
        
        ax.text(-0.9, 0.5, 'LOW', fontsize=10, color='green', fontweight='bold')
        ax.text(0, 1.1, 'MED', fontsize=10, color='orange', fontweight='bold')
        ax.text(0.9, 0.5, 'HIGH', fontsize=10, color='red', fontweight='bold')
    
    def _plot_weighted_contribution(self, ax, results):
        """Plot weighted contributions"""
        indicators = [k for k in results.keys() if k != 'overall']
        weighted_scores = [results[k]['weighted_score'] for k in indicators]
        labels = [k.replace('_', ' ').title() for k in indicators]
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(indicators)))
        
        wedges, texts, autotexts = ax.pie(weighted_scores, labels=labels, autopct='%1.1f%%',
                                           colors=colors, startangle=90)
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')
        
        for text in texts:
            text.set_fontsize(8)
        
        ax.set_title('Weighted Contribution\nto Overall Score', fontsize=11, fontweight='bold')
    
    def _plot_time_series(self, ax):
        """Plot enhanced historical trend - TIER 1 IMPROVEMENT"""
        if len(self.historical_scores) > 1:
            # Plot main trend line with better styling
            ax.plot(self.dates, self.historical_scores, marker='o', linewidth=2.5, 
                   markersize=10, color='#2E86DE', label='Success Score', zorder=3)
            
            # Add risk zones with subtle shading
            ax.axhspan(70, 100, alpha=0.1, color='green')
            ax.axhspan(50, 70, alpha=0.1, color='yellow')
            ax.axhspan(30, 50, alpha=0.1, color='orange')
            ax.axhspan(0, 30, alpha=0.1, color='red')
            
            # Risk level lines
            ax.axhline(70, color='green', linestyle='--', alpha=0.6, linewidth=1.5, label='Low Risk')
            ax.axhline(50, color='orange', linestyle='--', alpha=0.6, linewidth=1.5, label='Moderate')
            ax.axhline(30, color='red', linestyle='--', alpha=0.6, linewidth=1.5, label='Critical')
            
            # Add trend indicator
            if len(self.historical_scores) >= 2:
                trend = self.historical_scores[-1] - self.historical_scores[-2]
                trend_text = f"Trend: {'↑' if trend > 0 else '↓'} {abs(trend):.1f} pts"
                trend_color = 'green' if trend > 0 else 'red'
                ax.text(0.02, 0.98, trend_text, transform=ax.transAxes, 
                       fontsize=10, va='top', ha='left', fontweight='bold',
                       bbox=dict(boxstyle='round', facecolor=trend_color, alpha=0.2))
            
            ax.set_ylabel('Success Score', fontsize=11, fontweight='bold')
            ax.set_xlabel('Date', fontsize=11, fontweight='bold')
            ax.set_title('📈 Historical Trend Analysis', fontsize=12, fontweight='bold')
            ax.set_ylim(0, 100)
            ax.legend(fontsize=9, loc='best')
            ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, fontsize=9)
        else:
            ax.text(0.5, 0.5, '📊 Run Multiple Times\n\nNeed 2+ data points for trend analysis', 
                   ha='center', va='center', fontsize=12, style='italic',
                   bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.2))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.set_title('Historical Trend (Need More Data)', fontsize=12, fontweight='bold')
    
    def generate_html_dashboard(self, results: Dict):
        """Generate interactive HTML dashboard"""
        html_path = os.path.join(OUTPUT_DIR, 'tesla_robotaxi_dashboard.html')
        
        try:
            overall = results['overall']
            success_score = overall['success_score']
            failure_risk = overall['failure_risk']
            
            # Determine status and color
            if failure_risk >= 70:
                status = "CRITICAL"
                status_color = "#dc3545"
                status_icon = "🚨"
                recommendation = "Consider exit strategy"
            elif failure_risk >= 50:
                status = "HIGH RISK"
                status_color = "#ffc107"
                status_icon = "⚠️"
                recommendation = "Review position sizing"
            elif failure_risk >= 30:
                status = "MODERATE RISK"
                status_color = "#ff8c00"
                status_icon = "🔶"
                recommendation = "Stay vigilant"
            else:
                status = "LOW RISK"
                status_color = "#28a745"
                status_icon = "✅"
                recommendation = "Continue monitoring"
            
            # Load goals from input directory
            goals_html = ""
            goals_path = os.path.join(INPUT_DIR, 'goals.txt')
            if os.path.exists(goals_path):
                try:
                    # Calculate current progress based on monitoring data
                    current_year = 2024
                    target_year_1_2 = "2026-2027"
                    
                    # Assess current state against Year 1-2 goals
                    regulatory_status = "❌ No Approvals" if results.get('regulatory_sentiment', {}).get('score', 100) > 60 else "⚠️ Unclear"
                    service_status = "❌ Not Operational" if results.get('competitor_progress', {}).get('score', 100) > 70 else "⚠️ Testing"
                    fleet_status = "❌ 0 Vehicles (Goal: 5,000-10,000)"
                    
                    # Check CPUC data for actual deployment
                    try:
                        from real_data_monitor import fetch_cpuc_deployment_data
                        cpuc_check = fetch_cpuc_deployment_data()
                        tesla_deploy = cpuc_check.get('companies', {}).get('Tesla', {})
                        if tesla_deploy.get('commercial_status') == "No permit":
                            service_status = "❌ No Commercial Permit"
                    except:
                        pass
                    
                    # Calculate overall progress percentage (LOW scores = GOOD progress)
                    progress_pct = 0
                    # Technical Progress (low score = good tech)
                    tech_score = results.get('technical_progress', {}).get('score', 100)
                    if tech_score < 30:
                        progress_pct += 15
                    
                    # Regulatory (low score = good regulatory standing)
                    reg_score = results.get('regulatory_sentiment', {}).get('score', 100)
                    if reg_score < 40:
                        progress_pct += 20
                    
                    # Competitor Progress (low score = we're ahead)
                    comp_score = results.get('competitor_progress', {}).get('score', 100)
                    if comp_score < 40:
                        progress_pct += 25
                    
                    # Safety (low score = good safety record)
                    safety_score = results.get('safety_incidents', {}).get('score', 100)
                    if safety_score < 30:
                        progress_pct += 20
                    
                    # Timeline (low score = on schedule)
                    timeline_score = results.get('timeline_slippage', {}).get('score', 100)
                    if timeline_score < 40:
                        progress_pct += 20
                    
                    # Determine current phase
                    if progress_pct < 25:
                        current_phase = "Pre-Launch"
                        phase_desc = "Early development, no commercial deployment"
                    elif progress_pct < 50:
                        current_phase = "Testing Phase"
                        phase_desc = "Technology testing, regulatory preparation"
                    elif progress_pct < 75:
                        current_phase = "Limited Launch"
                        phase_desc = "Initial deployment in select markets"
                    else:
                        current_phase = "Scaling Phase"
                        phase_desc = "Multi-market expansion underway"
                    
                    goals_html = f"""
                <div class="indicator-card journey-card">
                    <div class="indicator-header">
                        <h3>🗺️ Robotaxi Journey Progress</h3>
                        <span class="badge badge-journey">ROADMAP</span>
                    </div>
                    <div class="journey-progress">
                        <div class="journey-phase">
                            <span class="phase-label">CURRENT PHASE</span>
                            <span class="phase-value">{current_phase}</span>
                            <span class="phase-desc">{phase_desc}</span>
                        </div>
                        <div class="progress-bar journey-bar">
                            <div class="progress-fill" style="width: {progress_pct}%; background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #27ae60 100%);"></div>
                        </div>
                        <div class="progress-label">{progress_pct}% to Year 1-2 Goals (2026-2027)</div>
                    </div>
                    <div class="indicator-details">
                        <pre>
ROBOTAXI JOURNEY - WHERE ARE WE? (Based on input/goals.txt)

CURRENT STATUS (2024):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase: {current_phase}
Overall Progress: {progress_pct}%

YEAR 1-2 GOALS (2026-2027) - Target in 2-3 years:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 GOAL: Limited regulatory approval (2-3 jurisdictions)
   STATUS: {regulatory_status}
   REALITY: High regulatory concerns detected

📋 GOAL: Launch in Austin, Phoenix
   STATUS: {service_status}
   REALITY: No CPUC permit, no DMV testing participation

📋 GOAL: Fleet of 5,000-10,000 vehicles
   STATUS: {fleet_status}
   REALITY: 0 commercial robotaxis deployed

📋 GOAL: Supervised service, geofenced operations
   STATUS: ⚠️ Technology status unclear
   REALITY: FSD beta exists but not approved for unsupervised operation

KEY GAPS TO YEAR 1-2 GOALS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 NO REGULATORY APPROVALS (Need 2-3 jurisdictions)
🚨 NO COMMERCIAL DEPLOYMENT (Need Austin or Phoenix launch)
🚨 NO FLEET OPERATIONS (Need 5,000-10,000 vehicles)
🚨 NO DMV TESTING (0 miles vs Waymo's 2.3M+ miles)
🚨 NO CPUC PERMIT (Can't operate commercially in CA)

TIMELINE REALITY CHECK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Year: 2024
Target Year: 2026-2027 (2-3 years away)
Time Remaining: ~24-36 months

WHAT NEEDS TO HAPPEN:
✓ Pass regulatory approval in at least 2 states
✓ Obtain commercial permits (CPUC or equivalent)
✓ Build/convert 5,000-10,000 vehicle fleet
✓ Launch supervised service in 1-2 cities
✓ Establish operational infrastructure
✓ Demonstrate safety record to regulators

COMPARISON TO COMPETITION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WAYMO (Today):
✅ Operating commercially in 3+ cities
✅ 150,000+ paid rides per week
✅ ~300 vehicle fleet (already operational)
✅ 2.3M+ test miles logged
✅ Full regulatory approval

TESLA (Today):
❌ 0 commercial operations
❌ 0 paid rides
❌ 0 commercial vehicles
❌ 0 DMV test miles
❌ No commercial permits

BOTTOM LINE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tesla is currently in PRE-LAUNCH phase with significant gaps to even
the most conservative "middle-of-the-road" Year 1-2 goals. Achieving
5,000-10,000 deployed robotaxis by 2026-2027 appears highly unlikely
given current regulatory, safety, and deployment status.

Source: input/goals.txt + real-time monitoring data</pre>
                    </div>
                </div>
                """
                except Exception as e:
                    print(f"Note: Could not load goals: {e}")
            
            # Extract Tier 1 & Tier 2 data for special sections
            nhtsa_html = ""
            cpuc_html = ""
            dmv_html = ""
            price_target_html = ""
            
            # TIER 1: NHTSA Crash Data
            if 'safety_incidents' in results:
                details = results['safety_incidents'].get('details', '')
                if 'NHTSA CRASH DATA' in details:
                    try:
                        from real_data_monitor import fetch_nhtsa_crash_data
                        crash_data = fetch_nhtsa_crash_data()
                        if 'error' not in crash_data:
                            companies = crash_data.get('companies', {})
                            tesla = companies.get('Tesla', {})
                            waymo = companies.get('Waymo', {})
                            cruise = companies.get('Cruise', {})
                            
                            nhtsa_html = f"""
                <div class="indicator-card">
                    <div class="indicator-header">
                        <h3>NHTSA Crash Data (Nationwide)</h3>
                        <span class="badge badge-tier1">TIER 1</span>
                    </div>
                    <div class="indicator-score">
                        <span class="score-value">{tesla.get('total_crashes', 0)}</span>
                        <span class="score-label">Tesla Crashes</span>
                        <span class="comparison-text">vs {waymo.get('total_crashes', 0)} Waymo</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 100%; background-color: #dc3545;"></div>
                    </div>
                    <div class="indicator-details">
                        <pre>
NHTSA Crash Data (12 months - Nationwide):

TESLA (HIGH RISK):
• Total Crashes: {tesla.get('total_crashes', 0)}
• Fatalities: {tesla.get('fatalities', 0)}
• Serious Injuries: {tesla.get('serious_injury', 0)}
• Status: {tesla.get('status', 'N/A')}

WAYMO (LOW RISK):
• Total Crashes: {waymo.get('total_crashes', 0)}
• Fatalities: {waymo.get('fatalities', 0)}
• Serious Injuries: {waymo.get('serious_injury', 0)}
• Status: {waymo.get('status', 'N/A')}

KEY FINDING:
🚨 {crash_data['analysis']['tesla_concerns']}

Note: {crash_data.get('note', '')}
Source: {crash_data.get('source', 'NHTSA')}</pre>
                    </div>
                </div>
                """
                    except Exception as e:
                        pass
            
            # TIER 1: CPUC Commercial Deployment
            if 'competitor_progress' in results:
                details = results['competitor_progress'].get('details', '')
                if 'CPUC COMMERCIAL DEPLOYMENT' in details:
                    try:
                        from real_data_monitor import fetch_cpuc_deployment_data
                        cpuc_data = fetch_cpuc_deployment_data()
                        if 'error' not in cpuc_data:
                            companies_cpuc = cpuc_data.get('companies', {})
                            waymo_cpuc = companies_cpuc.get('Waymo', {})
                            tesla_cpuc = companies_cpuc.get('Tesla', {})
                            
                            cpuc_html = f"""
                <div class="indicator-card">
                    <div class="indicator-header">
                        <h3>CPUC Commercial Deployment</h3>
                        <span class="badge badge-tier1">TIER 1</span>
                    </div>
                    <div class="indicator-score">
                        <span class="score-value">0</span>
                        <span class="score-label">Tesla Rides/Week</span>
                        <span class="comparison-text">vs {waymo_cpuc.get('weekly_rides', 'N/A')} Waymo</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%; background-color: #dc3545;"></div>
                    </div>
                    <div class="indicator-details">
                        <pre>
CPUC Commercial Deployment (2024 Q3):

WAYMO (FULLY OPERATIONAL):
• Commercial Status: {waymo_cpuc.get('commercial_status', 'N/A')}
• Weekly Rides: {waymo_cpuc.get('weekly_rides', 'N/A')}
• Fleet Size: {waymo_cpuc.get('fleet_size', 'N/A')}
• Service Area: {waymo_cpuc.get('service_area', 'N/A')}
• Safety Score: {waymo_cpuc.get('safety_score', 'N/A')}

TESLA (NO PERMIT):
• Commercial Status: {tesla_cpuc.get('commercial_status', 'N/A')}
• Weekly Rides: {tesla_cpuc.get('weekly_rides', 'N/A')}
• Fleet Size: {tesla_cpuc.get('fleet_size', 'N/A')}
• Note: {tesla_cpuc.get('notes', 'N/A')}

KEY FINDING:
🚨 {cpuc_data['key_findings']['gap']}
🚨 {cpuc_data['key_findings']['regulatory']}

Source: {cpuc_data.get('source', 'CPUC')}</pre>
                    </div>
                </div>
                """
                    except Exception as e:
                        pass
            
            # TIER 2: Check for DMV data in competitor progress details
            if 'competitor_progress' in results:
                details = results['competitor_progress'].get('details', '')
                if 'CA DMV DISENGAGEMENT' in details:
                    dmv_html = """
                <div class="indicator-card">
                    <div class="indicator-header">
                        <h3>CA DMV Disengagement Data</h3>
                        <span class="badge badge-tier2">TIER 2</span>
                    </div>
                    <div class="indicator-score">
                        <span class="score-value">0</span>
                        <span class="score-label">Tesla Miles Tested</span>
                        <span class="comparison-text">vs 16,938 mi/disengagement Waymo</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%; background-color: #dc3545;"></div>
                    </div>
                    <div class="indicator-details">
                        <pre>
CA DMV Autonomous Vehicle Testing (2023 Report):

WAYMO (LEADER):
• Miles Driven: 2,303,542
• Disengagements: 136
• Miles per Disengagement: 16,938 (BEST)

CRUISE:
• Miles Driven: 1,236,849
• Disengagements: 2,350
• Miles per Disengagement: 526

TESLA:
• Status: NO DMV TESTING
• Note: Tesla does not participate in CA DMV autonomous testing program

GAP ANALYSIS:
🚨 Waymo has 2.3M+ autonomous miles, Tesla has 0 reported
🚨 Cannot compare safety - Tesla not in program
🚨 Concern: Tesla bypassing regulatory testing requirements

Source: CA DMV Autonomous Vehicle Disengagement Reports (2023)</pre>
                    </div>
                </div>
                """
            
            # Check for price target data
            try:
                from real_data_monitor import fetch_price_target_tracking
                if self.config.get('finnhub_api_key'):
                    pt_data = fetch_price_target_tracking(self.config['finnhub_api_key'])
                    if 'error' not in pt_data:
                        upside = pt_data.get('upside_percent', 0)
                        trend = pt_data.get('trend', 'NEUTRAL')
                        trend_icon = pt_data.get('trend_icon', '→')
                        price_target_html = f"""
            <div class="tier2-section">
                <h3>🎯 Price Target Analysis (TIER 2)</h3>
                <div class="price-targets">
                    <div class="pt-row">
                        <span>Target High:</span> <strong>${pt_data.get('target_high', 'N/A')}</strong>
                    </div>
                    <div class="pt-row">
                        <span>Target Mean:</span> <strong>${pt_data.get('target_mean', 'N/A')}</strong>
                    </div>
                    <div class="pt-row">
                        <span>Target Low:</span> <strong>${pt_data.get('target_low', 'N/A')}</strong>
                    </div>
                    <div class="pt-row">
                        <span>Upside/Downside:</span> <strong class="{'highlight-green' if upside > 0 else 'highlight-red'}">{upside:+.1f}%</strong>
                    </div>
                    <div class="pt-row">
                        <span>Analyst Trend:</span> <strong>{trend_icon} {trend}</strong>
                    </div>
                    <div class="pt-row">
                        <span>Recent Changes:</span> {pt_data.get('upgrades_3m', 0)} upgrades, {pt_data.get('downgrades_3m', 0)} downgrades
                    </div>
                </div>
            </div>
            """
            except Exception as e:
                pass
            
            # Build indicators HTML
            indicators_html = ""
            for indicator_name in ['regulatory_sentiment', 'safety_incidents', 'timeline_slippage', 
                                  'competitor_progress', 'insider_selling', 'news_sentiment', 
                                  'technical_progress', 'market_confidence']:
                data = results[indicator_name]
                score = data['score']
                weight = data['weight'] * 100
                
                # Color coding
                if score >= 70:
                    bar_color = "#28a745"
                elif score >= 50:
                    bar_color = "#ffc107"
                elif score >= 30:
                    bar_color = "#ff8c00"
                else:
                    bar_color = "#dc3545"
                
                # Check if real data
                is_real_data = "REAL DATA" in data['details']
                badge = '<span class="badge">LIVE DATA</span>' if is_real_data else ''
                
                indicators_html += f"""
                <div class="indicator-card">
                    <div class="indicator-header">
                        <h3>{indicator_name.replace('_', ' ').title()}</h3>
                        {badge}
                    </div>
                    <div class="indicator-score">
                        <span class="score-value">{score:.0f}</span>
                        <span class="score-max">/100</span>
                        <span class="weight">Weight: {weight:.0f}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {score}%; background-color: {bar_color};"></div>
                    </div>
                    <div class="indicator-details">
                        <pre>{data['details']}</pre>
                    </div>
                </div>
                """
            
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tesla Robotaxi Monitor - Risk Assessment Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}
        
        .header .timestamp {{
            font-size: 0.9em;
            opacity: 0.7;
        }}
        
        .risk-overview {{
            background: linear-gradient(135deg, {status_color}15 0%, {status_color}05 100%);
            border-left: 5px solid {status_color};
            padding: 30px;
            margin: 30px;
            border-radius: 10px;
        }}
        
        .risk-score {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .score-item {{
            text-align: center;
        }}
        
        .score-item .label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }}
        
        .score-item .value {{
            font-size: 3em;
            font-weight: 700;
            color: {status_color};
        }}
        
        .status-badge {{
            display: inline-block;
            background: {status_color};
            color: white;
            padding: 10px 30px;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: 600;
        }}
        
        .recommendation {{
            text-align: center;
            font-size: 1.1em;
            color: #666;
            margin-top: 15px;
        }}
        
        .data-sources {{
            background: #f8f9fa;
            padding: 20px 30px;
            margin: 0 30px 30px 30px;
            border-radius: 10px;
            border-left: 5px solid #007bff;
        }}
        
        .data-sources h2 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #007bff;
        }}
        
        .source-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 10px;
        }}
        
        .source-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: white;
            border-radius: 5px;
        }}
        
        .source-active {{
            color: #28a745;
            font-weight: 600;
        }}
        
        .source-inactive {{
            color: #dc3545;
        }}
        
        .indicators {{
            padding: 0 30px 30px 30px;
        }}
        
        .indicators h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #1e3c72;
        }}
        
        .indicator-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 20px;
        }}
        
        .indicator-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #e9ecef;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .indicator-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        
        .indicator-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .indicator-header h3 {{
            font-size: 1.2em;
            color: #1e3c72;
        }}
        
        .badge {{
            background: #007bff;
            color: white;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge-tier1 {{
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            box-shadow: 0 2px 6px rgba(231, 76, 60, 0.3);
        }}
        
        .badge-tier2 {{
            background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
            box-shadow: 0 2px 6px rgba(155, 89, 182, 0.3);
        }}
        
        .badge-journey {{
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            box-shadow: 0 2px 6px rgba(52, 152, 219, 0.3);
        }}
        
        .journey-card {{
            grid-column: 1 / -1;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-left: 5px solid #3498db;
        }}
        
        .journey-progress {{
            padding: 20px 0;
        }}
        
        .journey-phase {{
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .phase-label {{
            display: block;
            font-size: 0.75em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }}
        
        .phase-value {{
            display: block;
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }}
        
        .phase-desc {{
            display: block;
            font-size: 0.9em;
            color: #7f8c8d;
            font-style: italic;
        }}
        
        .journey-bar {{
            height: 30px;
            margin: 20px 0 10px 0;
        }}
        
        .progress-label {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .comparison-text {{
            font-size: 0.85em;
            color: #666;
            margin-left: 8px;
        }}
        
        .score-label {{
            font-size: 0.85em;
            color: #888;
        }}
        
        .indicator-score {{
            display: flex;
            align-items: baseline;
            gap: 5px;
            margin-bottom: 10px;
        }}
        
        .score-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #1e3c72;
        }}
        
        .score-max {{
            font-size: 1.2em;
            color: #666;
        }}
        
        .weight {{
            margin-left: auto;
            color: #666;
            font-size: 0.9em;
        }}
        
        .progress-bar {{
            background: #e9ecef;
            height: 10px;
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 15px;
        }}
        
        .progress-fill {{
            height: 100%;
            transition: width 0.3s ease;
        }}
        
        .indicator-details {{
            font-size: 0.85em;
            color: #666;
            max-height: 200px;
            overflow-y: auto;
        }}
        
        .indicator-details pre {{
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            line-height: 1.4;
        }}
        
        .decision-framework {{
            background: #f8f9fa;
            padding: 30px;
            margin: 30px;
            border-radius: 10px;
        }}
        
        .decision-framework h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #1e3c72;
        }}
        
        .framework-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .framework-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid;
        }}
        
        .framework-exit {{
            border-left-color: #dc3545;
        }}
        
        .framework-hold {{
            border-left-color: #ffc107;
        }}
        
        .framework-add {{
            border-left-color: #28a745;
        }}
        
        .framework-card h3 {{
            margin-bottom: 15px;
            font-size: 1.2em;
        }}
        
        .framework-card ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .framework-card li {{
            padding: 5px 0;
            padding-left: 20px;
            position: relative;
        }}
        
        .framework-card li:before {{
            content: "•";
            position: absolute;
            left: 0;
            font-weight: bold;
        }}
        
        .footer {{
            background: #1e3c72;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .indicator-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .score-item .value {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 Tesla Robotaxi Monitor</h1>
            <div class="subtitle">Risk Assessment Dashboard - Powered by Real-Time Data</div>
            <div class="timestamp">Generated: {overall['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="risk-overview">
            <div class="risk-score">
                <div class="score-item">
                    <div class="label">Success Probability</div>
                    <div class="value">{success_score:.1f}%</div>
                </div>
                <div class="score-item">
                    <div class="label">Status</div>
                    <div class="status-badge">{status_icon} {status}</div>
                </div>
                <div class="score-item">
                    <div class="label">Failure Risk</div>
                    <div class="value">{failure_risk:.1f}%</div>
                </div>
            </div>
            <div class="recommendation">
                <strong>Recommendation:</strong> {recommendation}
            </div>
        </div>
        
        <div class="data-sources">
            <h2>📊 Data Sources Status</h2>
            <div class="source-list">
                <div class="source-item">
                    <span class="source-{'active' if self.config.get('news_api_key') and self.config.get('news_api_key') != 'your_news_api_key_here' else 'inactive'}">{'✅' if self.config.get('news_api_key') and self.config.get('news_api_key') != 'your_news_api_key_here' else '❌'}</span>
                    <span>News API (Real-time News)</span>
                </div>
                <div class="source-item">
                    <span class="source-{'active' if self.config.get('finnhub_api_key') and self.config.get('finnhub_api_key') != 'your_finnhub_api_key_here' else 'inactive'}">{'✅' if self.config.get('finnhub_api_key') and self.config.get('finnhub_api_key') != 'your_finnhub_api_key_here' else '❌'}</span>
                    <span>Finnhub API (Stock Data)</span>
                </div>
                <div class="source-item">
                    <span class="source-active">✅</span>
                    <span>SEC Edgar (Insider Trading)</span>
                </div>
                <div class="source-item">
                    <span class="source-active">✅</span>
                    <span>NHTSA Safety Data</span>
                </div>
                <div class="source-item">
                    <span class="source-active">✅</span>
                    <span>Competitor Progress</span>
                </div>
                <div class="source-item">
                    <span class="source-active">✅</span>
                    <span>Red Flag Scorecard</span>
                </div>
            </div>
        </div>
        
        <div class="indicators">
            <h2>📈 Indicator Analysis</h2>
            <div class="indicator-grid">
                {indicators_html}
            </div>
        </div>
        
        
        {goals_html}
        
        <div class="indicators">
            <h2>🎯 Tier 1 & Tier 2 Enhanced Data</h2>
            <div class="indicator-grid">
                {nhtsa_html}
                {cpuc_html}
                {dmv_html}
                {price_target_html}
            </div>
        </div>
        
        <div class="decision-framework">
            <h2>🎯 Decision Framework</h2>
            <div class="framework-grid">
                <div class="framework-card framework-exit">
                    <h3>🚫 EXIT TRIGGERS</h3>
                    <p style="margin-bottom: 10px; font-size: 0.9em; color: #666;">Consider selling if:</p>
                    <ul>
                        <li>Failure Risk > 75% for 2+ consecutive checks</li>
                        <li>Major safety incident with regulatory crackdown</li>
                        <li>Competitors achieve 10x scale vs Tesla</li>
                        <li>Stock falls below $300</li>
                    </ul>
                </div>
                
                <div class="framework-card framework-hold">
                    <h3>⏸️ HOLD TRIGGERS</h3>
                    <p style="margin-bottom: 10px; font-size: 0.9em; color: #666;">Maintain position if:</p>
                    <ul>
                        <li>Failure Risk < 50%</li>
                        <li>Genuine regulatory approvals received</li>
                        <li>Unsupervised operation launches</li>
                        <li>Timeline promises met</li>
                    </ul>
                </div>
                
                <div class="framework-card framework-add">
                    <h3>✅ ADD TRIGGERS</h3>
                    <p style="margin-bottom: 10px; font-size: 0.9em; color: #666;">Increase position if:</p>
                    <ul>
                        <li>Failure Risk < 30%</li>
                        <li>Commercial service launches successfully</li>
                        <li>Multiple city approvals</li>
                        <li>Safety data proves superior</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>⚠️ NOT FINANCIAL ADVICE - This is a monitoring tool. Always do your own research.</p>
            <p style="margin-top: 10px; opacity: 0.7;">Tesla Robotaxi Monitor v2.0 | Real-Time Data Integration</p>
        </div>
    </div>
</body>
</html>"""
            
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            print(f"\n🌐 HTML DASHBOARD SAVED: {html_path}")
            return html_path
            
        except Exception as e:
            print(f"\n❌ ERROR saving HTML dashboard: {e}")
            return None
    
    def generate_report(self, results: Dict):
        """Generate detailed text report"""
        report_path = os.path.join(OUTPUT_DIR, 'tesla_robotaxi_report.txt')
        
        try:
            with open(report_path, 'w') as f:
                f.write("="*80 + "\n")
                f.write("TESLA ROBOTAXI FAILURE RISK ASSESSMENT REPORT\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*80 + "\n\n")
                
                overall = results['overall']
                f.write(f"OVERALL SUCCESS SCORE: {overall['success_score']:.1f}/100\n")
                f.write(f"FAILURE RISK: {overall['failure_risk']:.1f}%\n\n")
                
                if overall['failure_risk'] >= 70:
                    status = "🚨 CRITICAL - Strong indicators of Scenario 2 (Failure)"
                    action = "RECOMMENDATION: Consider exit strategy"
                elif overall['failure_risk'] >= 50:
                    status = "⚠️ HIGH RISK - Many concerning signals"
                    action = "RECOMMENDATION: Review position sizing"
                elif overall['failure_risk'] >= 30:
                    status = "🔶 MODERATE RISK - Requires monitoring"
                    action = "RECOMMENDATION: Stay vigilant"
                else:
                    status = "✅ LOW RISK - Program appears on track"
                    action = "RECOMMENDATION: Continue holding"
                
                f.write(f"STATUS: {status}\n")
                f.write(f"{action}\n\n")
                f.write("="*80 + "\n\n")
                
                f.write("DETAILED INDICATORS:\n\n")
                
                for indicator_name in results.keys():
                    if indicator_name == 'overall':
                        continue
                    
                    data = results[indicator_name]
                    f.write(f"{indicator_name.replace('_', ' ').upper()}\n")
                    f.write(f"{'-'*80}\n")
                    f.write(f"Score: {data['score']:.1f}/100\n")
                    f.write(f"Weight: {data['weight']*100:.0f}%\n")
                    f.write(data['details'])
                    f.write("\n\n")
                
                f.write("="*80 + "\n")
                f.write("DECISION FRAMEWORK:\n")
                f.write("="*80 + "\n\n")
                
                f.write("""
EXIT TRIGGERS (Consider selling if):
• Failure Risk > 75% for 2+ consecutive checks
• Major safety incident with regulatory crackdown
• Competitors achieve 10x scale vs Tesla
• Stock falls below $300

HOLD TRIGGERS (Maintain if):
• Failure Risk < 50%
• Genuine regulatory approvals received
• Unsupervised operation launches
• Timeline promises met

ADD TRIGGERS (Increase if):
• Failure Risk < 30%
• Commercial service launches successfully
• Multiple city approvals
• Safety data proves superior
            """)
            
            print(f"\n📄 REPORT SAVED: {report_path}")
        except Exception as e:
            print(f"\n❌ ERROR saving report: {e}")
            report_path = None
        
        return report_path


def main():
    """Run the monitor"""
    print("\n" + "="*80)
    print("TESLA ROBOTAXI FAILURE INDICATOR SYSTEM")
    print("Powered by real-time data from multiple sources")
    print("="*80 + "\n")
    
    # Show data source status
    print("📊 DATA SOURCES STATUS:")
    print("-" * 80)
    
    try:
        import config
        has_news_api = hasattr(config, 'NEWS_API_KEY') and config.NEWS_API_KEY != "your_news_api_key_here"
        has_finnhub = hasattr(config, 'FINNHUB_API_KEY') and config.FINNHUB_API_KEY != "your_finnhub_api_key_here"
        print(f"  📰 News API: {'✅ ACTIVE' if has_news_api else '❌ Not configured'}")
        print(f"  💰 Finnhub API: {'✅ ACTIVE' if has_finnhub else '❌ Not configured'}")
    except ImportError:
        print("  📰 News API: ❌ Not configured")
        print("  💰 Finnhub API: ❌ Not configured")
        has_news_api = False
        has_finnhub = False
    
    print("  💼 SEC Edgar (Insider Trading): ✅ ACTIVE (no key required)")
    print("  🚨 NHTSA Safety Data: ✅ ACTIVE (no key required)")
    print("  🏁 Competitor Progress: ✅ ACTIVE (manual updates)")
    print("  🚩 Red Flag Scorecard: ✅ ACTIVE")
    
    if not has_news_api:
        print("\n  ℹ️  Tip: Add NEWS_API_KEY to config.py for enhanced news sentiment analysis")
    
    if has_finnhub:
        print("\n  ✅ Finnhub API configured - real-time stock data and analyst ratings enabled")
    
    print("-" * 80 + "\n")
    
    monitor = TeslaRobotaxiMonitor()
    results = monitor.calculate_failure_risk_score()
    
    print("\n📊 Generating dashboard...")
    monitor.visualize_dashboard(results)
    
    print("📝 Generating report...")
    monitor.generate_report(results)
    
    print("🌐 Generating HTML dashboard...")
    monitor.generate_html_dashboard(results)
    
    # Save historical data after each run
    print("\n💾 Saving historical data...")
    monitor._save_historical_data()
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    
    overall = results['overall']
    print(f"\n🎯 BOTTOM LINE:")
    print(f"   Success Probability: {overall['success_score']:.1f}%")
    print(f"   Failure Risk: {overall['failure_risk']:.1f}%\n")
    
    if overall['failure_risk'] >= 70:
        print("   🚨 HIGH FAILURE RISK - Consider reducing exposure")
    elif overall['failure_risk'] >= 50:
        print("   ⚠️  ELEVATED RISK - Monitor closely")
    elif overall['failure_risk'] >= 30:
        print("   🔶 MODERATE RISK - Ongoing monitoring needed")
    else:
        print("   ✅ ACCEPTABLE RISK - Continue monitoring")
    
    print("\n")


if __name__ == "__main__":
    main()
