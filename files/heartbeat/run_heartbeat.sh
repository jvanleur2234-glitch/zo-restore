#!/bin/bash
# Solomon OS Heartbeat Runner — infinite loop, survives restarts
# Started by Job Runner or manually

HEARTBEAT_DIR="/home/workspace/.agent/heartbeat"
LOG_DIR="/home/workspace/solomon-vault/brain/activity_log"
TIMESTAMP=$(date '+%Y-%m-%d')
LOG_FILE="$LOG_DIR/heartbeat_$TIMESTAMP.md"

mkdir -p "$LOG_DIR" "$HEARTBEAT_DIR"

while true; do
    TS=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TS] 💓 Heartbeat tick" >> "$LOG_FILE"
    
    cd "$HEARTBEAT_DIR"
    python3 decision_engine.py >> "$LOG_FILE" 2>&1
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 😴 Sleeping 30 min..." >> "$LOG_FILE"
    sleep 1800  # 30 minutes
done
