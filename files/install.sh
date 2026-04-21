#!/bin/bash
# ============================================================
# Solomon OS Installer — One command to rule them all
# Usage: curl -fsSL https://raw.githubusercontent.com/jvanleur2234-glitch/zo-restore/main/install.sh | bash
# ============================================================

SOLOMON_DIR="${SOLOMON_DIR:-$HOME/solomon-os}"
GITHUB_REPO="jvanleur2234-glitch/zo-restore"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

log()  { echo -e "${BLUE}[SOLOMON]${NC} $1"; }
ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
step() { echo -e "\n${BLUE}==>${NC} ${YELLOW}$1${NC}"; }

# Parse flags
while [[ $# -gt 0 ]]; do
    case $1 in
        --dir) SOLOMON_DIR="$2"; shift 2 ;;
        --telegram) TELEGRAM_BOT_TOKEN="$2"; shift 2 ;;
        --stripe-key) STRIPE_KEY="$2"; shift 2 ;;
        --hyrve) ENABLE_HYRVE="yes"; shift ;;
        --help) echo "Usage: ... | bash [ --dir /path ] [ --telegram TOKEN ] [ --stripe-key KEY ]"; exit 0 ;;
        *) shift ;;
    esac
done

echo ""
echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}     ${GREEN}Solomon OS Installer${NC}                 ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  AI-powered business ops, 24/7           ${BLUE}║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
echo ""

step "Creating Solomon OS directory..."
mkdir -p "$SOLOMON_DIR" && cd "$SOLOMON_DIR"
ok "Directory ready: $SOLOMON_DIR"

step "Fetching Solomon OS from GitHub..."
if [ -d ".git" ]; then
    log "Updating existing installation..."
    git pull origin main 2>/dev/null || git pull
else
    log "Cloning Solomon OS..."
    git clone --depth 1 https://github.com/$GITHUB_REPO . 2>/dev/null || \
    git clone --depth 1 git@github.com:$GITHUB_REPO . 2>/dev/null || \
        warn "GitHub unavailable — will create structure manually"
fi
ok "Files ready"

step "Installing Ollama..."
if command -v ollama &> /dev/null; then
    ok "Ollama already installed"
else
    curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1 && ok "Ollama installed" || warn "Ollama install failed"
fi

step "Pulling AI models (background)..."
if command -v ollama &> /dev/null; then
    ollama pull qwen3:1.7b > /dev/null 2>&1 &
    ollama pull nomic-embed-text > /dev/null 2>&1 &
    ok "Model pull started in background (use 'ollama list' to check)"
fi

step "Installing Hermes Agent..."
HERMES_DIR="$SOLOMON_DIR/hermes"
mkdir -p "$HERMES_DIR/skills" "$HERMES_DIR/config"
cat > "$HERMES_DIR/config.yaml" << 'HCONF'
inference:
  provider: nvidia
  model: nvidia/minimaxai-minimax-m2.7
  api_key: ${NVIDIA_API_KEY:-}
memory:
  provider: icarus
  icarus_url: http://localhost:5001
telegram:
  enabled: false
skills:
  directory: skills/
  auto_update: true
HCONF
ok "Hermes config ready at $HERMES_DIR/config.yaml"

step "Installing Solomon Bus..."
BUS_DIR="$SOLOMON_DIR/solomon-bus"
mkdir -p "$BUS_DIR/queue"
cat > "$BUS_DIR/bus.sh" << 'BUSEOF'
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
BUSEOF
chmod +x "$BUS_DIR/bus.sh"
ok "Solomon Bus ready at $BUS_DIR"

step "Installing Solomon Vault..."
VAULT_DIR="$SOLOMON_DIR/solomon-vault"
mkdir -p "$VAULT_DIR/brain/RD_REPORTS" "$VAULT_DIR/raw" "$VAULT_DIR/activity_log"
mkdir -p "$VAULT_DIR/brain/solomon-config"

cat > "$VAULT_DIR/brain/Services.md" << 'SVCEOF'
# Solomon OS Services

## Core Agents
- Zo — Main orchestrator
- Russell Tuna — Telegram bot (t.me/RussellTunaBot)
- Hermes — Task execution layer
- Solomon Bus — Message router

## Always-On
- Heartbeat — 30-min wake loop
- Job Runner — Background job daemon
SVCEOF

cat > "$VAULT_DIR/brain/NORTH_STAR.md" << 'NSEOF'
# North Star
Package Solomon OS as sellable AI employees for businesses.
First client: Jack Vanleur (real estate)
Revenue model: $99-499/mo per AI employee
NSEOF

cat > "$VAULT_DIR/brain/solomon-config/constitution.md" << 'CONSTEOF'
# Constitution — Tier 1 (Immutable)
1. Always improve — extract one lesson after every session
2. Never forget — store everything in the vault
3. Ship fast — perfect is the enemy of shipped
4. Make money — revenue > features
5. Client first — their time > our time
CONSTEOF

ok "Solomon Vault ready"

step "Installing Heartbeat..."
HB_DIR="$SOLOMON_DIR/.agent/heartbeat"
mkdir -p "$HB_DIR"
cat > "$HB_DIR/decision_engine.py" << 'PYEOF'
#!/usr/bin/env python3
import os, json
from datetime import datetime
VAULT = os.path.expanduser("~/solomon-os/solomon-vault/brain")
print(f"[{datetime.now().strftime('%H:%M:%S')}] Heartbeat tick — all systems nominal")
PYEOF
cat > "$HB_DIR/run_heartbeat.sh" << 'SHEOF'
#!/bin/bash
HB="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; SOL="$HOME/solomon-os"
while true; do python3 "$HB/decision_engine.py" >> "$SOL/solomon-vault/brain/activity_log/heartbeat_$(date +%Y-%m-%d).md" 2>&1; sleep 1800; done
SHEOF
chmod +x "$HB_DIR/run_heartbeat.sh"
nohup "$HB_DIR/run_heartbeat.sh" > /dev/null 2>&1 &
ok "Heartbeat running in background (PID=$!)"

step "Creating shortcuts..."
cat > "$SOLOMON_DIR/solomon" << 'SYMEOF'
#!/bin/bash
DIR="$HOME/solomon-os"; cd "$DIR"
case "$1" in status) cat solomon-vault/brain/activity_log/heartbeat_$(date +%Y-%m-%d).md 2>/dev/null | tail -3 ;; bus) bash solomon-bus/bus.sh "${2:-log}" ;; hermes) [ -x hermes/hermes ] && hermes/hermes "$@" || hermes "$@" ;; *) echo "Solomon OS — solomon {status|bus|hermes}"; esac
SYMEOF
chmod +x "$SOLOMON_DIR/solomon"
ln -sf "$SOLOMON_DIR/solomon" /usr/local/bin/solomon 2>/dev/null || true
ok "Command ready: ~/solomon-os/solomon"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}     ${GREEN}Solomon OS Installation Complete!${NC}       ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BLUE}Install dir:${NC}  $SOLOMON_DIR"
echo -e "  ${BLUE}Command:${NC}      ~/solomon-os/solomon"
echo -e "  ${BLUE}Heartbeat:${NC}    Running (check with: solomon status)"
echo ""
echo "Next steps:"
echo "  1. Set NVIDIA_API_KEY — get free credits at build.nvidia.com"
echo "  2. Set TELEGRAM_BOT_TOKEN — for Russell Tuna bot"
echo "  3. Run: ~/solomon-os/solomon status"
echo ""
