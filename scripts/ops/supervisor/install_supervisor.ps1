# Install the live-daemon supervisor (post-soak item 6). Re-running is safe: it refreshes the script copy and the
# scheduled task, and never overwrites an existing config.json (the pinned commit is changed there deliberately,
# as part of a deploy).
#
#   powershell -ExecutionPolicy Bypass -File install_supervisor.ps1 [-RuntimeDir DIR] [-PinnedCommit SHA]
#
# The scheduled task runs a copy outside git (RuntimeDir), so a git update cannot change what supervises the daemon.
param(
    [string]$RuntimeDir = "C:\Users\EugenioVardiero\osint-monitor\data\deploy\supervisor",
    [string]$PinnedCommit = "5f046b34fb07a00936b75c6a773cf78a4e855f2b",   # production-stable-20261006
    [string]$TaskName = "OSINT daemon supervisor"
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force $RuntimeDir | Out-Null
Copy-Item "$here\daemon_supervisor.py" "$RuntimeDir\daemon_supervisor.py" -Force

$config = Join-Path $RuntimeDir "config.json"
if (-not (Test-Path $config)) {
    $cfg = [ordered]@{
        pinned_commit         = $PinnedCommit
        daemon_worktree       = "C:\Users\EugenioVardiero\osint-monitor-daemon"
        db_url                = "sqlite:///C:/Users/EugenioVardiero/osint-monitor/data/eval/window-2026-09-25.db"
        python                = "C:\Users\EugenioVardiero\osint-monitor\.venv\Scripts\python.exe"
        pythonw               = "C:\Users\EugenioVardiero\osint-monitor\.venv\Scripts\pythonw.exe"
        keepawake             = $true
        keepawake_script      = "C:\Users\EugenioVardiero\osint-monitor-daemon\keepawake\keepawake.py"
        keepawake_hours       = 24
        max_restarts_per_hour = 3
        hold_file             = (Join-Path $RuntimeDir "HOLD")
        log                   = (Join-Path $RuntimeDir "supervisor.jsonl")
        log_every_check       = $false
    }
    ($cfg | ConvertTo-Json) | Out-File -Encoding utf8 $config
}

$pythonw = (Get-Content $config -Raw | ConvertFrom-Json).pythonw
$action = New-ScheduledTaskAction -Execute $pythonw -Argument "`"$RuntimeDir\daemon_supervisor.py`" `"$config`"" `
    -WorkingDirectory $RuntimeDir
$every5 = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 5)
$logon = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable `
    -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 3)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($every5, $logon) -Settings $settings `
    -Principal $principal -Description "Restarts the OSINT live daemon (pinned commit only) when its process is gone. See data/deploy/LIVE-DAEMON.md." `
    -Force | Out-Null
"installed: task '$TaskName' every 5 min; runtime $RuntimeDir; pinned $((Get-Content $config -Raw | ConvertFrom-Json).pinned_commit)"
