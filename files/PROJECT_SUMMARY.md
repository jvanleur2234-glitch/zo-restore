# Project Summary — Joseph's Open Source AI Business System
**Last Updated:** 2026-03-23

---

## 🤖 What We Built

A system that:
1. Finds open-source GitHub projects
2. Checks licenses for commercial use
3. Security scans them
4. Forks the good ones to your GitHub
5. Installs and tests them
6. Combines them into businesses

---

## 🌐 Live Services (Running Now)

| Service | URL | Status |
|---------|-----|--------|
| MoneyPrinterTurbo (video generator) | Port 8080 | ✅ RUNNING |
| OpenBotX (multi-agent platform) | https://openbotx-agent-platform-josephv.zocomputer.io | ✅ RUNNING |
| Zo Space (storefront) | https://josephv.zo.space | ✅ LIVE |

---

## 💰 Stripe Products (Live on Store)

| Product | Price | Payment Link |
|---------|-------|--------------|
| ChatGPT Pro Pro | $29 | https://buy.stripe.com/... |
| SpecToCode Full Spec | $49 | https://buy.stripe.com/... |
| ClonePilot | $79 | https://buy.stripe.com/... |
| AI Dev Agent Monthly | $499/mo | https://buy.stripe.com/... |
| Copywriting | $34 | https://buy.stripe.com/... |
| Research Master | $24 | https://buy.stripe.com/... |

---

## 🧠 Agent Personas Created

1. **AI Engineer** — ML/AI development specialist
2. **Growth Hacker** — Marketing and traffic
3. **Sales Engineer** — CRM and closing deals
4. **Creative Director** — Game/app creative direction
5. **Game Designer** — Game mechanics and systems
6. **Lead Programmer** — Code architecture
7. **Art Director** — Visual design
8. **QA Lead** — Testing and quality

---

## ⏰ Scheduled Agents

1. **Morning Business Brief** — Runs daily at 7 AM CT, checks Stripe revenue, reports findings via email
2. **48-Hour Pulse Agent** — Every 2 hours, monitors services and attempts restarts if down

---

## 📂 Memory System

- `memory_db/memory.jsonl` — All processed GitHub repos with full metadata
- `AGENTS.md` — This file, permanent workspace memory
- `money_logic/` — Business strategy docs
- `Projects/` — Combined project builds

---

## 🔑 Installed Tools & CLIs

| Tool | Version | Purpose |
|------|---------|---------|
| hermes | 0.4.0 | 94-skill AI agent (NousResearch) |
| megamemory | 1.6.1 | Memory/knowledge MCP server |
| browser-use | 0.12.2 | AI browser automation |
| cdp-use | installed | Chrome DevTools Protocol for browser-use |
| penny | 0.0.18 | Claude Code wrapper (frectonz) |
| prefect | 3.6.23 | Workflow orchestration |
| agentscope | installed | Multi-agent framework |
| langflow | NOT installed | Needs heavy deps |
| n8n-mcp | installed | n8n automation integration |
| trivy | 0.69.3 | Security vulnerability scanner |
| releaseguard | installed | Pre-release security checker |
| x11vnc | installed | VNC server for virtual screens |
| Xvfb | installed | Virtual framebuffer |
| gh | authenticated | GitHub CLI |
| uv | 0.6.14 | Python package installer |

---

## 📋 All Forked GitHub Repos

See `REPOS_INVENTORY.md` for full list of all 68+ repos processed.

---

## 🏗️ Zo Space Routes Built

- `/` — Homepage with products and checkout
- `/checkout` — Stripe checkout integration
- `/api/create-checkout` — Stripe checkout session API
- `/api/promptvault-checkout` — Prompt vault payment
- `/studio` — AI Game Studio
- `/api/studio-design` — Game generation API
- `/clone` — ClonePilot GitHub clone interface
- `/api/clone` — Clone execution API
- `/spec` — SpecToCode spec generator
- `/api/generate-spec` — Spec generation
- `/api/save-spec` — Spec download API
- `/packs` — Product packs page

---

## 🔒 Security Scanning

We use a 3-layer security approach:
1. **License scan** — Can we commercially use it?
2. **Pattern scan** — Our custom scanner for API keys, passwords, secrets
3. **Trivy scan** — Docker/container vulnerability scanning

All repos are flagged BLOCKED/CLEAN based on severity scores.
