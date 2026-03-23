# Zo Computer Restore Package
**For:** josephv's Zo Computer  
**Created:** 2026-03-23

This package replicates your entire Zo setup on a fresh Zo Computer.

## What's Included

| Component | Count | Notes |
|-----------|-------|-------|
| GitHub repos | 40 | All forked to your account |
| Pip packages | 60+ | Full AI/ML stack |
| Custom personas | 8 | AI Engineer, Growth Hacker, etc. |
| Scheduled agents | 2 | Morning Brief + Money Agent |
| Zo Space routes | 10+ | Full storefront + tools |
| Skills | 4 | zo-github, subagent-dev, etc. |
| Workspace config | Full | AGENTS.md, memory_db, inventory |

## Quick Restore (3 Steps)

### Step 1: On your NEW Zo Computer

```bash
# SSH into new Zo or open terminal, then:
cd ~
git clone https://github.com/josephv/zo-restore.git
cd zo-restore
chmod +x restore.sh
```

### Step 2: Authenticate GitHub
```bash
gh auth login --hostname github.com -p https -w
# Follow the prompts - open the device URL and enter the code
```

### Step 3: Run the restore
```bash
./restore.sh
```

## What Gets Restored

### ✅ Automatic
- Workspace files (AGENTS.md, REPOS_INVENTORY.md, memory_db/)
- Pip packages (prefect, langchain, browser-use, etc.)
- GitHub repo forks
- Custom personas
- Scheduled agents
- Zo Space routes (via routes.sh)

### ⚠️ Manual (after restore)
1. **Zo Space routes** — Route codes are in `routes/` directory. On new Zo, run `routes.sh` or manually recreate via Zo dashboard.
2. **Stripe** — Reconnect at Settings > Billing
3. **API keys** — Re-add secrets at Settings > Advanced
4. **OpenBotX service** — Re-register the service

## Zo Space Routes to Recreate

| Path | Type | Purpose |
|------|------|---------|
| `/` | page | PromptVault homepage |
| `/packs` | page | All prompt packs |
| `/checkout` | page | Stripe checkout |
| `/studio` | page | Game Studio AI |
| `/clone` | page | ClonePilot |
| `/spec` | page | SpecToCode |
| `/family` | page | Family baseball dashboard |
| `/watch` | page | Live game streaming |
| `/admin` | page | League admin |
| `/coach` | page | Coach scoring app |

## Files in This Package

```
zo-restore/
├── README.md              ← You are here
├── restore.sh             ← Main restore script (run this)
├── repos.sh               ← Forks all GitHub repos
├── personas.sh            ← Creates 8 custom personas
├── agents.sh              ← Schedules 2 agents
├── routes.sh              ← Restores Zo Space routes
├── requirements.txt       ← All pip packages
└── files/                 ← Workspace config files
    ├── AGENTS.md
    ├── REPOS_INVENTORY.md
    ├── memory.jsonl
    ├── HOW_TO_USE.md
    └── PROJECT_SUMMARY.md
```

## If Route Codes Don't Restore

The route codes are stored in your active Zo. If the new Zo can't restore them automatically:

1. On **THIS** Zo: I'll give you the route code for any path
2. On **NEW** Zo: Use `update_space_route()` to create it

Example:
```
update_space_route("/", "page", code="<paste code here>", public=True)
```

Just ask me for the code for any route you need.
