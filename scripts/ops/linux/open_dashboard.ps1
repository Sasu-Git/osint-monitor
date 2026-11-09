# Open the cloud dashboard on this laptop: forwards localhost:8790 to the VM's 127.0.0.1:8790 through the IAP SSH
# tunnel (no firewall port is opened). Leave this window open while using http://localhost:8790/ ; close it to stop.
$env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
$null = Start-Job { Start-Sleep 10; Start-Process "http://localhost:8790/" }   # after the tunnel is up
gcloud compute ssh osint-daemon --project osint-monitor-514209 --zone europe-north1-b --tunnel-through-iap `
    --ssh-flag="-L" --ssh-flag="8790:127.0.0.1:8790" --ssh-flag="-N"
