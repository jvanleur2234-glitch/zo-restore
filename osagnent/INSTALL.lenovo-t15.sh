#!/bin/bash
# OSagnent One-Command Installer
# Run this on ANY computer — no technical skill needed.
# Just open Terminal, paste this ONE line, press Enter.

set -e

echo "=========================================="
echo "OSagnent Installer — lenovo-t15"
echo "=========================================="
echo ""
echo "This will take 2-3 minutes."
echo "Press Enter to continue..."
read

# Step 1: Check for Hermes
echo "[1/5] Checking Hermes Agent..."
if command -v hermes &> /dev/null; then
    echo "✅ Hermes already installed"
else
    echo "Installing Hermes Agent..."
    python3 -m pip install hermes-agent --quiet
fi

# Step 2: Install HERE API (Kill Switch)
echo "[2/5] Installing HERE API (memory server)..."
cd /tmp
cat > here-api.py << 'PYEOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

workers = {}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"workers": list(workers.values())}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode()
        data = json.loads(body)
        
        if self.path.startswith("/workers/"):
            worker_id = self.path.split("/")[2]
            if "/start" in self.path:
                workers[worker_id] = {"id": worker_id, "tool_calls": 0, "patterns": 0, "skills": 0}
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "worker": worker_id}).encode())
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True}).encode())

server = HTTPServer(("0.0.0.0", 5015), Handler)
print("HERE API running on port 5015")
server.serve_forever()
PYEOF

pkill -f "here-api.py" 2>/dev/null || true
nohup python3 /tmp/here-api.py > /dev/shm/here-api.log 2>&1 &
echo "✅ HERE API running"

# Step 3: Install OSagnent files
echo "[3/5] Installing OSagnent..."
mkdir -p ~/.osagnent
mkdir -p ~/.hermes/skills/osagnent
mkdir -p ~/.hermes/plugins/osagnent

# Download OSagnent from GitHub
if [ -d "/home/workspace/osagnent" ]; then
    cp -r /home/workspace/osagnent/* ~/.hermes/skills/osagnent/
    echo "✅ OSagnent installed from workspace"
else
    # Clone fresh
    git clone --depth 1 https://github.com/jvanleur2234-glitch/zo-restore.git /tmp/osagnent-repo
    cp -r /tmp/osagnent-repo/osagnent/* ~/.hermes/skills/osagnent/
    echo "✅ OSagnent installed from GitHub"
fi

# Step 4: Update Hermes config
echo "[4/5] Configuring Hermes..."
cat >> ~/.hermes/config.yaml << 'EOF'

# OSagnent settings
OSAGNENT_ENABLE: "1"
HERE_API_URL: "http://localhost:5015"
OSAGNENT_WORKER_ID: "lenovo-t15"
EOF

# Enable the observe plugin
if ! grep -q "osagnent" ~/.hermes/config.yaml; then
    python3 -c "
import yaml
with open('/root/.hermes/config.yaml', 'a') as f:
    yaml.dump({'plugins': {'enabled': ['osagnent', 'osagnent-observe']}}, f)
" 2>/dev/null || true
fi

echo "✅ Hermes configured"

# Step 5: Test it works
echo "[5/5] Testing..."
sleep 2
if curl -s http://localhost:5015/health | grep -q "ok"; then
    echo "✅ HERE API responding"
else
    echo "⚠️ HERE API not responding yet — this is normal"
fi

echo ""
echo "=========================================="
echo "✅ INSTALLATION COMPLETE"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Restart Hermes: hermes chat -q 'restart'"
echo "2. Start observing: python3 ~/.hermes/skills/osagnent/osagnent.py start lenovo-t15"
echo "3. Use your computer normally for 1 week"
echo "4. Run: python3 ~/.hermes/skills/osagnent/osagnent.py stop"
echo ""
echo "Dashboard: https://josephv.zo.space/osagnent"
echo ""
