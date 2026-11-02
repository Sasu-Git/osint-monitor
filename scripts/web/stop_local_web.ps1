# Stop only the read-only web server (main.py serve on port 8790). Never touches the daemon or the demo.
#   .\scripts\web\stop_local_web.ps1
. (Join-Path $PSScriptRoot 'web_config.ps1')

$procs = Get-WebServer
if (-not $procs.Count) { Write-Host "No web server process on port $WebPort." }
foreach ($p in $procs) {
    if ($p.CommandLine -match 'main\.py"?\s+daemon') { Write-Host "SKIP $($p.ProcessId): daemon"; continue }
    Write-Host "stopping PID $($p.ProcessId): $($p.CommandLine)"
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2
$left = @(Get-NetTCPConnection -LocalPort $WebPort -State Listen -ErrorAction SilentlyContinue)
if ($left.Count) { Write-Host "Port $WebPort still listening (PID $(($left | ForEach-Object OwningProcess) -join ', '))" -ForegroundColor Red; exit 1 }
Remove-Item $WebStateFile -ErrorAction SilentlyContinue
Write-Host "Stopped. Port $WebPort closed." -ForegroundColor Green
