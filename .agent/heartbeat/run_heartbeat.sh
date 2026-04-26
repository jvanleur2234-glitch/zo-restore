#!/bin/bash
HB="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; SOL="$HOME/solomon-os"
while true; do python3 "$HB/decision_engine.py" >> "$SOL/solomon-vault/brain/activity_log/heartbeat_$(date +%Y-%m-%d).md" 2>&1; sleep 1800; done
