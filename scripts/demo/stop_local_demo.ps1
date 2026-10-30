# Stop only the local demo server (main.py serve on the demo port). Never touches the live daemon.
#   .\scripts\demo\stop_local_demo.ps1
. (Join-Path $PSScriptRoot 'demo_config.ps1')

if (-not (Test-Path $DemoPidFile)) { Write-Host 'Demo not started (no data\demo\server.json).'; exit 0 }
$state = Get-Content $DemoPidFile -Raw | ConvertFrom-Json
$procs = @(Get-DemoServer)
foreach ($p in $procs) {
    if ($p.CommandLine -match 'main\.py"?\s+daemon') { Write-Host "SKIP $($p.ProcessId): daemon"; continue }
    Write-Host "stopping PID $($p.ProcessId): $($p.CommandLine)"
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
}
Start-Sleep -Seconds 2
$left = @(Get-NetTCPConnection -LocalPort $state.port -State Listen -ErrorAction SilentlyContinue)
if ($left.Count) { Write-Host "Port $($state.port) still listening (PID $($left.OwningProcess))" -ForegroundColor Red; exit 1 }
Remove-Item $DemoPidFile
Write-Host "Stopped. Port $($state.port) closed." -ForegroundColor Green
