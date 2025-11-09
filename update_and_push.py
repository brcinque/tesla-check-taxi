#!/usr/bin/env python3
"""
Tesla Robotaxi Monitor - Auto Update & Push Script

This script:
1. Runs the monitoring system
2. Extracts current scores from the output
3. Updates README.md with latest data
4. Commits and pushes all changes to GitHub

Usage:
    python3 update_and_push.py
    or
    ./update_and_push.py (if chmod +x)
"""

import os
import sys
import json
import subprocess
import re
from datetime import datetime

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(SCRIPT_DIR, 'README.md')
REPORT_PATH = os.path.join(SCRIPT_DIR, 'output', 'tesla_robotaxi_report.txt')
HISTORY_PATH = os.path.join(SCRIPT_DIR, 'output', 'tesla_robotaxi_history.json')

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80 + "\n")

def run_monitor():
    """Run the Tesla robotaxi monitor"""
    print_header("🔄 STEP 1: Running Monitoring System")
    
    try:
        result = subprocess.run(
            ['python3', 'tesla_robotaxi_monitor.py'],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ Monitoring completed successfully")
            return True
        else:
            print(f"❌ Monitoring failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Monitoring timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running monitor: {e}")
        return False

def extract_scores():
    """Extract scores from the monitoring report"""
    print_header("📊 STEP 2: Extracting Current Scores")
    
    if not os.path.exists(REPORT_PATH):
        print(f"❌ Report file not found: {REPORT_PATH}")
        return None
    
    try:
        with open(REPORT_PATH, 'r') as f:
            content = f.read()
        
        # Extract overall scores
        failure_risk_match = re.search(r'FAILURE RISK:\s*([0-9.]+)%', content)
        success_score_match = re.search(r'OVERALL SUCCESS SCORE:\s*([0-9.]+)/100', content)
        
        if not failure_risk_match or not success_score_match:
            print("❌ Could not find overall scores in report")
            return None
        
        failure_risk = float(failure_risk_match.group(1))
        success_score = float(success_score_match.group(1))
        
        # Extract individual indicator scores
        scores = {}
        
        # Pattern to match indicator sections and their scores
        indicator_pattern = r'([A-Z][A-Z\s]+)\n-+\nScore:\s*([0-9.]+)/100'
        matches = re.finditer(indicator_pattern, content)
        
        for match in matches:
            indicator_name = match.group(1).strip()
            score = float(match.group(2))
            
            # Normalize indicator names
            if 'REGULATORY' in indicator_name:
                scores['Regulatory Sentiment'] = score
            elif 'SAFETY' in indicator_name:
                scores['Safety Incidents'] = score
            elif 'TIMELINE' in indicator_name:
                scores['Timeline Slippage'] = score
            elif 'COMPETITOR' in indicator_name:
                scores['Competitor Progress'] = score
            elif 'INSIDER' in indicator_name:
                scores['Insider Selling'] = score
            elif 'NEWS' in indicator_name:
                scores['News Sentiment'] = score
            elif 'TECHNICAL' in indicator_name:
                scores['Technical Progress'] = score
            elif 'MARKET' in indicator_name:
                scores['Market Confidence'] = score
            elif 'EXECUTIVE' in indicator_name:
                scores['Executive Departures'] = score
        
        result = {
            'failure_risk': failure_risk,
            'success_score': success_score,
            'scores': scores,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Extracted scores:")
        print(f"   Failure Risk: {failure_risk}%")
        print(f"   Success Score: {success_score}/100")
        print(f"   Individual indicators: {len(scores)}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error extracting scores: {e}")
        return None

def update_readme(scores_data):
    """Update README.md with current scores"""
    print_header("📝 STEP 3: Updating README")
    
    if not os.path.exists(README_PATH):
        print(f"❌ README not found: {README_PATH}")
        return False
    
    try:
        with open(README_PATH, 'r') as f:
            readme_content = f.read()
        
        scores = scores_data['scores']
        failure_risk = scores_data['failure_risk']
        
        # Update overall assessment
        old_assessment_pattern = r'## Current Assessment: \*\*[0-9.]+% Failure Risk\*\* ⚠️'
        new_assessment = f"## Current Assessment: **{failure_risk}% Failure Risk** ⚠️"
        readme_content = re.sub(old_assessment_pattern, new_assessment, readme_content)
        
        # Find the top 4 worst scores for Key Red Flags
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])[:4]
        
        # Build Key Red Flags section
        red_flags = []
        for indicator, score in sorted_scores:
            if indicator == 'Competitor Progress':
                red_flags.append(f"- **{indicator}: {score}/100** 🚨 Tesla 5+ years behind (REAL DATA)")
            elif indicator == 'Timeline Slippage':
                red_flags.append(f"- **{indicator}: {score}/100** 🚨 10 years of missed promises")
            elif indicator == 'Safety Incidents':
                red_flags.append(f"- **{indicator}: {score}/100** 🚨 NHTSA crash data shows 736 Tesla crashes vs 23 Waymo")
            elif indicator == 'Insider Selling':
                red_flags.append(f"- **{indicator}: {score}/100** ⚠️ Heavy executive sales (SEC EDGAR TRACKING)")
            else:
                red_flags.append(f"- **{indicator}: {score}/100** ⚠️")
        
        # Update Key Red Flags section
        red_flags_pattern = r'### Key Red Flags:\n(?:- \*\*.*\n)+'
        new_red_flags = "### Key Red Flags:\n" + "\n".join(red_flags[:4]) + "\n"
        readme_content = re.sub(red_flags_pattern, new_red_flags, readme_content)
        
        # Update indicator table
        table_rows = []
        indicator_order = [
            'Regulatory Sentiment', 'Safety Incidents', 'Timeline Slippage',
            'Competitor Progress', 'Insider Selling', 'News Sentiment',
            'Technical Progress', 'Market Confidence', 'Executive Departures'
        ]
        
        weights = {
            'Regulatory Sentiment': '20%',
            'Safety Incidents': '20%',
            'Timeline Slippage': '15%',
            'Competitor Progress': '10%',
            'Insider Selling': '10%',
            'News Sentiment': '10%',
            'Technical Progress': '10%',
            'Market Confidence': '5%',
            'Executive Departures': '0%'
        }
        
        for indicator in indicator_order:
            if indicator in scores:
                score = scores[indicator]
                weight = weights.get(indicator, '0%')
                
                # Add emoji based on score
                if score < 40:
                    emoji = ' 🚨'
                elif score < 50:
                    emoji = ''
                else:
                    emoji = ''
                
                if indicator == 'Executive Departures':
                    table_rows.append(f"| {indicator} | {weight} | Red Flag Indicator |")
                else:
                    table_rows.append(f"| {indicator} | {weight} | {score}/100{emoji} |")
        
        # Replace table
        table_pattern = r'\| Indicator \| Weight \| Current Score \|\n\|[-|]+\|\n(?:\|.*\|\n)+'
        new_table = "| Indicator | Weight | Current Score |\n|-----------|--------|---------------|\n" + "\n".join(table_rows) + "\n"
        readme_content = re.sub(table_pattern, new_table, readme_content)
        
        # Write updated README
        with open(README_PATH, 'w') as f:
            f.write(readme_content)
        
        print("✅ README updated successfully")
        print(f"   - Overall failure risk: {failure_risk}%")
        print(f"   - Key red flags: {len(red_flags)} indicators")
        print(f"   - Indicator table: {len(table_rows)} rows")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        import traceback
        traceback.print_exc()
        return False

