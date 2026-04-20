"""Check if soul.md needs updating based on recent activity."""
import os
from datetime import datetime

SOLOMON_VAULT = "/home/workspace/solomon-vault/brain"
SOUL_PATH = f"{SOLOMON_VAULT}/soul.md"
ACTIVITY_LOG_DIR = f"{SOLOMON_VAULT}/activity_log"

def run():
    try:
        if not os.path.exists(SOUL_PATH):
            return True, "soul.md missing — needs creation"
        soul_mtime = os.path.getmtime(SOUL_PATH)
        try:
            logs = [f for f in os.listdir(ACTIVITY_LOG_DIR) if f.endswith('.md')]
            if logs:
                latest = max(os.path.getmtime(os.path.join(ACTIVITY_LOG_DIR, f)) for f in logs)
                if latest > soul_mtime + 86400:
                    return True, "soul.md may need updating from recent activity"
        except:
            pass
        return False, "soul.md current"
    except Exception as e:
        return False, f"Soul check failed: {e}"
