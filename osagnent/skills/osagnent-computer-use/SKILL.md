---
name: osagnent-computer-use
description: |
  OSagnent computer use — control the desktop via Hermes + cua (Mac/Linux).
  Use when the human asks to control their computer, browse a site, click something, 
  fill a form, or perform desktop automation.
  Works with ANY model. Runs in background.
  
  For Mac: hermes computer-use install + hermes computer-use connect
  For Linux: wait for cua-driver release, then same commands
  
  After connect, agent can:
  - Browse web (chrome, safari)
  - Click UI elements
  - Type text
  - Read screen state
  - Execute commands
  
  Safety: Always confirm with human before destructive actions.
tools: [shell, read, write, grep, curl]
---

# OSagnent Computer Use Skill

## Activate
When human says "control my computer", "browse", "click", "use desktop", or any form of desktop automation.

## Commands

### Install (Mac/Linux)
\`\`\`bash
hermes computer-use install   # Download cua-driver
hermes computer-use connect   # Start background daemon
hermes computer-use status    # Check if connected
\`\`\`

### For Linux — wait for cua-driver release
Check https://github.com/tinybase-org/cua-driver for Linux release.

### Use
\`\`\`bash
# Check status
hermes computer-use status

# Connect to running session
hermes computer-use connect

# Show logs
hermes computer-use logs
\`\`\`

## Architecture
- OSagnent runs cua-driver in background
- Agent controls via Hermes tool calls
- Background execution — human keeps working
- Multiple agents can connect to same session

## Safety Rules
1. Confirm destructive actions (delete files, send emails)
2. Read screen before acting
3. Ask for confirmation on financial transactions
4. Log all actions to /tmp/osagnent-actions.log

## Status Check
\`\`\`bash
hermes computer-use status
cat /tmp/osagnent-actions.log
\`\`\`

## Integration
Combined with osagnent-observe skill:
- osagnent-observe: watches screen, detects patterns, triggers agents
- osagnent-computer-use: executes actions on screen

Together they form OSagnent's "eyes + body" — see then act.
