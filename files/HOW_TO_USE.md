# How to Use This System

## Quick Start

### Finding and Adding a New GitHub
```bash
# Clone
git clone --depth 1 https://github.com/OWNER/REPO

# License check
bun Skills/zo-github/scripts/gh-license.js --path /home/workspace/repos/REPO

# Security scan
bun Skills/zo-github/scripts/gh-security.js --path /home/workspace/repos/REPO

# Fork to your GitHub
gh repo fork OWNER/REPO

# Store in memory
python3 << 'EOF'
import json
from datetime import datetime
entry = {"repo": "OWNER/REPO", "stars": N, "license": "...", "commercial_use": True, "forked": True, "installed": False, "notes": "...", "ts": datetime.utcnow().isoformat()}
with open("/home/workspace/memory_db/memory.jsonl", "a") as f:
    f.write(json.dumps(entry) + "\n")
EOF
```

### Running Installed Tools

```bash
# Hermes (AI Agent with 94 skills)
export PATH="$PATH:/root/.hermes/hermes-agent/venv/bin"
hermes --help

# MegaMemory (Memory MCP server)
megamemory

# Browser Use (AI Browser Automation)
pip install browser-use
python -c "from browser_use import Browser; print('OK')"

# Prefect (Workflow Orchestration)
python -c "from prefect import flow; print('OK')"

# Penny (Claude Code wrapper)
penny --help

# ReleaseGuard (Security Pre-release check)
releaseguard check .

# MoneyPrinterTurbo (Video from text)
cd /home/workspace/repos/moneyprinterturbo && python main.py
# Runs on port 8080
```

### Zo Space (Your Storefront)

**URL:** https://josephv.zo.space

**Pages built:**
- `/` — Homepage store
- `/studio` — AI Game Studio
- `/clone` — GitHub ClonePilot
- `/spec` — Spec Generator
- `/packs` — Product packs

**API endpoints:**
- `POST /api/create-checkout` — Create Stripe checkout session
- `POST /api/studio-design` — Generate game/app from prompt
- `POST /api/clone` — Clone and analyze a GitHub repo
- `POST /api/generate-spec` — Generate feature spec

### Stripe Products

All products created in Stripe dashboard. Payment links:
- ChatGPT Pro Pro: https://buy.stripe.com/...
- SpecToCode: https://buy.stripe.com/...
- ClonePilot: https://buy.stripe.com/...
- AI Dev Agent: https://buy.stripe.com/...

### Scheduled Agents

1. **Morning Brief** — Runs at 7 AM CT daily, emails Stripe revenue report
2. **48-Hour Pulse** — Runs every 2 hours, monitors and restarts services

### Security Scanning

```bash
# Our custom scanner
bun Skills/zo-github/scripts/gh-security.js --path /path/to/repo

# Install and run Trivy (for Docker/vulns)
apt install -y trivy
trivy repo /path/to/repo --security-checks vuln,config,secret

# Check specific files
grep -rn "AKIA\|password.*=\|getenv\|exec(" /path/to/repo --include="*.py" --include="*.js"
```

### GitHub Auth
```bash
# Already authenticated as: jvanleur2234-glitch
gh auth status
gh repo list
```

### Memory System
```bash
# View all stored repos
cat /home/workspace/memory_db/memory.jsonl | python3 -c "import sys,json; [print(json.loads(l)['repo'], '|', json.loads(l).get('commercial_use','?')) for l in sys.stdin]"

# Search memory
grep "keyword" /home/workspace/memory_db/memory.jsonl

# Rebuild from cloned repos
python3 << 'EOF'
# See REPOS_INVENTORY.md for rebuild script
EOF
```

## Architecture Overview

```
User Request
    ↓
Zo Space (storefront) ← Stripe (payments)
    ↓
This Agent (orchestrator)
    ├── GitHub (find, fork, clone repos)
    ├── Security Scanner (license + secrets)
    ├── Installed Tools (hermes, browser-use, etc.)
    ├── Zo Space (build and deploy web apps)
    └── Scheduled Agents (monitoring + daily briefs)
```
