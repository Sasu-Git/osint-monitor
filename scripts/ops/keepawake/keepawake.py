"""Hold a power request until a UTC time (no power-plan changes). Run with pythonw.exe so it has no console and
cannot receive console Ctrl+C.

    pythonw keepawake.py 2026-10-06T18:00:00Z [--display]

--display also holds ES_DISPLAY_REQUIRED. On Modern Standby (S0ix) laptops the system enters standby when the
display turns off on idle, which ES_SYSTEM_REQUIRED alone does not prevent (observed 2026-10-05 16:27 CEST,
Kernel-Power 506 "Idle Timeout"). Neither flag prevents lid-close or user-initiated standby.
"""
import ctypes
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ES_CONTINUOUS, ES_SYSTEM_REQUIRED, ES_DISPLAY_REQUIRED = 0x80000000, 0x00000001, 0x00000002
LOG = Path(__file__).with_name("keepawake.log")


def log(msg: str) -> None:
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")


until = datetime.fromisoformat(sys.argv[1].replace("Z", "+00:00"))
flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | (ES_DISPLAY_REQUIRED if "--display" in sys.argv else 0)
set_state = ctypes.windll.kernel32.SetThreadExecutionState
set_state(flags)
log(f"keep-awake (python, flags {flags:#x}) held from {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%SZ} "
    f"until {until:%Y-%m-%d %H:%M:%SZ}")
try:
    while datetime.now(timezone.utc) < until:
        time.sleep(60)
        set_state(flags)
finally:
    set_state(ES_CONTINUOUS)
    log(f"keep-awake (python) released at {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%SZ}")
