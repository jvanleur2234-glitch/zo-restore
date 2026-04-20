# AGENTS.md — Joseph's Zo Computer

## System Overview
This is Joseph's personal AI business system. It finds, analyzes, forks, installs, and combines open-source GitHub projects into commercial products.

## Key Files
- `PROJECT_SUMMARY.md` — Live overview of everything built
- `REPOS_INVENTORY.md` — Complete list of all 60+ repos processed
- `memory_db/memory.jsonl` — Machine-readable repo database
- `HOW_TO_USE.md` — Quick reference for running everything

## Live Services
- **MoneyPrinterTurbo**: port 8080 (video from text)
- **OpenBotX**: https://openbotx-agent-platform-josephv.zocomputer.io
- **Zo Space Store**: https://josephv.zo.space

## Core Installed Tools
- hermes (100+ skills including Taste-Skill), megamemory, browser-use, prefect, penny, releaseguard, trivy

## Always-On Systems

- **Solomon Heartbeat** — Autonomous wake loop every 30 min. Survives conversation resets.
  - Runner: tmux session `solomon-heartbeat`
  - Scripts: `heartbeat/run_heartbeat.sh` + `heartbeat/decision_engine.py`
  - 5 checks per cycle: services, job queue, HYRVE jobs, Stripe revenue, soul update
  - Activity log: `solomon-vault/brain/activity_log/`
  - Status: `solomon-vault/brain/heartbeat_status.json`
  - Alerts: `solomon-vault/brain/alerts.json`
  - Also syncs `brain/soul.md` — full identity file all agents read for context
- **Job Runner** — Persistent background jobs. Survives resets.
  - Submit: `.agent/jobs/submit.sh "<command>" [timeout]`
  - Status: `.agent/jobs/status.sh`
  - Logs: `.agent/jobs/logs/`
- **tmux** — Installed. Use for anything > 2 min.
  - Start: `tmux new -s agent -d`
  - Send cmd: `tmux send -t agent 'command'`

## zo-excellence-package (brain files)
Lives at: /home/workspace/zo-excellence-package
Brain files, skills, and shared knowledge synced from GitHub: jvanleur2234-glitch/zo-excellence-package
Key files: HERMES_CAPABILITIES.md, SOLOMON_OS.md, ARENA_AI.md, MegaPlan/, brain/soul.md

## Zo Space Routes
Homepage `/`, checkout `/checkout`, game studio `/studio`, clonepilot `/clone`, spectocode `/spec`

## Scheduled Agents
- Morning Business Brief: daily 7 AM CT (email)
- 48-Hour Pulse: every 2 hours (monitoring)

## Payment
Stripe connected. Products live. No ads — organic growth only.
