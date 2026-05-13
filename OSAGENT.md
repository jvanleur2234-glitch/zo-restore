# OSagent — Complete Project History

> Last updated: 2026-05-13
> Status: ACTIVE BUILD
> Repo: `https://github.com/jvanleur2234-glitch/zo-restore`
> Brain: `/home/workspace/solomon-vault/`
> Working dir: `/home/workspace/osagnent/`

---

## WHAT OSAGENT IS

**OSagent** watches any worker doing any task with any tool, learns the patterns, generates an AI agent to replicate that job, and clones itself as a workforce per department — all running LOCAL on the customer's machine.

**The mission:** Build once, employ forever. One human trains it, it clones itself across an entire company.

**The insight from Joseph (April 30, 2026):**
> "Workers should be self-evolving. Self-correcting. Self-improving. 
> Not just responding. They should learn from their mistakes. 
> If they do something wrong and the human corrects them — they remember. 
> They get better. They adapt."

---

## COMPLETE STACK

### Base Layer
- **Hermes Agent** (v0.13+ VPS/24/7) — orchestration layer
- **here.now** — 10GB per-client permanent memory
- **The Agency** — 147 AI agents (cloned from `TheMeganews/agency`)
- **holaOS** — desktop agent OS (cloned, local-first)
- **Paperclip** — inter-agent communication
- **JCPaid Bus** — fleet dispatch per client

### OSagent 5 Layers
| Layer | Component | Status |
|-------|-----------|--------|
| 🦾 Body | Hermes `computer-use` + UI-TARS | ✅ Active |
| 👀 Observe | Hermes plugin (pre/post tool hooks) | ✅ Active |
| 🧠 Auto-learn | Pattern engine → agent generator | ✅ Active |
| 💾 Memory | here.now 10GB/client | ✅ Connected |
| 🗣️ Voice | Voice layer skill | ✅ Active |

### Oh My Hermes (CTO Stack)
Installed from: `Salomondiei08/oh-my-hermes`
- 23 skills (clarify-requirements, product-brief, deploy-to-vercel, security-review, etc.)
- 6 agent roles (CTO, PM, Dev, Security, QA, Ops)
- 5 workflows (cto-loop, idea-to-deploy, design-to-code, github-ops, deploy-and-monitor)

### Competitor Intelligence
- **HermesOS** ($9.99-$19.99/mo, crypto required, cloud-only) — We win on flat $299, no crypto, holaOS desktop, here.now permanent memory
- **AgentForge** — FORGE immediately (new AI paradigm)
- **Browser-Hawk / Scarf** — Desktop observability layer for OSagnent
- **FLOCI** — ONE specific use case for OSagnent: legal AI
- **Huly** — Self-hosted Workstack alternative, good UI reference
- **Noustiny** — Zero-Employee blueprint (exactly what JCPaid is)
- **TimesFM** — forecasting model, repomix for context compression
- **OpenManus / Flowise** — Agentic workflow foundations
- **vllm-studio** — local vLLM UI, good for HERE integration
- **UI-TARS-desktop** — THE observation layer OSagnent needs
- **Orgo AI** — Demo everyone is talking about (agent uses tools in real-time)
- **Tinyfish** — Web intelligence for Hermes (browser + fetch + grep)

### OSagnent Integrations
- **AionUi** — Desktop agent UI (Electron + React)
- **dflash** — Block diffusion for screen understanding
- **Fusion** — Agentic workflow framework (3,291 lines, sophisticated)
- **DeepSwarm 2** — Peer-to-peer agent swarm
- **CubeSandbox** — Cloud browser infrastructure
- **ClawSync** — Task mirroring between AI platforms

---

## KEY DECISIONS MADE

### Project Name: OSagent (not OSagnent)
- OSagnent = the architecture/methodology
- OSagent = the product name (simpler, clearer)
- Keep both in documentation but product = OSagent

### What OSagent is NOT
- NOT Hermes OS (separate project)
- NOT just Hermes customization
- NOT a chatbot
- NOT cloud-only

### Business Model: JCPaid
- $299/month flat — AI employees for SMBs
- No per-seat pricing
- here.now 10GB permanent memory included
- holaOS desktop access
- No crypto required (vs HermesOS)
- First target: Sioux Falls businesses (HVAC, real estate)

### Kill Switch Built
- Local HTTP API at `http://localhost:5015/`
- Hermes plugin kills unauthorized tool calls
- Budget tracking per agent
- Confidence-based autonomy

### Confidence Model
| Confidence | AI Behavior |
|------------|-------------|
| 95%+ | AI does task autonomously, notifies human when done |
| 80-95% | AI does task, flags uncertainties for human review |
| 60-80% | AI does task, shows full plan before executing |
| <60% | AI asks human how to proceed |

