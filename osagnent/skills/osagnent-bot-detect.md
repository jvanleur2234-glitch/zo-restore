---
name: osagent-bot-detect
description: Detects if a Telegram user is a bot. Checks username patterns, verifies via Telegram Bot API. Auto-responds to Joseph if he messages a bot.
compatibility: Hermes Agent v0.13+
---

# OSagent Bot Detection

## What It Does

Detects if a Telegram user/chat is a bot before or after Joseph messages them.

## Bot Detection Signals

1. **Username pattern** — ends in `bot` (e.g., `@SomeBotBot`)
2. **No phone number** — bots don't have phone numbers in Telegram
3. **"Bot" type** — Telegram API returns `"type": "bot"` for bot accounts
4. **Instant response** — bots reply in <100ms (behavioral)
5. **Known bot list** — HERE memory stores confirmed bot IDs

## Auto-Response Flow

```
Joseph messages @unknown_user
  → Check username for "bot" suffix
  → Query Telegram API: getChat(chat_id)
  → If type == "bot" → auto-reply to Joseph: "⚠️ That's a bot"
  → Store in HERE memory as known bot
  → If human → normal flow continues
```

## Usage

```bash
# Check if a username is a bot
hermes chat -q "Is @SomeUsernameBot a bot?"

# Check a chat ID
hermes chat -q "Check if chat 123456789 is a bot"

# Add a bot to known list
hermes chat -q "Add @KnownSpamBot to bot list"

# Scan a group for bots
hermes chat -q "Scan this group for bot accounts"
```

## Skills Used

- `telegram-bot-detect` — core detection logic
- `telegram-auto-reply` — sends warning to Joseph
- `here-now-memory` — stores bot名单 in 10GB memory
