# Automated Update Guide

This guide explains how to automatically update your monitoring data, README, and push everything to GitHub with one command.

---

## 🚀 Quick Start

**Single command to update everything:**

```bash
python3 update_and_push.py
```

or

```bash
./update_and_push.py
```

**That's it!** The script will:
1. ✅ Run the monitoring system
2. ✅ Extract current scores
3. ✅ Update README with latest data
4. ✅ Update dashboard and reports
5. ✅ Commit all changes
6. ✅ Push to GitHub

---

## 📋 What Gets Updated

### Monitoring Outputs
- `output/tesla_robotaxi_dashboard.html` - Interactive HTML dashboard
- `output/tesla_robotaxi_dashboard.png` - Visualization chart
- `output/tesla_robotaxi_report.txt` - Detailed text report
- `output/tesla_robotaxi_history.json` - Historical tracking

### README.md
- **Current Assessment** - Updated failure risk percentage
- **Key Red Flags** - Top 4 worst indicators dynamically updated
- **Indicator Table** - All 9 indicators with current scores

### Git Repository
- All changes committed with descriptive message
- Everything pushed to GitHub automatically

---

## 🔧 How It Works

### Step 1: Run Monitoring
```
🔄 STEP 1: Running Monitoring System
✅ Monitoring completed successfully
```

Runs `tesla_robotaxi_monitor.py` to generate fresh data from all sources.

### Step 2: Extract Scores
```
📊 STEP 2: Extracting Current Scores
✅ Extracted scores:
   Failure Risk: 54.2%
   Success Score: 45.8/100
   Individual indicators: 9
```

Parses `output/tesla_robotaxi_report.txt` to extract all current scores.

### Step 3: Update README
```
📝 STEP 3: Updating README
✅ README updated successfully
   - Overall failure risk: 54.2%
   - Key red flags: 4 indicators
   - Indicator table: 9 rows
```

Updates `README.md` with:
- Current overall failure risk
- Top 4 worst scores in "Key Red Flags"
- Complete indicator table with latest scores

### Step 4: Commit & Push
```
🚀 STEP 4: Committing and Pushing to GitHub
📦 Staging changes...
💾 Committing changes...
🌐 Pushing to GitHub...
✅ Successfully pushed to GitHub
```

Commits everything with an automated message and pushes to your repository.

---

## 📝 Commit Message Format

The script creates descriptive commit messages:

```
Update monitoring data and README - 2024-11-08 14:30

- Updated monitoring output with latest data
- Refreshed README with current risk scores
- Failure risk: 54.2%
- Dashboard and reports regenerated

[Automated update via update_and_push.py]
```

---

## ⚙️ Configuration

The script automatically detects:
- Script directory location
- README.md path
- Output file paths
- Git repository

**No configuration needed!**

---

## 🔄 Recommended Usage

### Daily Updates
```bash
# Run once per day to track changes
python3 update_and_push.py
```

### Weekly Updates
```bash
# Add to crontab for weekly automation
# Every Monday at 9 AM:
0 9 * * 1 cd /path/to/tesla-check && python3 update_and_push.py
```

### Before Sharing
```bash
# Always run before sharing your repository
python3 update_and_push.py
```

---

## 🛡️ Safety Features

### Error Handling
- ✅ Validates monitoring completed successfully
- ✅ Checks that scores were extracted
- ✅ Verifies README was updated
- ✅ Handles git errors gracefully
- ✅ Provides clear error messages

### Protections
- Only commits if there are actual changes
- Preserves your API keys (never committed)
- Respects .gitignore rules
- Clear output showing what's happening

---

## 🔍 Troubleshooting

### "Monitoring failed"
**Issue:** Monitor script couldn't run

**Solutions:**
1. Check API keys in `config.py`
2. Ensure dependencies installed: `pip install -r requirements.txt`
3. Run manually first: `python3 tesla_robotaxi_monitor.py`

### "Could not extract scores"
**Issue:** Report file not found or format changed

