"""Poll HYRVE AI marketplace for new jobs (max once per hour)."""
import os
from datetime import datetime, timedelta

HEARTBEAT_DIR = "/home/workspace/.agent/heartbeat"
HYRVE_FLAG = f"{HEARTBEAT_DIR}/.last_hyrve_check"
JOB_LOGS = "/home/workspace/.agent/jobs/logs"

def run():
    try:
        if os.path.exists(HYRVE_FLAG):
            last = datetime.fromtimestamp(os.path.getmtime(HYRVE_FLAG))
            if datetime.now() - last < timedelta(hours=1):
                return False, "HYRVE checked recently, skipping"
        # Run CashClaw HYRVE check
        result = os.system("cd /home/workspace/cashclaw && cashclaw hyrve jobs >> /dev/shm/hyrve_check.log 2>&1")
        open(HYRVE_FLAG, 'w').close()
        if result == 0:
            return True, "HYRVE marketplace checked"
        return False, "HYRVE check completed with issues"
    except Exception as e:
        return False, f"HYRVE check failed: {e}"
