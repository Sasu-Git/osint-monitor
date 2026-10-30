# Start the situational-awareness workspace for a local demo: 127.0.0.1 only, scratch intelligence DB,
# separate demo user-state DB, no reload, no daemon, no collectors.
#   .\scripts\demo\start_local_demo.ps1 [-Port 8770] [-Refresh] [-AllowAnyCommit]
param(
    [int]$Port = 8770,
    [switch]$Refresh,          # re-copy the live DB into the scratch file first
    [switch]$AllowAnyCommit    # skip the branch/commit check
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'demo_config.ps1')

function Fail([string]$Msg) { Write-Host "REFUSED: $Msg" -ForegroundColor Red; exit 2 }

# 1. Right worktree and commit
$branch = (& git -C $DemoRoot rev-parse --abbrev-ref HEAD).Trim()
$head   = (& git -C $DemoRoot rev-parse HEAD).Trim()
if (-not $AllowAnyCommit -and ($branch -ne $DemoBranch -or -not $head.StartsWith($DemoCommit))) {
    Fail "worktree $DemoRoot is on $branch @ $($head.Substring(0,7)); expected $DemoBranch @ $DemoCommit (use -AllowAnyCommit to override)"
}
if ($DemoRoot -like '*osint-monitor-daemon*') { Fail "this is the live daemon worktree" }

# 2. Not already running, port free
if (@(Get-DemoServer).Count) { Fail "a demo server is already running (stop_local_demo.ps1 first)" }
if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) { Fail "port $Port is in use" }

# 3. Scratch DB: refresh from the live DB (read-only source, SQLite backup API). The copy stays writable: the app
#    sets WAL mode on connect, which a read-only file refuses. Nothing it writes reaches the live DB.
if (Test-ForbiddenDb $DemoScratchDb) { Fail "scratch path $DemoScratchDb resolves to a production database" }
if (Test-ForbiddenDb $DemoUserDb)    { Fail "user-state path $DemoUserDb resolves to a production database" }
if ($Refresh -or -not (Test-Path $DemoScratchDb)) {
    if (Test-Path $DemoScratchDb) { Set-ItemProperty $DemoScratchDb -Name IsReadOnly -Value $false }
    & $DemoPython -I (Join-Path $PSScriptRoot 'make_scratch_db.py') --src $LiveDb --dst $DemoScratchDb
    if ($LASTEXITCODE -ne 0) { Fail "scratch copy failed" }
}

# 4. Environment for the server process only (restored afterwards)
$vars = @{
    OSINT_DB_URL         = 'sqlite:///' + ($DemoScratchDb -replace '\\', '/')
    OSINT_USER_STATE_DB  = $DemoUserDb
    OSINT_API_HOST       = $DemoHost
    OSINT_API_PORT       = "$Port"
    PYTHONPATH           = $DemoRoot
    HF_HUB_OFFLINE       = '1'
}
$saved = @{}
foreach ($k in $vars.Keys) { $saved[$k] = [Environment]::GetEnvironmentVariable($k); Set-Item "env:$k" $vars[$k] }
try {
    $out = Join-Path $DemoDir 'server.out.log'; $err = Join-Path $DemoDir 'server.err.log'
    $p = Start-Process -FilePath $DemoPython -WorkingDirectory $DemoRoot -WindowStyle Hidden -PassThru `
        -ArgumentList 'main.py', 'serve', '--host', $DemoHost, '--port', "$Port", '--no-reload' `
        -RedirectStandardOutput $out -RedirectStandardError $err
} finally {
    foreach ($k in $vars.Keys) {
        if ($null -eq $saved[$k]) { Remove-Item "env:$k" -ErrorAction SilentlyContinue } else { Set-Item "env:$k" $saved[$k] }
    }
}
@{ pid = $p.Id; port = $Port; host = $DemoHost; scratch_db = $DemoScratchDb; user_state_db = $DemoUserDb;
   commit = $head; started_utc = (Get-Date).ToUniversalTime().ToString('s') } | ConvertTo-Json | Set-Content $DemoPidFile -Encoding UTF8

# 5. Wait for HTTP 200 on /
$url = "http://${DemoHost}:$Port/"
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 1
    if ($p.HasExited) { Remove-Item $DemoPidFile -ErrorAction SilentlyContinue; Write-Host "Server exited; see $err" -ForegroundColor Red; Get-Content $err -Tail 20; exit 1 }
    try { if ((Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 5).StatusCode -eq 200) { break } } catch {}
}
Write-Host "Demo server PID $($p.Id) on $DemoHost`:$Port  (scratch DB $DemoScratchDb; user state $DemoUserDb)"
Write-Host "Open: $url" -ForegroundColor Green
