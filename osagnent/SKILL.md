---
name: osagnent
description: OSagnent MVP — watches workers, learns jobs, generates AI agents. Phase 1: generic observation layer.
compatibility: Hermes Agent v0.13+
---

# OSagnent — The AI-Native Operating System

## What It Is

OSagnent watches ANY worker doing ANY task with ANY tool, learns the patterns, generates an AI agent to replicate that job, and clones itself as a workforce per department — all running LOCAL.

## Quick Start

```bash
hermes skills add osagnent
hermes chat -q "Start OSagnent observation for worker: sales_rep_01"
```

## Architecture

```
Employee works → Hermes Observe plugin (pre/post tool hooks)
              → OSagnent Core (pattern recognition + skill generation)
              → here.now (10GB per-worker memory)
              → Self-generated agent skill
              → Clone factory
```

## Phase 1 — What Gets Built

1. **Observe Layer** — Hermes plugin that logs ALL tool calls + screenshots
2. **Pattern Engine** — Groups observations → task workflows
3. **Agent Generator** — Converts learned patterns → Hermes skill files
4. **Confidence Tracker** — Tracks AI accuracy vs human approval %

## Confidence Model

| Confidence | AI Behavior |
|------------|-------------|
| 95%+ | AI does task autonomously, notifies human when done |
| 80-95% | AI does task, flags uncertainties for human review |
| 60-80% | AI does task, shows full plan before executing |
| <60% | AI asks human how to proceed |

## Status

- Phase 1: BUILDING NOW
- Phase 2: Pattern Engine
- Phase 3: Agent Generator
- Phase 4: Clone Factory

## OSagnent Skills (auto-installed)

| Skill | Purpose | Status |
|-------|---------|--------|
| `osagnent-observe` | Screen watching + pattern detection | ✅ Active |
| `osagnent-computer-use` | Desktop control via Hermes cua | ✅ Active |
| `osagnent-voice` | Voice commands + output | ✅ Active |
| `osagnent-auto-learn` | Pattern → skill generator | ✅ Active |

## Plugin

| Plugin | Hook | Purpose |
|--------|------|---------|
| `osagnent-observe` | pre/post tool | Kill switch + logging |
| `osagnent-cua` | pre/post tool + agent lifecycle | Cua session tracking + action log |

## Logs

- Kill switch: `http://localhost:5015/agents`
- Cua actions: `/tmp/osagnent-actions.log`
- Cua session: `/tmp/osagnent-cua-session.json`
- HERE API: `http://localhost:5015/`

## Activate

```bash
hermes skills add osagnent-computer-use
hermes skills add osagnent-observe
hermes skills add osagnent-voice
hermes skills add osagnent-auto-learn
hermes computer-use install  # Mac only for now
```

---

## Oh My Hermes — CTO Stack (2026-05-12)

Installed from: `https://github.com/Salomondiei08/oh-my-hermes`
Installed to: `~/.hermes/skills/` + `~/.hermes/agents/`

### What it adds

**23 new skills** covering the full app lifecycle:
- `clarify-requirements` — asks 7 structured questions, saves to memory
- `product-brief` — generates PRODUCT_BRIEF.md from requirements
- `design-handoff` — converts design notes to implementation spec
- `choose-engine` — routes to Hermes / Claude Code / Codex
- `implement-with-claude-code` — scaffolds Claude Code with full context
- `implement-with-codex` — targeted single-file fixes
- `deploy-to-vercel` — pre-deploy → deploy → capture URL
- `connect-supabase` — DB links, migrations, env vars
- `setup-monitoring` — Sentry + Uptime Kuma
- `health-check` — validates /api/health
- `post-deploy-followup` — health check + log + notification
- `manage-github-issues` — triage, create, label, assign
- `create-github-pr` — creates PR with secret scan
- `auto-issue-triage` — hourly: scores issues, picks priority
- `review-github-pr` — reviews diff, runs checks, plain-English summary
- `security-review` — secret scan + OWASP + CVE audit
- `await-merge-approval` — sends YES/NO to founder, merges or iterates
- `kanban-task` — creates and updates kanban cards at every stage
- `cto-status-report` — daily morning report
- `onboarding` — guides full setup in chat
- `send-notification` — Slack/Telegram webhook notifications
- `backup-hermes-data` — tarballs ~/.hermes/ to S3/Dropbox
- `create-skill` — meta-skill for creating new skills

**6 agent roles:**
| Agent | Role | Kanban ownership |
|---|---|---|
| CTO | Orchestrates all agents, monitors kanban, reports daily | All columns |
| PM | Triages GitHub issues, writes tickets, prioritizes | Backlog |
| Dev | Implements tickets, picks right engine, creates PRs | In Progress |
| Security | Scans every PR for secrets, OWASP, CVEs | Between Dev and QA |
| QA | Reviews PRs, runs health checks, writes founder summary | Review |
| Ops | Deploys, monitors production, handles incidents | Done + monitoring |

**5 workflows** for orchestrating multi-skill workflows.

### OSagnent integration

OSagnent's 5 layers stack WITH Oh My Hermes — they complement each other:

| OSagnent Layer | Oh My Hermes role |
|---|---|
| 🦾 Body (computer-use) | Dev agent executes via OSagnent's tool layer |
| 👀 Observe | Security agent hooks into observe to audit actions |
| 🧠 Auto-learn | CTO agent uses pattern engine to improve routing |
| 💾 HERE memory | All agents share persistent memory across sessions |
| 🗣️ Voice | Same voice layer — all agents speak to you on Telegram |

### Architecture

```
YOU (Telegram)
     ↓
HERMES (24/7 on VPS)
     ↓
┌─────────────────────────────────────┐
│            CTO Agent               │
│  monitors kanban, orchestrates      │
└──────┬──────────────────┬───────────┘
       │                  │
   ┌───┴────┐         ┌───┴─────┐
   │  PM    │         │  Dev    │
   │  Dev   │         │ Security│
   │  QA    │         │  Ops    │
   └───┬────┘         └───┬─────┘
       │                  │
       └───── Kanban ─────┘
            Backlog → In Progress → Review → Done
```

### Note

Oh My Hermes is NOT Hermes OS. It's a skill/workflow layer on top of Hermes Agent. The naming is unfortunate but intentional (Oh My Zsh pattern).
