# Shared settings for the local demo scripts (dot-sourced by start/status/stop). Localhost only.
$DemoRoot      = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path          # the frontend worktree
$DemoPython    = 'C:\Users\EugenioVardiero\osint-monitor\.venv\Scripts\python.exe'
$DemoBranch    = 'feat/sa-workspace'
$DemoCommit    = '5e36c1c'                                                       # approved app code (feat/sa-workspace)
$DemoHost      = '127.0.0.1'
$DemoDir       = Join-Path $DemoRoot 'data\demo'
$DemoScratchDb = Join-Path $DemoDir 'intel-scratch.db'
$DemoUserDb    = Join-Path $DemoDir 'user_state-demo.db'
$DemoPidFile   = Join-Path $DemoDir 'server.json'
$LiveDb        = 'C:\Users\EugenioVardiero\osint-monitor\data\eval\window-2026-09-25.db'   # live daemon DB: source only

# Paths the demo must never use as its intelligence or user-state database
$ForbiddenDbs = @(
    $LiveDb,
    'C:\Users\EugenioVardiero\osint-monitor\data\osint.db',
    'C:\Users\EugenioVardiero\osint-monitor-daemon\data\osint.db',
    (Join-Path $DemoRoot 'data\osint.db'),
    'C:\Users\EugenioVardiero\osint-monitor\data\user_state.db',
    (Join-Path $DemoRoot 'data\user_state.db')
) | ForEach-Object { [IO.Path]::GetFullPath($_).ToLower() }

function Test-ForbiddenDb([string]$Path) {
    $full = [IO.Path]::GetFullPath($Path).ToLower()
    return ($ForbiddenDbs -contains $full) -or ($full -like '*\osint-monitor-daemon\*')
}

function Get-DemoServer {
    # The demo server's processes (venv launcher + interpreter), found by command line: main.py serve on the demo port
    if (-not (Test-Path $DemoPidFile)) { return @() }
    $state = Get-Content $DemoPidFile -Raw | ConvertFrom-Json
    $procs = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object {
        $_.CommandLine -match 'main\.py"?\s+serve' -and $_.CommandLine -match "--port\s+$($state.port)\b" })
    return $procs
}
