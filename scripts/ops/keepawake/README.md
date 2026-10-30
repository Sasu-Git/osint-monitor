# Host keep-awake and detached daemon launch (operations; post-soak item 6, host power)

Used on the live host since 2026-09-29. Neither script changes the power plan; they hold a power request until a
UTC time. On a Modern Standby laptop a closed lid or a battery-saver standby is not prevented.

- `keepawake.py UNTIL_UTC [--display]`: run with `pythonw.exe` (no console). Holds ES_SYSTEM_REQUIRED (and
  ES_DISPLAY_REQUIRED with `--display`) until the given time. Current launcher.
- `keepawake.ps1` / `keepawake-run.ps1`: the earlier PowerShell version and its log wrapper.

## Launch detached (no console, so a console Ctrl+C or close event cannot kill it)

A daemon started from a `cmd` console was killed by a console `^C` on 2026-10-08 20:49 UTC. Both processes are now
created through WMI, which detaches them from any console:

```powershell
$daemon = 'cmd /c cd /d C:\Users\EugenioVardiero\osint-monitor-daemon && set "OSINT_DB_URL=sqlite:///C:/Users/EugenioVardiero/osint-monitor/data/eval/window-2026-09-25.db" && "C:\Users\EugenioVardiero\osint-monitor\.venv\Scripts\python.exe" main.py daemon >> data\logs\daemon.out.log 2>> data\logs\daemon.err.log'
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $daemon; CurrentDirectory = 'C:\Users\EugenioVardiero\osint-monitor-daemon'}

$keep = '"C:\Users\EugenioVardiero\osint-monitor\.venv\Scripts\pythonw.exe" C:\Users\EugenioVardiero\osint-monitor-daemon\keepawake\keepawake.py 2026-10-16T00:00:00Z --display'
Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $keep; CurrentDirectory = 'C:\Users\EugenioVardiero\osint-monitor-daemon\keepawake'}
```

Check health with `python main.py status` (with the same `OSINT_DB_URL`).
