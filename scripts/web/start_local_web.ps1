# Start the read-only production-local web server: 127.0.0.1:8790, live intelligence DB opened read-only
# (OSINT_DB_READONLY=1), personal priorities in data\web\user_state.db, no reload. Starts no daemon, no collector,
# changes no supervisor. Runbook: docs/deploy/WEB-LOCAL.md.
#   .\scripts\web\start_local_web.ps1
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'web_config.ps1')

function Fail([string]$Msg) { Write-Host "REFUSED: $Msg" -ForegroundColor Red; exit 2 }

# 1. The dedicated web worktree, exactly at the approved tag, with no local edits
if (-not (Test-SameFile $WebRoot $WebExpectedRoot)) { Fail "scripts run from $WebRoot; expected the web worktree $WebExpectedRoot" }
$tag = Get-ApprovedTag
if (-not $tag) { Fail "no approved tag: write the owner-approved deploy-web-* tag to $WebApprovedFile" }
if ($tag -notlike 'deploy-web-*') { Fail "approved tag '$tag' is not a deploy-web-* tag" }
$tagCommit = (& git -C $WebRoot rev-parse --verify --quiet "$tag^{commit}")
if (-not $tagCommit) { Fail "tag $tag does not exist in $WebRoot (git fetch --tags)" }
$head = (& git -C $WebRoot rev-parse HEAD).Trim()
if ($head -ne $tagCommit.Trim()) { Fail "worktree HEAD $($head.Substring(0,7)) is not the approved tag $tag ($($tagCommit.Substring(0,7)))" }
if (& git -C $WebRoot status --porcelain --untracked-files=no) { Fail "worktree $WebRoot has uncommitted changes to tracked files" }

# 2. Databases: live DB present; user state separate, persistent, outside every worktree
if (-not (Test-Path $LiveDb -PathType Leaf)) { Fail "live intelligence DB not found: $LiveDb" }
foreach ($suffix in '', '-wal', '-shm', '-journal') {
    if (Test-SameFile $WebUserDb "$LiveDb$suffix") { Fail "user-state DB $WebUserDb resolves to the intelligence DB" }
}
if (-not ([IO.Path]::GetFullPath($WebUserDb).ToLower().StartsWith([IO.Path]::GetFullPath($WebDataDir).ToLower()))) {
    Fail "user-state DB $WebUserDb is not under $WebDataDir"
}

# 3. Not already running; port free
if ((Get-WebServer).Count) { Fail "the web server is already running (stop_local_web.ps1 first)" }
$listen = @(Get-NetTCPConnection -LocalPort $WebPort -State Listen -ErrorAction SilentlyContinue)
if ($listen.Count) { Fail "port $WebPort is in use by an unrelated process (PID $(($listen | ForEach-Object OwningProcess) -join ', '))" }

# 4. Logs: keep the previous run's logs, timestamped
New-Item -ItemType Directory -Force $WebLogDir | Out-Null
$out = Join-Path $WebLogDir 'web.out.log'; $err = Join-Path $WebLogDir 'web.err.log'
$stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')
foreach ($f in $out, $err) { if (Test-Path $f) { Move-Item $f ($f -replace '\.log$', ".$stamp.log") } }

# 5. Environment for the server process only (restored afterwards). OSINT_DB_READONLY is what makes it read-only.
$vars = @{
    OSINT_DB_URL         = 'sqlite:///' + ($LiveDb -replace '\\', '/')
    OSINT_DB_READONLY    = '1'
    OSINT_USER_STATE_DB  = $WebUserDb
    PYTHONPATH           = $WebRoot
    HF_HUB_OFFLINE       = '1'
}
$saved = @{}
foreach ($k in $vars.Keys) { $saved[$k] = [Environment]::GetEnvironmentVariable($k); Set-Item "env:$k" $vars[$k] }
if ($env:OSINT_DB_READONLY -ne '1') { Fail "OSINT_DB_READONLY is not set" }
try {
    $p = Start-Process -FilePath $WebPython -WorkingDirectory $WebRoot -WindowStyle Hidden -PassThru `
        -ArgumentList 'main.py', 'serve', '--host', $WebHost, '--port', "$WebPort", '--no-reload' `
        -RedirectStandardOutput $out -RedirectStandardError $err
} finally {
    foreach ($k in $vars.Keys) {
        if ($null -eq $saved[$k]) { Remove-Item "env:$k" -ErrorAction SilentlyContinue } else { Set-Item "env:$k" $saved[$k] }
    }
}
@{ pid = $p.Id; port = $WebPort; host = $WebHost; tag = $tag; commit = $head; live_db = $LiveDb; user_state_db = $WebUserDb;
   read_only = $true; started_utc = (Get-Date).ToUniversalTime().ToString('s') } | ConvertTo-Json | Set-Content $WebStateFile -Encoding ASCII

# 6. Wait for HTTP 200 on /; a read-only startup that fails its schema check exits here
$url = "http://${WebHost}:$WebPort/"
for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 1
    if ($p.HasExited) { Remove-Item $WebStateFile -ErrorAction SilentlyContinue; Write-Host "Server exited; see $err" -ForegroundColor Red; Get-Content $err -Tail 20; exit 1 }
    try { if ((Invoke-WebRequest $url -UseBasicParsing -TimeoutSec 5).StatusCode -eq 200) { break } } catch {}
}
Write-Host "Web server PID $($p.Id) on $WebHost`:$WebPort, $tag ($($head.Substring(0,7))), intelligence DB READ-ONLY, user state $WebUserDb"
Write-Host "Open: $url" -ForegroundColor Green
