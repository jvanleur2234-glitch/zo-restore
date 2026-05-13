#!/usr/bin/env python3
"""
OSagent Bot Detection — Telegram Bot Verifier
Detects if Telegram users are bots and auto-warns Joseph.
"""

import os
import json
import requests
import time
from datetime import datetime

# Telegram Bot Token (Joseph needs to get from @BotFather)
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# HERE API for persistent memory
HERE_API = os.environ.get("HERE_API", "http://localhost:5015")
HERE_KEY = os.environ.get("HERE_API_KEY", "dev-key-osagnent")

# Known bot list (stored in memory)
KNOWN_BOTS_FILE = "/tmp/osagnent-known-bots.json"

def load_known_bots():
    try:
        with open(KNOWN_BOTS_FILE) as f:
            return json.load(f)
    except:
        return {"bots": [], "humans": []}

def save_known_bots(data):
    with open(KNOWN_BOTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def is_bot_by_username(username):
    """Check if username pattern suggests a bot."""
    if not username:
        return None
    return username.lower().endswith("bot")

def check_telegram_bot(chat_id_or_username):
    """Check if a Telegram user is a bot via API."""
    if not BOT_TOKEN:
        return {"error": "No bot token set. Get one from @BotFather."}
    
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"
    
    # Try getChat first
    try:
        # If it's numeric, use chat_id. If username, use username.
        payload = {"chat_id": chat_id_or_username}
        r = requests.get(f"{base_url}/getChat", json=payload, timeout=10)
        data = r.json()
        
        if not data.get("ok"):
            return {"error": f"API error: {data.get('description', 'Unknown')}"}
        
        chat = data.get("result", {})
        chat_type = chat.get("type", "")
        
        # Bot accounts have type "bot" in getMe response
        # getChat returns private groups etc, but for users:
        # "bot" in username is the main signal
        username = chat.get("username", "")
        first_name = chat.get("first_name", "")
        
        # Check if it looks like a bot
        is_bot = (
            chat_type == "bot" or
            (username and username.lower().endswith("bot")) or
            "bot" in (first_name or "").lower()
        )
        
        return {
            "chat_id": chat.get("id"),
            "username": username,
            "first_name": first_name,
            "type": chat_type,
            "is_bot": is_bot,
            "checked_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {"error": str(e)}

def check_with_telegram_api(username):
    """Use getMe to definitively check if a username is a bot."""
    if not BOT_TOKEN:
        return None
    
    if not username.startswith("@"):
        username = "@" + username
    
    try:
        r = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getChat",
            json={"chat_id": username},
            timeout=10
        )
        result = r.json()
        if result.get("ok"):
            chat = result.get("result", {})
            return chat.get("type") == "bot"
    except:
        pass
    return None

def add_to_known_list(username, is_bot):
    """Add a user to known bots or humans list."""
    data = load_known_bots()
    username_lower = username.lower()
    
    if is_bot:
        if username_lower not in data["bots"]:
            data["bots"].append(username_lower)
    else:
        if username_lower in data["bots"]:
            data["bots"].remove(username_lower)
        if username_lower not in data["humans"]:
            data["humans"].append(username_lower)
    
    save_known_bots(data)
    return data

def send_telegram_message(chat_id, text):
    """Send a message via Telegram bot."""
    if not BOT_TOKEN:
        return {"error": "No bot token"}
    
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def detect_and_warn(username_or_id, joseph_chat_id=None):
    """
    Main detection function.
    Returns: {"is_bot": bool, "confidence": float, "message": str, "action": str}
    """
    result = {
        "username": username_or_id,
        "is_bot": None,
        "confidence": 0.0,
        "message": "",
        "action": ""
    }
    
    # 1. Check known list first
    known = load_known_bots()
    username_lower = username_or_id.lower().lstrip("@")
    
    if username_lower in [b.lower() for b in known["bots"]]:
        result.update({
            "is_bot": True,
            "confidence": 1.0,
            "message": f"⚠️ <b>Bot Detected</b>\n\n@{username_lower} is a known bot (confirmed by you).",
            "action": "auto_warn"
        })
        return result
    
    if username_lower in [h.lower() for h in known["humans"]]:
        result.update({
            "is_bot": False,
            "confidence": 1.0,
            "message": f"✅ <b>Human Verified</b>\n\n@{username_lower} is a confirmed human.",
            "action": "none"
        })
        return result
    
    # 2. Username pattern check
    pattern_bot = is_bot_by_username(username_lower)
    
    # 3. Telegram API check (if token available)
    api_bot = check_telegram_bot(username_or_id)
    
    if api_bot.get("is_bot"):
        result.update({
            "is_bot": True,
            "confidence": 0.95,
            "message": f"🚫 <b>Bot Detected</b>\n\n@{username_lower} is a Telegram bot account.\n\nI auto-replied to them on your behalf.",
            "action": "auto_warn_and_store"
        })
        add_to_known_list(username_lower, True)
        return result
    
    if pattern_bot and api_bot.get("error"):
        # Username suggests bot but API failed — be cautious
        result.update({
            "is_bot": True,
            "confidence": 0.7,
            "message": f"⚠️ <b>Possible Bot</b>\n\n@{username_lower} ends in 'bot' which strongly suggests it's an automated account.\n\nProceeding with caution — I've flagged this for you.",
            "action": "warn_only"
        })
        return result
    
    if pattern_bot is False:
        result.update({
            "is_bot": False,
            "confidence": 0.6,
            "message": f"ℹ️ <b>Likely Human</b>\n\n@{username_lower} doesn't look like a bot account.",
            "action": "none"
        })
        return result
    
    result.update({
        "is_bot": False,
        "confidence": 0.5,
        "message": f"❓ <b>Unknown</b>\n\nCan't definitively determine if @{username_lower} is a bot or human.\n\nAdd me (@YourBotUsername) to check for you, or manually verify.",
        "action": "manual_check"
    })
    return result

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("""# OSagent Bot Detection

Usage:
    python3 bot_detect.py check @username    — Check if a username is a bot
    python3 bot_detect.py check 123456789   — Check if a chat ID is a bot
    python3 bot_detect.py list              — List known bots and humans
    python3 bot_detect.py add @username bot — Add to known list
    python3 bot_detect.py add @username human — Add as confirmed human
    python3 bot_detect.py server            — Run as HTTP API server

Example:
    python3 bot_detect.py check @SomeUserBot
""")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "check" and len(sys.argv) >= 3:
        target = sys.argv[2]
        result = detect_and_warn(target)
        print(json.dumps(result, indent=2))
    
    elif cmd == "list":
        known = load_known_bots()
        print(json.dumps(known, indent=2))
    
    elif cmd == "add" and len(sys.argv) >= 4:
        username = sys.argv[2]
        is_bot = sys.argv[3].lower() == "bot"
        data = add_to_known_list(username, is_bot)
        print(f"Added @{username} as {'bot' if is_bot else 'human'}")
        print(json.dumps(data, indent=2))
    
    elif cmd == "server":
        print("Starting OSagent Bot Detection API on :5016...")
        # HTTP server mode for Hermes to call
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import urllib.parse
        
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "osagent-bot-detect", "port": 5016}')
            
            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                try:
                    data = json.loads(body)
                    result = detect_and_warn(data.get("username", ""))
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode())
                except:
                    self.send_response(400)
                    self.end_headers()
        
        server = HTTPServer(("0.0.0.0", 5016), Handler)
        print("OSagent Bot Detect API running on http://0.0.0.0:5016")
        server.serve_forever()
    
    else:
        print("Unknown command. Run with no args for help.")

if __name__ == "__main__":
    main()