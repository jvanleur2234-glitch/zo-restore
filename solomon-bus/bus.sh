#!/bin/bash
BUS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUEUE_DIR="$BUS_DIR/queue"
LOG="$BUS_DIR/bus.log"
PID_FILE="$BUS_DIR/bus.pid"
mkdir -p "$QUEUE_DIR"
log_msg() { echo "[$(date '+%H:%M:%S')] $1" >> "$LOG"; }
publish() { echo "{\"id\":\"$(date +%s%N)\",\"ch\":\"$1\",\"msg\":$2}" > "$QUEUE_DIR/$1-$(date +%s%N).jsonl"; log_msg "PUB $1"; }
subscribe() { inotifywait -q -t "${2:-5}" -e create "$QUEUE_DIR" 2>/dev/null || true; cat "$(ls "$QUEUE_DIR"/${1}-*.jsonl 2>/dev/null | head -1)" 2>/dev/null; }
case "$1" in start) nohup "$BUS_DIR/bus.sh" loop > /dev/null 2>&1 & echo $! > "$PID_FILE"; log_msg "Bus started" ;; stop) kill "$(cat "$PID_FILE" 2>/dev/null)" 2>/dev/null ;; pub) publish "$2" "$3" ;; sub) subscribe "$2" "$3" ;; log) tail -f "$LOG" ;; esac