---

## WHAT WAS BUILT

### Phase 1 (COMPLETED May 8-13)
- ✅ OSagnent SKILL.md — full architecture documented
- ✅ Observe plugin — Hermes pre/post tool hooks
- ✅ Pattern engine — groups observations into task workflows
- ✅ Agent generator — converts learned patterns → Hermes SKILL.md
- ✅ Voice layer skill — voice interaction for approvals
- ✅ Hermes plugin registration + config updates
- ✅ Kill switch API + Hermes integration
- ✅ Oh My Hermes CTO stack (23 skills + 6 agents + 5 workflows)
- ✅ Easy install scripts (Mac, Linux, Windows)
- ✅ Auto-learn pipeline
- ✅ Phase 2 auto-learn loop

### Phase 2 (IN PROGRESS)
- Pattern engine on observation data
- HERE memory integration
- First learned skill generation

---

## TELEGRAM BOT DETECTION FEATURE

### What Joseph Wants
Joseph wants a way to detect if Telegram profiles are bots before messaging them. Specifically:
- When Joseph messages something, if it's a bot → auto-respond and tell him
- If it's a human → normal flow

### What's Technically Possible

**What Telegram bots look like:**
- Username ends in `bot` (e.g., `@SomeBotBot`)
- Official bots have verified badges
- Bot accounts don't show "last seen" — they show "bot" instead

**What we CAN'T do reliably:**
- Detect if a "human" account is actually a bot (no reliable signal)
- Access other users' phone contacts
- Force bots to identify themselves externally

**What we CAN build:**
1. **Verification bot** — A Telegram bot Joseph adds, that:
   - When someone DMs it, checks if they're a bot (by username pattern)
   - Responds with "✅ Human verified" or "⚠️ Bot detected"
   - Can be added to groups and scan members

2. **Auto-response bot for Joseph's Telegram:**
   - When Joseph messages a contact, if the contact is a known bot → bot replies to Joseph automatically
   - Stores bot名单 in HERE memory

3. **Group bot scanner:**
   - Add bot to any Telegram group
   - On join, scans all members
   - Reports bot accounts in the group

### Implementation Options

**Option A: Telegram Bot API approach (recommended)**
- Create a bot via @BotFather
- Use `getChat` and `getChatMember` API calls
- Can detect if a username contains "bot" or has no phone number
- Limitations: Telegram doesn't expose "is bot" flag via Bot API for regular users

**Option B: Behavioral detection (stretch)**
- Bots respond instantly (0ms delay)
- Bots always reply in same format
- Bots don't have "last seen" — shows "bot" instead
- Not reliable for sophisticated bots

**Option C: Manual bot list (simplest)**
- HERE memory stores known bot usernames/IDs
- When Joseph messages anyone, system checks list
- Auto-reply if match found
- Joseph adds to list over time

---

## FILE STRUCTURE

```
osagnent/
├── AGENTS.md              # Build status
├── MVP_SPEC.md            # Full spec
├── SKILL.md               # Skills + Oh My Hermes integration
├── README.md              # Project overview
├── INSTALL.mac.sh         # Mac install
├── INSTALL.linux.sh       # Linux install
├── INSTALL.windows.ps1    # Windows install
├── osagnent.py            # Main orchestrator
├── core/
│   ├── pattern_engine.py  # Observation → patterns
│   ├── agent_generator.py # Patterns → skills
│   └── skill_generator.py # Meta-skill creator
├── agents/
│   ├── cto.md            # CTO agent
│   ├── pm.md             # PM agent
│   ├── dev.md            # Dev agent
│   ├── security.md        # Security agent
│   ├── qa.md             # QA agent
│   └── ops.md            # Ops agent
├── skills/
│   ├── osagnent-observe.md
│   ├── osagnent-computer-use.md
│   ├── osagnent-voice.md
│   └── osagnent-auto-learn.md
├── workflows/
│   ├── cto-loop.md
│   ├── idea-to-deploy.md
│   ├── design-to-code.md
│   ├── github-ops.md
│   └── deploy-and-monitor.md
├── observe/
│   └── observe.py         # Hermes plugin
├── plugins/
│   ├── osagnent-observe/
│   └── osagnent-cua/
└── config/
    └── osagnent.yaml
```

---

## NEXT STEPS

1. **Bot detection bot** — Build Telegram bot that verifies other bots
2. **HERE memory integration** — Connect 10GB per-client memory
3. **UI-TARS screen capture** — Desktop observation layer
4. **Clone factory** — Department-specific workforce deployment
5. **First paid client** — HVAC Jon or Sioux Falls real estate

---

*OSagent: Build once, employ forever.*