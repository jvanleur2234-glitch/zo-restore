---
name: osagnent-voice
description: OSagnent voice interaction layer — speaks learned tasks, narrates agent actions, asks for approval via voice
compatibility: Hermes Agent v0.13+
---

# OSagnent Voice Layer

## What It Does

- Speaks learned tasks aloud to the worker
- Narrates what the AI agent is doing in real-time
- Asks for approval via voice confirmation ("Sounds good?", "Should I continue?")
- Reports confidence level before execution

## Voice Commands

- "Start OSagnent" → Begin observation session
- "What did you learn?" → Reports current pattern knowledge
- "Run [task name]" → Executes learned task
- "How confident are you?" → Reports confidence per task
- "Approve [task]" → Human approves task for autonomous execution
- "Stop observing" → Ends session, generates patterns

## Confidence Speech

| Confidence | What OSagnent Says |
|-----------|-------------------|
| 95%+ | "I'm ready to do this one myself. Starting now." |
| 80-95% | "I can handle this, but I'll flag anything I'm unsure about." |
| 60-80% | "Here's my plan. Should I proceed?" |
| <60% | "I'd like your guidance on this one. What should I do?" |

## Status

Phase 1 ✓ — Built. Hooks into Hermes Agent for real-time voice feedback.
