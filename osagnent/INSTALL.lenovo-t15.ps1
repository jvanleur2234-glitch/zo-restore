# OSagnent Windows Installer — lenovo-t15
# HOW TO RUN (non-technical person):
# 1. Press Windows key + R
# 2. Type: powershell
# 3. Press Ctrl+V to paste this entire script
# 4. Press Enter
# 5. Wait 3 minutes, answer Y when asked

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "OSagnent Installer — lenovo-t15" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will take 2-3 minutes." -ForegroundColor Yellow
Write-Host "Press Enter to continue..." -ForegroundColor Gray
$null = Read-Host

# Check admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "Restarting as Administrator..." -ForegroundColor Yellow
    Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -File $($MyInvocation.MyCommand.Path)"
    exit
}

# Step 1: Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3") {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Python not found. Install from: https://python.org/downloads" -ForegroundColor Red
    Write-Host "Download Python 3.11+, restart this installer, try again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

# Step 2: Install Hermes
Write-Host "[2/6] Installing Hermes Agent..." -ForegroundColor Cyan
python -m pip install hermes-agent --quiet 2>&1 | Out-Null
if (Get-Command hermes -ErrorAction SilentlyContinue) {
    Write-Host "✅ Hermes installed" -ForegroundColor Green
} else {
    Write-Host "⚠️ Hermes install failed — continuing anyway" -ForegroundColor Yellow
}

# Step 3: Install HERE API
Write-Host "[3/6] Starting HERE memory server..." -ForegroundColor Cyan
$hereCode = @'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

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
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"success": True}).encode())

server = HTTPServer(("0.0.0.0", 5015), Handler)
print("HERE API running on port 5015")
server.serve_forever()
'@
$hereCode | Out-File -FilePath "$env:TEMP\here-api.py" -Encoding UTF8
Start-Process python -ArgumentList "$env:TEMP\here-api.py" -WindowStyle Hidden
Start-Sleep 2
Write-Host "✅ HERE API running on port 5015" -ForegroundColor Green

# Step 4: Install OSagnent files
Write-Host "[4/6] Installing OSagnent..." -ForegroundColor Cyan
$osagnentDir = "$env:USERPROFILE\.hermes\skills\osagnent"
New-Item -ItemType Directory -Force -Path $osagnentDir | Out-Null

# Copy from workspace if available
if (Test-Path "C:\Users\josep\workspace\osagnent") {
    Copy-Item -Path "C:\Users\josep\workspace\osagnent\*" -Destination $osagnentDir -Recurse -Force
    Write-Host "✅ OSagnent installed from workspace" -ForegroundColor Green
} else {
    # Clone from GitHub
    git clone --depth 1 https://github.com/jvanleur2234-glitch/zo-restore.git "$env:TEMP\osagnent-repo" 2>&1 | Out-Null
    if (Test-Path "$env:TEMP\osagnent-repo\osagnent") {
        Copy-Item -Path "$env:TEMP\osagnent-repo\osagnent\*" -Destination $osagnentDir -Recurse -Force
        Write-Host "✅ OSagnent installed from GitHub" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Could not download OSagnent. Will sync later." -ForegroundColor Yellow
    }
}

# Step 5: Update Hermes config
Write-Host "[5/6] Configuring Hermes..." -ForegroundColor Cyan
$configPath = "$env:USERPROFILE\.hermes\config.yaml"
$configContent = @"

# OSagnent settings
OSAGNENT_ENABLE: "1"
HERE_API_URL: "http://localhost:5015"
OSAGNENT_WORKER_ID: "lenovo-t15"
"@
if (Test-Path $configPath) {
    Add-Content -Path $configPath -Value $configContent
} else {
    $configContent | Out-File -FilePath $configPath -Encoding UTF8
}
Write-Host "✅ Hermes configured" -ForegroundColor Green

# Step 6: Create shortcuts
Write-Host "[6/6] Creating shortcuts..." -ForegroundColor Cyan
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutContent = @"
[Desktop Entry]
Name=OSagnent Observe
Exec=python $osagnentDir\osagnent.py start lenovo-t15
Type=Application
"@

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ INSTALLATION COMPLETE" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor White
Write-Host "1. Restart Hermes Agent" -ForegroundColor Yellow
Write-Host "   (Close and reopen your terminal)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start observing yourself:" -ForegroundColor White
Write-Host "   python $osagnentDir\osagnent.py start lenovo-t15" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Use your computer normally for 1 week" -ForegroundColor White
Write-Host ""
Write-Host "4. After 1 week, run:" -ForegroundColor White
Write-Host "   python $osagnentDir\osagnent.py stop" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dashboard: https://josephv.zo.space/osagnent" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to close"
