#!/bin/bash
set -e
echo "=== Zo Computer Restore ==="

WORKSPACE="/home/workspace"
ZO_RESTORE="$WORKSPACE/zo-restore"

echo "[1/7] Syncing workspace files..."
cp -r "$ZO_RESTORE/files/"* "$WORKSPACE/" 2>/dev/null || true
echo "  ✅ Workspace files copied"

echo "[2/7] Installing pip packages..."
pip install -r "$ZO_RESTORE/requirements.txt" 2>&1 | tail -5
echo "  ✅ Packages installed"

echo "[3/7] Forking GitHub repos..."
bash "$ZO_RESTORE/repos.sh"
echo "  ✅ Repos forked"

echo "[3.5/7] Syncing zo-excellence-package (brain files, skills)..."
EXCELLENCE="$WORKSPACE/zo-excellence-package"
if [ -d "$EXCELLENCE/.git" ]; then
  cd "$EXCELLENCE"
  git pull origin main 2>&1 | tail -3
  echo "  ✅ zo-excellence-package synced"
else
  git clone https://github.com/jvanleur2234-glitch/zo-excellence-package.git "$EXCELLENCE" 2>&1 | tail -3
  echo "  ✅ zo-excellence-package cloned"
fi

echo "[4/7] Restoring Zo Space routes..."
bash "$ZO_RESTORE/routes.sh"
echo "  ✅ Space routes restored"

echo "[5/7] Creating personas..."
bash "$ZO_RESTORE/personas.sh"
echo "  ✅ Personas created"

echo "[6/7] Restoring scheduled agents..."
bash "$ZO_RESTORE/agents.sh"
echo "  ✅ Agents scheduled"

echo "[6.5/7] Setting up Solomon Heartbeat..."
mkdir -p "$WORKSPACE/.agent/heartbeat/actions"
mkdir -p "$WORKSPACE/solomon-vault/brain/activity_log"
cp -r "$ZO_RESTORE/files/heartbeat/"* "$WORKSPACE/.agent/heartbeat/" 2>/dev/null || true
chmod +x "$WORKSPACE/.agent/heartbeat/run_heartbeat.sh"
chmod +x "$WORKSPACE/.agent/heartbeat/heartbeat.sh"
chmod +x "$WORKSPACE/.agent/heartbeat/decision_engine.py"
chmod +x "$WORKSPACE/.agent/heartbeat/actions/"*.py 2>/dev/null || true
tmux new -s solomon-heartbeat -d "$WORKSPACE/.agent/heartbeat/run_heartbeat.sh" 2>/dev/null || true
echo "  ✅ Solomon Heartbeat started"

echo "[7/7] Registering services..."
bash "$ZO_RESTORE/services.sh"
echo "  ✅ Services registered"

echo ""
echo "=== RESTORE COMPLETE ==="
echo "NOTE: Re-connect GitHub with: gh auth login"
echo "NOTE: Re-configure API keys in Settings > Advanced"
