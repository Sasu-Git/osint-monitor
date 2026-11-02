# Shared settings for the read-only production-local web server (dot-sourced by start/status/stop).
# Runbook: docs/deploy/WEB-LOCAL.md. Localhost only; intelligence DB read-only; personal state in its own DB.
$WebRoot         = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path          # the worktree these scripts run from
$WebExpectedRoot = 'C:\Users\EugenioVardiero\osint-monitor-web'                   # the dedicated web worktree
$WebPython       = 'C:\Users\EugenioVardiero\osint-monitor\.venv\Scripts\python.exe'
$WebHost         = '127.0.0.1'
$WebPort         = 8790
$LiveDb          = 'C:\Users\EugenioVardiero\osint-monitor\data\eval\window-2026-09-25.db'   # opened mode=ro
# Persistent web state, outside every worktree (gitignored data/web/)
$WebDataDir      = 'C:\Users\EugenioVardiero\osint-monitor\data\web'
$WebUserDb       = Join-Path $WebDataDir 'user_state.db'
$WebLogDir       = Join-Path $WebDataDir 'logs'
$WebStateFile    = Join-Path $WebDataDir 'server.json'
$WebApprovedFile = Join-Path $WebDataDir 'approved-tag.txt'   # one line: the owner-approved deploy-web-* tag
$DaemonRoot      = 'C:\Users\EugenioVardiero\osint-monitor-daemon'

function Get-WebServer {
    # The web server's processes (venv launcher + interpreter), found by command line: main.py serve on the web port
    return @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object {
        $_.CommandLine -match 'main\.py"?\s+serve' -and $_.CommandLine -match "--port\s+$WebPort\b" })
}

function Get-ApprovedTag {
    if (-not (Test-Path $WebApprovedFile)) { return $null }
    return (Get-Content $WebApprovedFile -TotalCount 1).Trim()
}

function Test-SameFile([string]$A, [string]$B) {
    return [IO.Path]::GetFullPath($A).ToLower() -eq [IO.Path]::GetFullPath($B).ToLower()
}

function Read-LiveScalar([string]$Sql) {
    # One value from the live DB, opened read-only (never the web app's engine)
    $q = "import sqlite3,sys; print(sqlite3.connect('file:'+sys.argv[1].replace(chr(92),'/')+'?mode=ro',uri=True).execute(sys.argv[2]).fetchone()[0])"
    return (& $WebPython -I -c $q $LiveDb $Sql)
}
