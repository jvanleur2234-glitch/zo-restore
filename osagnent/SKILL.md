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
