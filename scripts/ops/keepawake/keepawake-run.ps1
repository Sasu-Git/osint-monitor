# Wrapper: run keepawake.ps1 and append all its output to keepawake.log (no cmd.exe / console redirection needed,
# so the process can be created detached in its own process group, out of reach of console Ctrl+C).
param([string]$UntilUtc)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
& "$here\keepawake.ps1" -UntilUtc $UntilUtc *>> "$here\keepawake.log"
