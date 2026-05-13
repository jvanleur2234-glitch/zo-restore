# Workflow: Idea to Deploy

Full lifecycle from a raw idea to a running, deployed, monitored app.

## Invoke

```
tell hermes: start a new app
tell hermes: run the idea-to-deploy workflow
```

## Steps

### 1. clarify-requirements
Ask 7 structured questions. Save answers to Hermes memory.
Do not proceed until all 7 are answered.

### 2. product-brief
Generate product brief from requirements. Save to memory and PRODUCT_BRIEF.md.
If there are open questions, resolve them before continuing.

### 3. Design (human step)
Open claude.ai/design. Describe what you are building.
Export design decisions to `design-output.md` in the project root.
This step is optional — skip if the project is purely backend.

### 4. design-handoff (if design step was done)
Convert design-output.md to IMPLEMENTATION_SPEC.md.
Save spec to Hermes memory.

### 5. choose-engine
Route to Claude Code or Codex based on task complexity.
For a new app from scratch: almost always Claude Code.

### 6. implement-with-claude-code or implement-with-codex
Pass full context (brief + spec + architecture decisions) to the coding engine.
Wait for implementation to complete.

### 7. deploy-to-vercel
Run pre-deploy checklist. Deploy. Capture URL.

### 8. connect-supabase (if database is needed)
Link Supabase project. Push migrations. Add env vars to Vercel.

### 9. send-notification
Send Slack notification with deployment URL.

### 10. setup-monitoring (first deploy only)
Configure Sentry. Document Uptime Kuma setup.

### 11. post-deploy-followup
Health check. Log deployment. Confirm monitoring.

## Resuming

If the session ends mid-workflow:
```
tell hermes: we were running idea-to-deploy for [project].
We completed [last step]. Continue from [next step].
```

Hermes loads prior memory and continues.

## Variations

**Backend-only project (no UI):** Skip steps 3 and 4.
**Existing codebase (no new requirements):** Start at step 5.
**Re-deploy after a change:** Start at step 5, skip to step 7 after implementation.
