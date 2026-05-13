# Hermes Capabilities — All Installed Skills & Integrations
Last updated: 2026-05-13

## Core Hermes
- Hermes Agent v0.13.0 "The Tenacious Tapir"
- 1,223+ built-in skills
- Plugin architecture: ~/.hermes/plugins/
- Skill architecture: ~/.hermes/skills/
- Agent OS: macOS/Windows/Linux desktop control
- computer-use: full desktop automation
- Update: `hermes update`

## Self-Improvement (Critical)
- **TinyFish Search + Fetch** — Free research API (500 credits/signup)
- **TinySkills** — Hermes/OpenClaw self-writing skill. Agent researches any topic → writes SKILL.md → installs autonomously. Send "tinyskills" or "write me a skill about [topic]"
- **PLUR** — Persistent memory for agents. Local YAML at ~/.plur/. "Haiku with PLUR memory outperformed Opus without it" (2.6x better on tool routing, 10x less cost). Installed via `pip install plur-hermes`
- **Idea Workflow** — Pre-build spec pipeline: rough idea → design doc → implementation spec → build handoff. 8 stages, lite + full modes

## Memory Stack
- **HERE.now** — 10GB persistent memory per client (vector search)
- **PLUR** — Zero-cost persistent YAML, cross-tool, cross-session. Engrams with ACT-R activation/decay. Scope: global/project/cluster/service
- **Memary** — Cloned, Python venv ready

## OSagnent Skills (in osagnent/skills/)
- osagnent-voice — Voice layer (Speech to text, LLM, Text to speech pipeline)
- osagnent-observe — Observation layer (mouse tracking, screen recording, pattern learning)
- osagnent-pattern-engine — Pattern detection and learning
- osagnent-agent-generator — Generates new agent capabilities from discoveries
- osagnent-computer-use — Full desktop automation via Hermes computer-use
- osagnent-memory — Memory management (HERE.now + PLUR integration)
- tinyskills — Self-writing skill (TinyFish integration for autonomous skill creation)

## Oh My Hermes (23 skills installed)
- auto-issue-creator
- auto-pr-merger  
- bitwarden-password-manager
- bugfix
- cheatsheet-creator
- code-review
- dependency-updater
- git-suggester
- health-check
- hotkey-helper
- image-resizer
- log-reader
- pr-description-generator
- pr-summarizer
- progress-checker
- readme-improver
- repo-health-monitor
- search-codebase
- security-auditor
- shell-command-suggester
- skill-builder
- terminal-styling
- todo-to-readme
- code-cleanup

## Cloned Repos (as reference/inspiration)
- hermes-agent-idea-workflow — Pre-build spec pipeline
- plur — Local-first persistent memory for agents
- openclaude — Claude Code multi-agent orchestrator
- huly — 25,576 stars, all-in-one workspace OS
- aionui — Desktop agent UI reference
- Fusion — 3D AI workspace (React/Three.js/R3F)
- UI-TARS-desktop — Multi-agent UI control (ByteDance)
- dflash — Block diffusion for image generation
- cube-sandbox — Cross-platform desktop agent
- osagnent — The AI-Native OS project

## JCPaid Integration
- Kill Switch API: http://localhost:5015 (agent registry + budget tracking)
- Kill Switch Hermes Plugin: ~/.hermes/plugins/kill-switch/
- Auto-shutoff when budget exceeded

## API Keys Needed
- TINYFISH_API_KEY — https://accounts.tinyfish.ai/sign-in (500 free credits)
- GROQ_API_KEY — https://console.groq.com (free, fast LLM inference)