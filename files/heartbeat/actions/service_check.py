"""Check service health and alert if anything is down."""
import json, os

SERVICES_JSON = "/home/workspace/.agent/status/services.json"
ALERT_FILE = "/home/workspace/solomon-vault/brain/alerts.json"

def run():
    try:
        with open(SERVICES_JSON) as f:
            services = json.load(f)
        down = [s for s in services if s.get("status") != "up"]
        if down:
            msg = f"Services down: {', '.join([s['name'] for s in down])}"
            # Write alert
            alerts = []
            if os.path.exists(ALERT_FILE):
                with open(ALERT_FILE) as f:
                    alerts = json.load(f)
            alerts.append({"type": "service_down", "message": msg, "time": str(__import__('datetime').datetime.now())})
            with open(ALERT_FILE, 'w') as f:
                json.dump(alerts[-50:], f)  # keep last 50
            return True, msg
        return False, "All services healthy"
    except Exception as e:
        return False, f"Service check skipped: {e}"