def commit_and_push():
    """Commit and push changes to GitHub"""
    print_header("🚀 STEP 4: Committing and Pushing to GitHub")
    
    try:
        # Check if there are changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True
        )
        
        if not result.stdout.strip():
            print("ℹ️  No changes to commit")
            return True
        
        print("📋 Changes detected:")
        print(result.stdout)
        
        # Add all changes
        print("\n📦 Staging changes...")
        subprocess.run(['git', 'add', '.'], cwd=SCRIPT_DIR, check=True)
        
        # Create commit message with timestamp and scores
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Try to get failure risk from history
        try:
            with open(HISTORY_PATH, 'r') as f:
                history = json.load(f)
                latest_score = history['scores'][-1] if history['scores'] else 'N/A'
            failure_risk = f"{100 - latest_score:.1f}%" if isinstance(latest_score, (int, float)) else 'N/A'
        except:
            failure_risk = 'N/A'
        
        commit_message = f"""Update monitoring data and README - {timestamp}

- Updated monitoring output with latest data
- Refreshed README with current risk scores
- Failure risk: {failure_risk}
- Dashboard and reports regenerated

[Automated update via update_and_push.py]"""
        
        # Commit
        print("\n💾 Committing changes...")
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=SCRIPT_DIR,
            check=True
        )
        
        # Push
        print("\n🌐 Pushing to GitHub...")
        result = subprocess.run(
            ['git', 'push'],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Successfully pushed to GitHub")
            return True
        else:
            print(f"❌ Push failed: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in commit/push: {e}")
        return False

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("🚀 TESLA ROBOTAXI MONITOR - AUTO UPDATE & PUSH")
    print("=" * 80)
    
    # Step 1: Run monitoring
    if not run_monitor():
        print("\n❌ FAILED: Could not run monitoring system")
        sys.exit(1)
    
    # Step 2: Extract scores
    scores_data = extract_scores()
    if not scores_data:
        print("\n❌ FAILED: Could not extract scores from report")
        sys.exit(1)
    
    # Step 3: Update README
    if not update_readme(scores_data):
        print("\n❌ FAILED: Could not update README")
        sys.exit(1)
    
    # Step 4: Commit and push
    if not commit_and_push():
        print("\n❌ FAILED: Could not commit and push changes")
        sys.exit(1)
    
    # Success!
    print_header("✅ SUCCESS - ALL UPDATES COMPLETE")
    print("📊 Monitoring data updated")
    print("📝 README.md refreshed with current scores")
    print("🌐 All changes pushed to GitHub")
    print("\nRepository URL: https://github.com/brcinque/tesla-check-taxi")
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()

