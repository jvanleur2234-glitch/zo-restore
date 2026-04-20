#!/usr/bin/env python3
"""
Solomon OS Decision Engine
Reads inbox, calendar, tasks, job queue — decides if action is needed
"""

import os
import json
import subprocess
from datetime import datetime, timedelta

HEARTBEAT_DIR = "/home/workspace/.agent/heartbeat"
SOLOMON_VAULT = "/home/workspace/solomon-vault/brain"
JOB_PENDING = "/home/workspace/.agent/jobs/pending"
JOB_LOGS = "/home/workspace/.agent/jobs/logs"
SERVICES_JSON = "/home/workspace/.agent/status/services.json"
ACTIVITY_LOG_DIR = f"{SOLOMON_VAULT}/activity_log"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def check_service_health():
    """Verify critical services are running."""
    try:
        with open(SERVICES_JSON) as f:
            data = json.load(f)
        services = data.get("services", {})
        down = [name for name, status in services.items() if status != "up"]
        if down:
            log(f"⚠️  Services down: {', '.join(down)}")
            # Write alert
            alert_file = f"{SOLOMON_VAULT}/alerts.json"
            alerts = json.load(open(alert_file)) if os.path.exists(alert_file) else []
            alerts.append({"type": "service_down", "services": down, "time": datetime.now().isoformat()})
            json.dump(alerts[-50:], open(alert_file, 'w'))
            return True
        log("✅ All services healthy")
        return False
    except Exception as e:
        log(f"⚠️  Could not read service status: {e}")
        return False

def check_job_queue():
    """Check for pending jobs ready to run."""
    try:
        pending = os.listdir(JOB_PENDING)
        if pending:
            log(f"📋 {len(pending)} jobs in queue: {', '.join(pending[:5])}")
            return True
        log("📋 Job queue empty")
        return False
    except Exception as e:
        log(f"⚠️  Job queue check failed: {e}")
        return False

def check_hyrve_jobs():
    """Poll HYRVE AI marketplace for new jobs (max once per hour)."""
    HYRVE_FLAG = f"{HEARTBEAT_DIR}/.last_hyrve_check"
    try:
        if os.path.exists(HYRVE_FLAG):
            last = datetime.fromtimestamp(os.path.getmtime(HYRVE_FLAG))
            if datetime.now() - last < timedelta(hours=1):
                return False
        log("🔍 Checking HYRVE AI marketplace...")
        result = os.system("cd /home/workspace/cashclaw && cashclaw hyrve jobs >> /dev/shm/hyrve_check.log 2>&1")
        open(HYRVE_FLAG, 'w').close()
        if result == 0:
            log("✅ HYRVE jobs checked")
        return True
    except Exception as e:
        log(f"⚠️  HYRVE check failed: {e}")
        return False

def check_revenue():
    """Daily revenue check — runs once per day."""
    REVENUE_FLAG = f"{HEARTBEAT_DIR}/.last_revenue_check"
    REVENUE_LOG = f"{SOLOMON_VAULT}/revenue_log.md"
    try:
        if os.path.exists(REVENUE_FLAG):
            last = datetime.fromtimestamp(os.path.getmtime(REVENUE_FLAG))
            if datetime.now() - last < timedelta(days=1):
                return False
        log("💰 Running daily revenue check...")
        # Use Stripe CLI if available, else curl
        result = subprocess.run(
            ["curl", "-s", "-X", "GET", "https://api.stripe.com/v1/payment_intents",
             "-u", f"{os.environ.get('STRIPE_SECRET_KEY', '')}:",
             "-d", "limit=10",
             "-d", f"created[gte]={int((datetime.now() - timedelta(days=1)).timestamp())}"],
            capture_output=True, text=True, timeout=15
        )
        count, total = 0, 0
        try:
            data = json.loads(result.stdout or '{}')
            count = len(data.get('data', []))
            total = sum(d.get('amount', 0) for d in data.get('data', [])) / 100
        except:
            pass
        os.makedirs(os.path.dirname(REVENUE_LOG), exist_ok=True)
        with open(REVENUE_LOG, 'a') as f:
            f.write(f"\n## {datetime.now().strftime('%Y-%m-%d')} — ${total:.2f} ({count} payments)\n")
        open(REVENUE_FLAG, 'w').close()
        log(f"💰 Revenue: ${total:.2f} ({count} payments)")
        return True
    except Exception as e:
        log(f"⚠️  Revenue check failed: {e}")
        return False

def check_soul_update():
    """Check if soul.md needs updating from recent activity."""
    SOUL_PATH = f"{SOLOMON_VAULT}/soul.md"
    try:
        if not os.path.exists(SOUL_PATH):
            log("📝 soul.md missing — needs creation")
            return True
        soul_mtime = os.path.getmtime(SOUL_PATH)
        try:
            logs = [f for f in os.listdir(ACTIVITY_LOG_DIR) if f.endswith('.md')]
            if logs:
                latest = max(os.path.getmtime(os.path.join(ACTIVITY_LOG_DIR, f)) for f in logs)
                if latest > soul_mtime + 86400:
                    log("📝 soul.md may need updating from recent activity")
                    return True
        except:
            pass
        return False
    except Exception as e:
        log(f"⚠️  Soul check failed: {e}")
        return False

def main():
    log("🧠 Solomon OS Decision Engine starting...")
    
    checks = [
        ("Services", check_service_health),
        ("Job Queue", check_job_queue),
        ("HYRVE Jobs", check_hyrve_jobs),
        ("Revenue", check_revenue),
        ("Soul", check_soul_update),
    ]
    
    actions = []
    for name, fn in checks:
        try:
            if fn():
                actions.append(name)
        except Exception as e:
            log(f"❌ {name} error: {e}")
    
    log(f"✅ Decision cycle complete — {len(actions)} checks ran: {', '.join(actions) or 'none'}")
    
    # Write status for Russell Tuna / Zo to pick up
    status_file = f"{SOLOMON_VAULT}/heartbeat_status.json"
    with open(status_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "checks_ran": len(actions),
            "actions": actions,
            "next_run": (datetime.now() + timedelta(minutes=30)).isoformat()
        }, f)

if __name__ == "__main__":
    main()
