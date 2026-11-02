# Is the read-only web server running as deployed: approved tag, 127.0.0.1 only, live DB read-only, writes refused,
# personal state separate, daemon untouched? Changes nothing (only GET requests and one refused POST).
#   .\scripts\web\status_local_web.ps1
. (Join-Path $PSScriptRoot 'web_config.ps1')

function Line([bool]$Ok, [string]$Msg) {
    $tag = if ($Ok) { '[OK]  ' } else { '[FAIL]' }
    Write-Host "$tag $Msg" -ForegroundColor $(if ($Ok) { 'Green' } else { 'Red' })
}

if (-not (Test-Path $WebStateFile)) { Write-Host "Web server not started (no $WebStateFile)."; exit 1 }
$state = Get-Content $WebStateFile -Raw | ConvertFrom-Json
$base = "http://${WebHost}:$WebPort"

# Code: the approved tag
$approved = Get-ApprovedTag
$head = (& git -C $WebRoot rev-parse HEAD).Trim()
$tagCommit = if ($approved) { (& git -C $WebRoot rev-parse --verify --quiet "$approved^{commit}") } else { '' }
Line ($approved -and $head -eq "$tagCommit".Trim()) "web worktree $WebRoot at $($head.Substring(0,7)) = approved tag $approved"

# Process and port
$procs = Get-WebServer
Line ($procs.Count -gt 0) "process alive: $(($procs | ForEach-Object { $_.ProcessId }) -join ', ')"
$listen = @(Get-NetTCPConnection -LocalPort $WebPort -State Listen -ErrorAction SilentlyContinue)
Line ($listen.Count -gt 0 -and ($listen | Where-Object LocalAddress -ne '127.0.0.1').Count -eq 0) `
     "port $WebPort listening on: $(($listen | ForEach-Object { $_.LocalAddress }) -join ', ') only"

# Pages
foreach ($r in '/', '/map', '/situations', '/priorities') {
    try { $code = (Invoke-WebRequest "$base$r" -UseBasicParsing -TimeoutSec 60).StatusCode } catch { $code = $_.Exception.Message }
    Line ($code -eq 200) "GET $r -> $code"
}

# Live reading: the newest Development in the live DB is served
$liveMax = [int](Read-LiveScalar 'select max(id) from events')
$served = Invoke-RestMethod "$base/api/events/$liveMax" -TimeoutSec 60
Line ($served.id -eq $liveMax) "serves the newest live Development D$liveMax"
Write-Host "[INFO] live schema version $(Read-LiveScalar "select value from schema_meta where key='schema_version'")"

# Read-only: a write route and the daemon controls are refused
foreach ($probe in @(@('POST', '/api/alerts/0/acknowledge'), @('POST', '/api/daemon/pause'), @('GET', '/api/daemon/status'))) {
    try { $r = Invoke-WebRequest "$base$($probe[1])" -Method $probe[0] -UseBasicParsing -TimeoutSec 30; $code = $r.StatusCode }
    catch { $code = [int]$_.Exception.Response.StatusCode }
    Line ($code -eq 403) "$($probe[0]) $($probe[1]) -> $code (refused)"
}
Line (-not (Test-Path (Join-Path $WebRoot 'data\pause'))) "no pause flag in the web worktree"

# Personal state: only data\web\user_state.db
if (Test-Path $WebUserDb) {
    $q = "import sqlite3,sys; print(sqlite3.connect('file:'+sys.argv[1].replace(chr(92),'/')+'?mode=ro',uri=True).execute('select count(*) from preferences').fetchone()[0])"
    Write-Host "[INFO] user-state DB $WebUserDb`: $(& $WebPython -I -c $q $WebUserDb) priority rows, modified $((Get-Item $WebUserDb).LastWriteTime)"
}
Line (-not (Test-Path (Join-Path $WebRoot 'data\user_state.db'))) "no default data\user_state.db in the web worktree"

# Daemon untouched (informational)
$daemon = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object CommandLine -match 'main\.py"?\s+daemon')
$dhead = (& git -C $DaemonRoot rev-parse --short HEAD).Trim()
$lastRun = Read-LiveScalar "select max(finished_at) from pipeline_runs"
Write-Host "[INFO] live daemon PIDs $(($daemon | ForEach-Object { $_.ProcessId }) -join ', ') at $dhead; last finished run $lastRun UTC"
