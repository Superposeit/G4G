<#
    TutorRD - First-run bootstrap installer (Windows, student edition)
    ------------------------------------------------------------------
    This script sets up everything a student needs to run TutorRD offline:
      1. Checks for uv (the tool that manages Python for us)
      2. Installs a matching Python + the app's backend
      3. Checks for Node.js and builds the web page you will see
      4. Looks at your PC's memory (RAM) and picks the right AI model
      5. Downloads that model (if your PC can host one)
      6. Puts a "TutorRD" shortcut on your Desktop

    HOW TO RUN
    ----------
    Easiest: right-click this file and choose "Run with PowerShell".
    If Windows blocks it, open PowerShell and run this one line:

        powershell -ExecutionPolicy Bypass -File install.ps1

    You only need to run this once. Running it again is safe - it skips
    anything that is already done.
#>

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Pretty, plain-language output helpers
# ---------------------------------------------------------------------------
function Write-Banner {
    Write-Host ""
    Write-Host "  ============================================================" -ForegroundColor Cyan
    Write-Host "        T u t o r R D   -   S e t u p   A s s i s t a n t"       -ForegroundColor Cyan
    Write-Host "        Your offline AI tutor. No internet needed to study."     -ForegroundColor Gray
    Write-Host "  ============================================================" -ForegroundColor Cyan
    Write-Host ""
}
function Write-Step($m) { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Write-Ok($m)   { Write-Host "    [OK]  $m" -ForegroundColor Green }
function Write-Info($m) { Write-Host "          $m" -ForegroundColor Gray }
function Write-Warn2($m){ Write-Host "    [!]   $m" -ForegroundColor Yellow }

function Pause-End {
    if ([Environment]::UserInteractive) {
        try { Read-Host "`nPress Enter to close this window" | Out-Null } catch {}
    }
}

# Stop with a plain-language cause + fix. Never leaves a raw stack trace last.
function Fail($cause, $fix) {
    Write-Host ""
    Write-Host "  ------------------------------------------------------------" -ForegroundColor Red
    Write-Host "  SETUP STOPPED" -ForegroundColor Red
    Write-Host "  What happened : $cause" -ForegroundColor Red
    if ($fix) { Write-Host "  How to fix    : $fix" -ForegroundColor Yellow }
    Write-Host "  ------------------------------------------------------------" -ForegroundColor Red
    Pause-End
    exit 1
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
try {
    Write-Banner

    # Resolve the project root. This script lives in packaging\bootstrap\, so
    # the project root is two folders up.
    $ScriptDir = $PSScriptRoot
    if (-not $ScriptDir) { $ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
    $RepoRoot  = (Resolve-Path (Join-Path $ScriptDir "..\..")).Path
    Write-Info "Project folder: $RepoRoot"

    $webPending = $false

    # -----------------------------------------------------------------------
    # 1. uv (Python runtime manager)
    # -----------------------------------------------------------------------
    Write-Step "Checking for uv (this manages Python for you)"
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Warn2 "uv is not installed on this computer."
        $consent = $false
        if ([Environment]::UserInteractive) {
            $ans = Read-Host "          Install uv now automatically? [Y/n]"
            if ($ans -eq "" -or $ans -match '^(y|yes)$') { $consent = $true }
        }
        if ($consent) {
            Write-Info "Downloading and installing uv from https://astral.sh/uv ..."
            try {
                Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
            } catch {
                Fail "Could not install uv automatically (no internet, or download blocked)." `
                     "Connect to the internet and re-run this installer, OR install uv by hand: open PowerShell and run  irm https://astral.sh/uv/install.ps1 | iex"
            }
            # Make uv visible in this same window without reopening PowerShell.
            $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
        }
        if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
            Fail "uv is required but was not found." `
                 "Install it once by opening PowerShell and running:  irm https://astral.sh/uv/install.ps1 | iex   -- then re-run this installer."
        }
    }
    Write-Ok "uv is ready ($(uv --version))"

    # -----------------------------------------------------------------------
    # 2. Python + backend dependencies
    # -----------------------------------------------------------------------
    Write-Step "Installing Python (via uv)"
    uv python install 3.12
    if ($LASTEXITCODE -ne 0) {
        Fail "uv could not install Python 3.12." `
             "Check your internet connection and re-run this installer. uv downloads Python for you."
    }
    Write-Ok "Python 3.12 is ready."

    Write-Step "Installing the TutorRD backend (this can take a few minutes)"
    Write-Info "Downloading the app's Python packages..."
    Push-Location $RepoRoot
    try {
        uv sync --extra server
        if ($LASTEXITCODE -ne 0) {
            Fail "The backend install (uv sync) did not finish." `
                 "Re-run this installer with internet access. If it keeps failing, delete the '.venv' folder inside the project and try again."
        }
    } finally { Pop-Location }
    Write-Ok "Backend installed."

    # -----------------------------------------------------------------------
    # 3. Node.js check
    # -----------------------------------------------------------------------
    Write-Step "Checking for Node.js (needed to show the app in your browser)"
    $node   = Get-Command node -ErrorAction SilentlyContinue
    $nodeOk = [bool]$node
    if ($nodeOk) {
        Write-Ok "Node.js is ready ($(node --version))"
    } else {
        Write-Warn2 "Node.js is NOT installed."
        Write-Info "TutorRD needs Node.js to display the tutor in your web browser."
        Write-Info "Install it, then run this installer again. Pick ONE of these:"
        Write-Info "    winget install OpenJS.NodeJS.LTS"
        Write-Info "  or download the LTS Windows installer from https://nodejs.org"
    }

    # -----------------------------------------------------------------------
    # 4. Web UI (build the page the student sees)
    # -----------------------------------------------------------------------
    Write-Step "Preparing the web page (the tutor screen)"
    $packagedServer = Join-Path $RepoRoot "deeptutor_web\server.js"
    $webSource      = Join-Path $RepoRoot "web\package.json"
    $webNodeModules = Join-Path $RepoRoot "web\node_modules"

    if (Test-Path $packagedServer) {
        Write-Ok "Web page is already built. Nothing to do."
    } elseif ($nodeOk -and (Test-Path $webSource)) {
        Push-Location (Join-Path $RepoRoot "web")
        try {
            if (-not (Test-Path $webNodeModules)) {
                Write-Info "Installing web building blocks (npm install)..."
                npm install
                if ($LASTEXITCODE -ne 0) {
                    Fail "npm install failed while preparing the web page." `
                         "Make sure Node.js finished installing, close and reopen PowerShell, then re-run this installer."
                }
            } else {
                Write-Info "Web building blocks already present."
            }
        } finally { Pop-Location }

        Write-Info "Building the production web page (first time only, a few minutes)..."
        Push-Location $RepoRoot
        try {
            uv run python scripts/prepare_web_package.py
            if ($LASTEXITCODE -ne 0) {
                Fail "The web page build did not finish." `
                     "Re-run this installer. If it keeps failing, open PowerShell in the 'web' folder and run 'npm install' then 'npm run build' to see the exact error."
            }
        } finally { Pop-Location }
        Write-Ok "Web page built."
    } else {
        if (-not $nodeOk) {
            Write-Warn2 "Skipping the web page build because Node.js is missing (see above)."
            Write-Info "After you install Node.js, run this installer again to finish this step."
            $webPending = $true
        } else {
            Fail "The 'web' folder is missing and there is no pre-built web page." `
                 "Re-download (clone) the TutorRD project so the 'web' folder is included, then re-run this installer."
        }
    }

    # -----------------------------------------------------------------------
    # 5. Hardware tier + model choice
    # -----------------------------------------------------------------------
    Write-Step "Checking your computer's memory (RAM)"
    $ramBytes = (Get-CimInstance Win32_ComputerSystem -ErrorAction SilentlyContinue).TotalPhysicalMemory
    if (-not $ramBytes) {
        # Fallback: add up the physical memory sticks.
        $ramBytes = (Get-CimInstance Win32_PhysicalMemory -ErrorAction SilentlyContinue |
                     Measure-Object -Property Capacity -Sum).Sum
    }
    if (-not $ramBytes -or $ramBytes -le 0) {
        Write-Warn2 "Could not read your RAM. Assuming the LITE tier to be safe."
        $ramGB = 4.0
    } else {
        $ramGB = [math]::Round($ramBytes / 1GB, 1)
    }
    Write-Info "Detected RAM: $ramGB GB"

    if ($ramGB -ge 8)      { $tier = "full" }
    elseif ($ramGB -ge 4)  { $tier = "lite" }
    else                   { $tier = "client" }

    $doDownload = $false
    switch ($tier) {
        "full" {
            Write-Ok "Tier: FULL (8 GB or more). Your PC can host the tutor comfortably."
            Write-Info "Best model for you: Gemma 4 E2B in GGUF (Q4_K_M) - fastest chat."
            Write-Info "Note: GGUF chat runs through llama.cpp, which a newer TutorRD update adds."
            Write-Info "For now this installer sets up the LiteRT Gemma 4 E2B model so you can"
            Write-Info "start studying right away. You can switch to GGUF later inside the app."
            $doDownload = $true
        }
        "lite" {
            Write-Ok "Tier: LITE (4 to 8 GB). Your PC can host a small model."
            Write-Info "Best model for you: LiteRT Gemma 4 E2B (about 1.4 GB)."
            $doDownload = $true
        }
        "client" {
            Write-Warn2 "Tier: CLIENT (under 4 GB). This PC is best used as a CLIENT."
            Write-Info "Do NOT download a model here - it would be too slow."
            Write-Info "Instead, run TutorRD on a stronger PC on your network, and open its"
            Write-Info "address from THIS computer's web browser, for example:"
            Write-Info "    http://192.168.1.50:3782"
            Write-Info "(Replace 192.168.1.50 with the other PC's address. Ask whoever set up"
            Write-Info " the main TutorRD PC for that number - it is shown when TutorRD starts.)"
            $doDownload = $false
        }
    }

    # -----------------------------------------------------------------------
    # 6. Model download (full + lite only)
    # -----------------------------------------------------------------------
    if ($doDownload) {
        $modelsDir = Join-Path $RepoRoot "data\models"
        $existing  = @(Get-ChildItem -Path $modelsDir -Filter *.litertlm -ErrorAction SilentlyContinue)
        if ($existing.Count -gt 0) {
            Write-Ok "A model is already downloaded ($($existing[0].Name)). Skipping download."
        } else {
            Write-Step "Downloading the AI model (about 1.4 GB - the slow part)"
            Write-Info "You can leave this running. Progress is shown below."
            Push-Location $RepoRoot
            try {
                uv run python scripts/download_litertlm_model.py
                if ($LASTEXITCODE -ne 0) {
                    Fail "The model download did not finish." `
                         "Check your internet connection and re-run this installer. It resumes from where it stopped, so you will not lose progress."
                }
            } finally { Pop-Location }
            Write-Ok "Model downloaded."
        }
    }

    # -----------------------------------------------------------------------
    # 7. Desktop shortcut
    # -----------------------------------------------------------------------
    Write-Step "Creating a 'TutorRD' shortcut on your Desktop"
    $startScript = Join-Path $ScriptDir "start-tutorrd.ps1"
    $desktop = Join-Path $env:USERPROFILE "Desktop"
    if (-not (Test-Path $desktop)) { $desktop = [Environment]::GetFolderPath("Desktop") }
    $lnkPath = Join-Path $desktop "TutorRD.lnk"
    try {
        $ws = New-Object -ComObject WScript.Shell
        $sc = $ws.CreateShortcut($lnkPath)
        $sc.TargetPath       = (Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe")
        $sc.Arguments        = "-NoProfile -ExecutionPolicy Bypass -File `"$startScript`""
        $sc.WorkingDirectory = $RepoRoot
        $sc.IconLocation     = "$env:SystemRoot\System32\shell32.dll,220"
        $sc.Description       = "Start TutorRD - your offline AI tutor"
        $sc.Save()
        Write-Ok "Shortcut created: $lnkPath"
    } catch {
        Write-Warn2 "Could not create the Desktop shortcut automatically."
        Write-Info  "You can still start TutorRD: right-click 'start-tutorrd.ps1' (in the"
        Write-Info  "packaging\bootstrap folder) and choose 'Run with PowerShell'."
    }

    # -----------------------------------------------------------------------
    # Done
    # -----------------------------------------------------------------------
    Write-Host ""
    Write-Host "  ============================================================" -ForegroundColor Green
    if ($tier -eq "client") {
        Write-Host "   Setup complete." -ForegroundColor Green
        Write-Host "   This PC is set up as a CLIENT. Open the main TutorRD PC's" -ForegroundColor Green
        Write-Host "   address in your browser to start studying (see notes above)." -ForegroundColor Green
    } else {
        Write-Host "   Setup complete - double-click TutorRD on your desktop to start." -ForegroundColor Green
    }
    Write-Host "  ============================================================" -ForegroundColor Green
    if ($webPending) {
        Write-Host ""
        Write-Warn2 "One thing left: install Node.js, then run this installer again"
        Write-Info  "so the tutor screen can be built. Until then the app cannot open."
    }
    Pause-End
    exit 0
}
catch {
    # Catch-all so students never see a raw red stack trace as the final word.
    Fail "Something unexpected went wrong: $($_.Exception.Message)" `
         "Take a photo of this screen and share it with your TutorRD helper. It is safe to run this installer again."
}
