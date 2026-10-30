# Is the local demo running, on 127.0.0.1, against the scratch DB only? Changes nothing.
#   .\scripts\demo\status_local_demo.ps1
. (Join-Path $PSScriptRoot 'demo_config.ps1')

function Line([bool]$Ok, [string]$Msg) {
    $tag = if ($Ok) { '[OK]  ' } else { '[FAIL]' }
    Write-Host "$tag $Msg" -ForegroundColor $(if ($Ok) { 'Green' } else { 'Red' })
}

if (-not (Test-Path $DemoPidFile)) { Write-Host 'Demo not started (no data\demo\server.json).'; exit 1 }
$state = Get-Content $DemoPidFile -Raw | ConvertFrom-Json
$port = $state.port; $base = "http://$($state.host):$port"

# Process and port
$procs = @(Get-DemoServer)
Line ($procs.Count -gt 0) "process alive: $(($procs | ForEach-Object { $_.ProcessId }) -join ', ')"
$listen = @(Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)
Line ($listen.Count -gt 0 -and ($listen | Where-Object LocalAddress -ne '127.0.0.1').Count -eq 0) `
     "port $port listening on: $(($listen | ForEach-Object { $_.LocalAddress }) -join ', ') (owner PID $(($listen | ForEach-Object { $_.OwningProcess }) -join ', '))"

# Routes
foreach ($r in '/', '/map', '/situations', '/priorities') {
    try { $code = (Invoke-WebRequest "$base$r" -UseBasicParsing -TimeoutSec 30).StatusCode } catch { $code = $_.Exception.Message }
    Line ($code -eq 200) "GET $r -> $code"
}

# Which intelligence DB the app reads: the newest Development in the scratch copy must be served, and a
# Development that exists only in the live DB (created after the copy) must not be.
$q = "import sqlite3,sys; print(sqlite3.connect('file:'+sys.argv[1].replace(chr(92),'/')+'?mode=ro',uri=True).execute('select max(id) from events').fetchone()[0])"
$scratchMax = [int](& $DemoPython -I -c $q $state.scratch_db)
$liveMax    = [int](& $DemoPython -I -c $q $LiveDb)
$served = (Invoke-RestMethod "$base/api/events/$scratchMax" -TimeoutSec 30)
Line ($served.id -eq $scratchMax) "app serves scratch Development D$scratchMax (scratch max id)"
if ($liveMax -gt $scratchMax) {
    $live = Invoke-RestMethod "$base/api/events/$liveMax" -TimeoutSec 30
    Line ($null -eq $live.id) "app does NOT serve live-only Development D$liveMax (live DB is ahead of the copy)"
} else { Write-Host "[INFO] live DB has no Development newer than the copy yet (live max D$liveMax); refresh-age check skipped" }
Line (-not (Test-ForbiddenDb $state.scratch_db)) "scratch DB is not a production path"

# User state: only the demo file
Line (-not (Test-Path (Join-Path $DemoRoot 'data\user_state.db'))) "no default data\user_state.db in the frontend worktree"
if (Test-Path $state.user_state_db) {
    $q2 = "import sqlite3,sys; print(sqlite3.connect('file:'+sys.argv[1].replace(chr(92),'/')+'?mode=ro',uri=True).execute('select count(*) from preferences').fetchone()[0])"
    Write-Host "[INFO] demo user-state DB $($state.user_state_db): $(& $DemoPython -I -c $q2 $state.user_state_db) priority rows, modified $((Get-Item $state.user_state_db).LastWriteTime)"
}

# Live daemon unaffected (PIDs, pinned commit)
$daemon = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object CommandLine -match 'main\.py"?\s+daemon')
$dhead = (& git -C 'C:\Users\EugenioVardiero\osint-monitor-daemon' rev-parse --short HEAD).Trim()
Write-Host "[INFO] live daemon PIDs $(($daemon | ForEach-Object { $_.ProcessId }) -join ', ') at $dhead (not touched by the demo)"
$extra = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.CommandLine -match 'main\.py"?\s+(daemon|collect)' -and $_.CommandLine -notmatch 'osint-monitor-daemon' -and ($daemon.ProcessId -notcontains $_.ProcessId) })
Line ($extra.Count -eq 0) "no extra daemon/collector processes"
