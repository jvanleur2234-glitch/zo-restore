# OSagnent MVP — Phase 1

## The Vision

OSagnent watches ANY worker doing ANY task, learns the job from observation, generates an AI agent to replicate that work, and clones itself as a workforce per department — all running LOCAL, never touching the cloud.

**4 rules from Joseph:**
1. Worker opens app, starts shift → OSagnent observes everything they do with their tools
2. Worker closes app, ends shift → OSagnent generates a skill for everything they did
3. Next day: AI does the work, worker supervises
4. When AI makes a mistake, worker tells it once → AI never makes that mistake again

## Architecture

```
Worker does task → Hermes pre/post tool hooks (observe every action)
               → OSagnent pattern engine (clusters into job workflows)
               → Self-generated Hermes skill (learned from observation)
               → here.now memory (10GB per worker, permanent)
               → Clone factory (generate department-specific AI agents)

Worker corrects AI → feedback recorded → OSagnent never repeats that mistake
```

## Phase 1 Components

### 1. OSagnent Observe Plugin (Hermes)
- Location: `~/.hermes/plugins/osagnent-observe/`
- Hooks: `pre_tool_call`, `post_tool_call`, `on_session_finalize`
- Stores: `~/.hermes/osagnent/observations/<worker_id>/<session>.jsonl`
- Tracks: tool calls, arguments, results, time spent, decisions made

### 2. OSagnent Skill (Hermes)
- Location: `~/.hermes/skills/osagnent/`
- Commands:
  - `osagnent start <worker_id>` — begin observation session
  - `osagnent stop` — end observation, trigger pattern analysis
  - `osagnent status` — show current observation session
  - `osagnent confidence` — show AI confidence score vs worker
  - `osagnent report` — show learned patterns

### 3. Pattern Engine (Python)
- Location: `~/.hermes/osagnent/core/pattern_engine.py`
- Reads: observation JSONL files
- Groups: sequential tool calls into task workflows
- Scores: confidence based on repetition + human approval rate

### 4. here.now Memory Integration
- Each worker gets 10GB persistent memory
- Stores: raw observations, learned skills, feedback corrections
- On restart: reloads worker's full history instantly

### 5. Kill Switch (already built)
- Enforces budget per worker
- Stops runaway AI spending
- Tracks cost per learned task

## Confidence Model

| Confidence | AI Behavior |
|------------|------------|
| 95%+ | AI does task autonomously, notifies worker when done |
| 80-95% | AI does task, flags uncertainties for review |
| 60-80% | AI does task, shows plan before executing |
| <60% | AI asks worker how to proceed |

Confidence = (task_repetition_score × 0.6) + (human_approval_rate × 0.4)

## The Learning Loop

```
Day 1: Worker does task manually
     → OSagnent observes (pre/post hooks log everything)
     → Pattern engine clusters observations into "task_001"
     → Confidence = 30% (needs 20+ reps to climb)

Day 2-20: Worker does task, AI watches
     → Each correct repetition: confidence += 5%
     → Each human correction: logged, confidence unchanged
     → At 95%: AI takes over that task

Day 21+: AI does task autonomously
     → Worker supervises, occasional corrections
     → Corrections → permanent memory update (never repeat)

Day 90: Worker is now supervising 5 AI agents doing their old jobs
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Base OS | holaOS |
| Execution | Hermes Agent v0.13+ |
| AI Agents | The Agency (147 agents) |
| Observation | Hermes pre/post tool hooks |
| Pattern Learning | MemOS + custom pattern_engine.py |
| Memory | here.now (10GB/worker) |
| Fleet Management | JCPaid Bus |
| Budget Control | Kill Switch |
| Desktop UI | AionUi (fork as OSagnent Shell) |
| Web Intell | TinyFish |
| Automation | n8n |

## Quick Start

```bash
# 1. Start observation for a worker
hermes chat -q "osagnent start sales_rep_01"

# 2. Worker does their normal job for 1-2 weeks

# 3. Check what was learned
hermes chat -q "osagnent status"

# 4. AI starts doing learned tasks
hermes chat -q "osagnent start shift"

# 5. Worker supervises and corrects mistakes
hermes chat -q "osagnent correct task_003: don't skip the follow-up email"
```

## What's NOT Built in Phase 1

- Clone factory (Phase 2)
- Visual UI-TARS observation (Phase 2)
- Multi-worker collaboration (Phase 3)
- Self-improving agent generation (Phase 3)

## Files

```
osagnent/
├── SKILL.md                          # Hermes skill definition
├── MVP_SPEC.md                       # This file
├── observe/
│   ├── osagnent_observe.py          # Hermes pre/post hook plugin
│   └── plugin.yaml                   # Plugin manifest
└── core/
    └── pattern_engine.py             # Pattern recognition + confidence scoring
```

---

## Phase 2: Auto-Learn Pipeline (TO DO)

### What Phase 2 Does
Connects the observe layer to the pattern engine and skill generator — so OSagnent goes from WATCHING to DOING automatically.

### Phase 2 Architecture
```
observe/          pattern_engine/       generate/
─────────       ────────────────      ─────────
tool_logs   →   cluster_observations   →   generate_skill
session_data →   score_confidence    →   test_skill  
                task_sequences        →   deploy_skill
                                       →   request_approval
```

### Phase 2 Files to Build
1. `observe/auto_export.py` — exports logs in pattern_engine format
2. `pattern_engine/learn.py` — batch learning from multiple sessions
3. `generate/skill_generator.py` — creates Hermes SKILL.md from patterns
4. `generate/self_improve.py` — refines skills from corrections

### Phase 2 Status
STATUS: NOT STARTED
PRIORITY: HIGH
