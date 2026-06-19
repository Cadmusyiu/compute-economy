#!/bin/bash
# compute-economy Daily GPU Data Collector Wrapper
# Designed to be non-blocking and log-friendly for LaunchAgent
# Handles errors gracefully and reports exit codes

REPO_DIR="$HOME/.openclaw/workspace/references/compute-economy"
LOG_FILE="$REPO_DIR/daily_collection.log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
EXIT_CODE=0

echo "[$TIMESTAMP] Starting GPU data collection..." >> "$LOG_FILE"

# Run the collection script
cd "$REPO_DIR"
python3 scripts/collect_daily.py >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "  ❌ Collection script failed with exit code $?" >> "$LOG_FILE"
    EXIT_CODE=1
fi

# Run the assessment
python3 scripts/assess_market.py >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "  ❌ Assessment script failed with exit code $?" >> "$LOG_FILE"
    EXIT_CODE=1
fi

# Run the correlation builder (non-fatal if it fails)
python3 scripts/build_correlation.py >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "  ⚠️  Correlation builder warning (non-fatal)" >> "$LOG_FILE"
fi

# If we have a git repo, commit the data
cd "$REPO_DIR"
git add -A 2>/dev/null
git commit -m "auto: daily data collection $(date +%Y-%m-%d)" --quiet 2>/dev/null
if [ $? -eq 0 ]; then
    echo "  ✅ Data committed to git" >> "$LOG_FILE"
    git push origin main --quiet 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  ✅ Pushed to origin main" >> "$LOG_FILE"
    else
        echo "  ⚠️  Git push failed (network?)" >> "$LOG_FILE"
    fi
fi

END_TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "[$END_TIMESTAMP] Collection complete (exit: $EXIT_CODE)." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Keep only last 100 lines of log
tail -n 100 "$LOG_FILE" > /tmp/gpu_log_tmp && mv /tmp/gpu_log_tmp "$LOG_FILE"

exit $EXIT_CODE
