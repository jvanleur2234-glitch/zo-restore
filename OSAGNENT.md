# OSagnent — The AI-Native Operating System for the Post-Employee Era

**Status:** CONCEPT → BUILD PHASE  
**Uniqueness:** LOCAL SELF-LEARNING ENTERPRISE AGENT  
**Last updated:** 2026-05-10

---

## The Vision

OSagnent is a self-hosted, air-gapped AI workforce that:
1. **Watches** employees for 6 months (learning all jobs)
2. **Generates** its own software tools (learned from observations)
3. **Clones** itself as a complete workforce per enterprise
4. **Never** touches the cloud — everything stays local

The AI learns how YOUR specific business operates — not generic patterns, but the actual decisions your loan officer makes, your accountant's judgment calls, your customer service scripts.

---

## Why This Is Genuinely New

| Competitor | What they do | OSagnent Enterprise difference |
|---|---|---|
| Oracle Cloud ERP | One-size-fits-all SaaS, 5yr deploy, armies of consultants | Learns how THIS specific bank operates, deploys in months |
| Microsoft 365 Copilot | Cloud AI, data leaves the building | Air-gapped, local, never touches external servers |
| IBM Watson | Generic AI, training required | Learns from watching — zero training needed |
| Accenture / consulting | Human consultants mapping processes | Self-learning agents that observe and replicate |

---

## The Stack (2026-05-10)

| Component | Tech | Purpose |
|---|---|---|
| **Core Agent** | Hermes Agent v0.13+ | Execution engine with skills system |
| **Permanent Memory** | here.now (10GB/client) | Long-term memory per employee/department |
| **Desktop UI** | UI-TARS (ByteDance) | Native OS observation layer |
| **Voice Layer** | OpenVoice / Realtime API | Natural voice I/O for the agent |
| **AWS Emulation** | Floci (MIT, 24ms startup) | Local cloud infrastructure for testing |
| **Dispatch System** | JCPaid Bus | Fleet management, kill switch, billing |
| **Browser Automation** | Agent Capsule + TinyFish | Web learning + interaction |
| **Kill Switch** | JCPaid Kill Switch (port 5015) | Budget enforcement + safety guard |

---

## The Observation Stack

1. **Screen capture** — UI-TARS (ByteDance, desktop-native)
2. **Keyboard/mouse logging** — holainput (input learning layer)
3. **File operations** — Watch every document, spreadsheet, email
4. **Decision logging** — Every "yes/no" decision employees make
5. **Workflow mapping** — Sequence of actions for every job

---

## The Learning Pipeline

```
Observation → Storage (here.now, 10GB per employee)
           → Pattern Recognition (MemOS, vector+graph)
           → Workflow Models (what does a loan officer DO all day)
           → Self-Improvement Loop (DeepSwarm, parallel training)
           → Tool Generation (OSagnent writes its own agents)
           → Clone Deployment (department-specific AI workforce)
```

---

## The Kill Switch (Safety Layer)

Every AI action logs to an external Kill Switch service:

```typescript
// Kill Switch API — http://localhost:5015
POST /register    — Register new agent with budget
POST /decision    — Pre-action approval (blocks if over budget)
POST /result      — Post-action logging
GET  /status      — Current budget usage
```

**3-Strike System:**
1. **Warning** — "You've used 80% of your budget"
2. **Soft block** — "Human approval needed for next 3 actions"
3. **Hard stop** — "Agent paused until human re-authorizes"

**Budget:** $299/mo per department = $3,588/yr  
**ROI:** One employee costs $50K+/yr. OSagnent clones that employee for $299/mo.

---

## Pricing Model

| Tier | Price | What's included |
|---|---|---|
| **First Department** | $299/mo | Core OSagnent, 1 department, unlimited agents |
| **Additional Departments** | $499/mo each | Per department clone |
| **Enterprise (custom)** | $2,000/mo+ | On-prem deployment, unlimited departments |

**Competitive against:**
- Oracle Cloud ERP: $1M+ implementation + $100K/yr maintenance
- Accenture consulting: $5M-50M per deployment
- Microsoft 365 Copilot: $30/user/mo, cloud-dependent

---

## MVP Build Status

| Component | Status |
|---|---|
| OSAGNENT.md spec | ✅ Complete |
| JCPaid Kill Switch API | ✅ Running on port 5015 |
| Hermes OSagnent Voice Plugin | ✅ Installed |
| Hermes OSagnent Observe Plugin | ✅ Installed |
| Floci (AWS emulation) | ✅ Cloned |
| Hermes v0.13.0 | ✅ Installed |
| UI-TARS Desktop | ✅ Cloned |
| OpenHuman (desktop reference) | ✅ Cloned |
| TinyFish browser skill | ✅ Installed |
| **Core OSagnent Agent** | ⏳ Waiting on 7 answers |
| **Demo Video** | ⏳ Pending MVP |

---

## The 7 Questions (MVP blockers)

1. What TYPE of worker should OSagnent learn first? (accountant, HR, customer service, loan officer, etc.)
2. What SPECIFIC tasks does that worker do daily? (be as detailed as possible)
3. What TOOLS/APPS does that worker use? (Excel, email, internal software, databases)
4. What DECISIONS do they make that a machine can't? (judgment calls, gray areas)
5. What does SUCCESS look like? (how would you measure if OSagnent did the job right)
6. Should OSagnent be LOCAL (your server) or CLOUD (Zo server)?
7. Do you want VOICE interface (talks to you) or TEXT only?

---

## Files in This Project

- `OSAGNENT.md` — This file
- `OSAGNENT_ENTERPRISE_SPEC.md` — Detailed enterprise spec
- `Skills/osagnent-voice/` — Voice layer plugin for Hermes
- `Skills/osagnent-observe/` — Observation layer plugin for Hermes
- `floci/` — AWS emulation for local testing
- `kill-switch-api.ts` — Running on port 5015

---

*OSagnent: The last operating system you'll ever need to buy.*
