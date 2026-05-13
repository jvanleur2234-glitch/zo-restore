# Workflow: Design to Code

For when requirements are already clear but UI/UX design should happen before coding.

## Invoke

```
tell hermes: I have done design work. Convert it to code.
tell hermes: run the design-to-code workflow
```

## Prerequisites

- Requirements are already clear (product brief exists or requirements are well understood)
- `design-output.md` exists with exported Claude Design notes, OR you are about to do the design step now

## Steps

### 1. design-with-claude (human step)
Open claude.ai/design. Describe the feature or screen.
Export design decisions to `design-output.md`.

### 2. design-handoff
Convert design-output.md to IMPLEMENTATION_SPEC.md.
Flag any ambiguities with [NEEDS CLARIFICATION].
Save spec to Hermes memory.

### 3. Resolve [NEEDS CLARIFICATION] items
For each flagged item, ask the user and update IMPLEMENTATION_SPEC.md before continuing.

### 4. choose-engine
For a single new page or component: likely Codex.
For a multi-page feature or new subsystem: Claude Code.

### 5. implement-with-claude-code or implement-with-codex
Pass implementation spec + any relevant memory context.

## If design-output.md is missing

Ask the user: "Do you have Claude Design output ready? If yes, paste it into design-output.md. If no, open claude.ai/design first."

Do not proceed to design-handoff without design-output.md.
