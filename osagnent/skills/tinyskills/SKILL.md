---
name: tinyskills
description: TinyFish self-writing skill — agents can research any topic and write their own SKILL.md files autonomously. Use when you need to learn something new, create a new capability, or improve your existing skills.
version: 1.0.0
source: https://github.com/tinyfish-io/tinyfish-cookbook/tree/main/skills/tinyskills
---

# TinySkills — Self-Writing Skill Generator

## What This Does
Your agent uses TinyFish's free Search + Fetch API to research any topic, then writes production-ready SKILL.md files autonomously.

## How to Use
1. Get your free API key: https://accounts.tinyfish.ai/sign-in?redirect_url=https%3A%2F%2Fagent.tinyfish.ai%2Fapi-keys
2. Set: `export TINYFISH_API_KEY=your_key`
3. Send your agent: "tinyskills" or "write me a skill about [topic]"

## Process
1. Use TinyFish Search to research the topic
2. Use TinyFish Fetch to get detailed documentation
3. Write a production-ready SKILL.md based on findings
4. Install the new skill to ~/.hermes/skills/

## Commands
- `tinyskills` — start self-improvement cycle
- `tinyskills <topic>` — write a specific skill about <topic>

## Self-Improvement Loop
The agent can continuously improve itself by:
1. Identifying knowledge gaps
2. Researching via TinyFish API
3. Writing new skills to fill gaps
4. Installing and testing new skills
5. Reporting back what was learned

## Example Workflow
"I found a gap in my knowledge about video editing. Research it and write me a skill."
→ Agent uses TinyFish to learn video editing
→ Agent writes SKILL.md for video editing
→ Agent installs it and reports capability added

## API (Free)
- Search: https://api.tinyfish.ai/v1/search?query=...
- Fetch: https://api.tinyfish.ai/v1/fetch?url=...
- Credits: 500 free on signup
