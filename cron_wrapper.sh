#!/bin/bash
# compute-economy Daily GPU Data Collector Wrapper
# Designed to be non-blocking and log-friendly for LaunchAgent

REPO_DIR="$HOME/.openclaw/workspace/references/compute-economy"
LOG_FILE="$REPO_DIR/daily_collection.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "[$TIMESTAMP] Starting GPU data collection..." >> "$LOG_FILE"

# Run the collection script
cd "$REPO_DIR"
python3 scripts/collect_daily.py >> "$LOG_FILE" 2>&1

# Run the assessment
python3 scripts/assess_market.py >> "$LOG_FILE" 2>&1

# If we have a git repo, commit the data
cd "$REPO_DIR"
git add -A 2>/dev/null
git commit -m "auto: daily data collection $(date +%Y-%m-%d)" --quiet 2>/dev/null
git push origin main --quiet 2>/dev/null

END_TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "[$END_TIMESTAMP] Collection complete." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Keep only last 100 lines of log
tail -n 100 "$LOG_FILE" > /tmp/gpu_log_tmp && mv /tmp/gpu_log_tmp "$LOG_FILE"