**Solutions:**
1. Check `output/tesla_robotaxi_report.txt` exists
2. Run monitor manually to verify it works
3. Check for errors in monitoring output

### "Git operation failed"
**Issue:** Can't commit or push

**Solutions:**
1. Ensure git is configured: `git config --list`
2. Check GitHub authentication (token/SSH)
3. Verify repository remote: `git remote -v`
4. Check for uncommitted changes: `git status`

### "Permission denied"
**Issue:** Script not executable

**Solution:**
```bash
chmod +x update_and_push.py
```

---

## 📊 What Gets Pushed

### Always Included:
- ✅ Updated README.md
- ✅ output/tesla_robotaxi_dashboard.html
- ✅ output/tesla_robotaxi_dashboard.png
- ✅ output/tesla_robotaxi_report.txt
- ✅ output/tesla_robotaxi_history.json

### Always Excluded (via .gitignore):
- 🔒 config.py (your API keys)
- 🔒 tokens.txt (your tokens)
- 🔒 archive/ (local backups)

---

## 🎯 Manual Alternative

If you prefer to do it manually:

```bash
# 1. Run monitoring
python3 tesla_robotaxi_monitor.py

# 2. Manually update README.md with scores from output/

# 3. Commit and push
git add .
git commit -m "Update monitoring data"
git push
```

**But the script does all this automatically!**

---

## 🔄 Integration with GitHub Actions (Future)

Want to automate even further? You could:

1. **Schedule automatic updates** with GitHub Actions
2. **Run on a schedule** (daily, weekly)
3. **Automatic commits** to your repo

See GitHub Actions documentation for scheduling workflows.

---

## 📈 Benefits

### Time Savings
- **Manual process**: 10-15 minutes
  - Run monitor
  - Extract scores manually
  - Update README by hand
  - Commit and push

- **Automated process**: 1 minute
  - Single command
  - Everything updated
  - Ready to share

### Accuracy
- ✅ No manual transcription errors
- ✅ Always current data
- ✅ Consistent formatting
- ✅ Automated score ranking

### Consistency
- ✅ Same process every time
- ✅ Standardized commit messages
- ✅ Professional update cadence

---

## 🎯 Example Output

```
================================================================================
🚀 TESLA ROBOTAXI MONITOR - AUTO UPDATE & PUSH
================================================================================

================================================================================
🔄 STEP 1: Running Monitoring System
================================================================================

✅ Monitoring completed successfully

================================================================================
📊 STEP 2: Extracting Current Scores
================================================================================

✅ Extracted scores:
   Failure Risk: 54.2%
   Success Score: 45.8/100
   Individual indicators: 9

================================================================================
📝 STEP 3: Updating README
================================================================================

✅ README updated successfully
   - Overall failure risk: 54.2%
   - Key red flags: 4 indicators
   - Indicator table: 9 rows

================================================================================
🚀 STEP 4: Committing and Pushing to GitHub
================================================================================

📋 Changes detected:
 M README.md
 M output/tesla_robotaxi_dashboard.html
 M output/tesla_robotaxi_dashboard.png
 M output/tesla_robotaxi_history.json
 M output/tesla_robotaxi_report.txt

📦 Staging changes...

💾 Committing changes...

🌐 Pushing to GitHub...
✅ Successfully pushed to GitHub

================================================================================
✅ SUCCESS - ALL UPDATES COMPLETE
================================================================================

📊 Monitoring data updated
📝 README.md refreshed with current scores
🌐 All changes pushed to GitHub

Repository URL: https://github.com/brcinque/tesla-check-taxi

================================================================================
```

---

## ✅ Checklist

Before running for the first time:

- [ ] API keys configured in `config.py`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Git configured with your credentials
- [ ] Repository has remote set: `git remote -v`
- [ ] Script is executable: `chmod +x update_and_push.py`

Then just run:
```bash
python3 update_and_push.py
```

---

**That's it! Your monitoring system, README, and GitHub repository will always be in sync.** 🚀

