#!/bin/bash
# Solomon OS Heartbeat — runs every 30 minutes via crontab
# Wakes Solomon OS, checks for actions, executes if needed

HEARTBEAT_DIR="/home/workspace/.agent/heartbeat"
LOG_DIR="/home/workspace/solomon-vault/brain/activity_log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="$LOG_DIR/heartbeat_$(date '+%Y-%m-%d').md"

# Ensure log dir exists
mkdir -p "$LOG_DIR"

echo "[$TIMESTAMP] 💓 Heartbeat triggered" >> "$LOG_FILE"

# Run decision engine
cd "$HEARTBEAT_DIR"
python3 decision_engine.py >> "$LOG_FILE" 2>&1

# Log completion
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Heartbeat complete" >> "$LOG_FILE"
