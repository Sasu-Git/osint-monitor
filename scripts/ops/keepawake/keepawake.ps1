# Hold a system-required power request until the given UTC time (no power-plan changes).
param([string]$UntilUtc = "2026-09-29T13:30:00Z")
Add-Type -Namespace Win -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint esFlags);'
$ES_CONTINUOUS = [uint32]"0x80000000"; $ES_SYSTEM_REQUIRED = [uint32]"0x00000001"
$until = [DateTime]::Parse($UntilUtc).ToUniversalTime()
[Win.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED) | Out-Null
"keep-awake held from $([DateTime]::UtcNow.ToString('u')) until $($until.ToString('u'))"
while ([DateTime]::UtcNow -lt $until) { Start-Sleep -Seconds 60; [Win.Power]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED) | Out-Null }
[Win.Power]::SetThreadExecutionState($ES_CONTINUOUS) | Out-Null
"keep-awake released at $([DateTime]::UtcNow.ToString('u'))"
