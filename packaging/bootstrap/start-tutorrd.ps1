<#
    TutorRD - Start the app
    -----------------------
    Double-click the "TutorRD" shortcut on your Desktop (which runs this file).

    What this does:
      1. Starts the local AI engine (Engine Manager) in the background.
      2. Starts the TutorRD app (backend + web page).
      3. Opens your web browser to the tutor once it is ready.

    To STOP TutorRD: close this window, or press Ctrl+C. Everything shuts
    down cleanly, including the background AI engine.
#>

$ErrorActionPreference = "Stop"

# --- small, quiet output helpers -------------------------------------------
function Say($m)  { Write-Host $m -ForegroundColor Cyan }
function Ok($m)   { Write-Host $m -ForegroundColor Green }
function Warn($m) { Write-Host $m -ForegroundColor Yellow }

# Project root is two folders up from packaging\bootstrap\.
$ScriptDir = $PSScriptRoot
if (-not $ScriptDir) { $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
$RepoRoot  = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path

# Ports (defaults read from the app; kept here so we can wait/open the browser).
$FrontendPort = 3782   # the tutor web page you open
$BackendPort  = 8001   # the app's API (internal)
$BridgePort   = 8000   # the local AI engine (internal)
$AppUrl       = "http://localhost:$FrontendPort"

Say "Starting TutorRD..."
Set-Location $RepoRoot
$env:DEEPTUTOR_HOME = $RepoRoot

# ---------------------------------------------------------------------------
# 1. Start the local AI engine (Engine Manager) if a model is present.
# ---------------------------------------------------------------------------
$modelsDir = Join-Path $RepoRoot "data\models"
$model = Get-ChildItem -Path $modelsDir -Filter *.litertlm -ErrorAction SilentlyContinue |
         Select-Object -First 1

$bridge = $null
if ($model) {
    $env:LITERTLM_MODEL_PATH = $model.FullName
    Say "Starting the local AI engine..."
    $bridge = Start-Process -FilePath "uv" `
                            -ArgumentList @("run", "bridge.py") `
                            -WorkingDirectory (Join-Path $RepoRoot "litertlm") `
                            -WindowStyle Hidden -PassThru
} else {
    Warn "No local AI model was found on this PC."
    Warn "TutorRD will still open, but the tutor cannot answer until a model is"
    Warn "installed (run install.ps1 again) OR you point this browser at another"
    Warn "TutorRD PC on your network."
}

# ---------------------------------------------------------------------------
# 2. Open the browser automatically once the web page is answering.
#    (The app launcher below blocks, so we watch for readiness in the
#     background and pop the browser when the frontend port responds.)
# ---------------------------------------------------------------------------
$watcher = Start-Job -ScriptBlock {
    param($url, $port)
    for ($i = 0; $i -lt 300; $i++) {
        try {
            $client = New-Object System.Net.Sockets.TcpClient
            $client.Connect("127.0.0.1", [int]$port)
            $client.Close()
            Start-Sleep -Seconds 2   # give the page a moment to finish loading
            Start-Process $url
            break
        } catch {
            Start-Sleep -Seconds 1
        }
    }
} -ArgumentList $AppUrl, $FrontendPort

Ok "TutorRD will open at $AppUrl when it is ready (usually under a minute)."
Say "Keep this window open while you study."
Say "To stop TutorRD, close this window or press Ctrl+C."
Write-Host ""

# ---------------------------------------------------------------------------
# 3. Start the app (backend + web page). This blocks until you stop it.
# ---------------------------------------------------------------------------
try {
    uv run python scripts/start_web.py --home "$RepoRoot"
} finally {
    # Clean shutdown: stop the browser watcher and the background AI engine.
    if ($watcher) {
        Stop-Job   $watcher -ErrorAction SilentlyContinue
        Remove-Job $watcher -ErrorAction SilentlyContinue
    }
    if ($bridge -and -not $bridge.HasExited) {
        # Kill the engine AND its child python process (the /T stops the tree).
        Start-Process -FilePath "taskkill" `
                      -ArgumentList @("/PID", "$($bridge.Id)", "/T", "/F") `
                      -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue | Out-Null
    }
    Say "TutorRD has stopped. You can close this window."
}
