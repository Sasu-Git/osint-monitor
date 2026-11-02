"""Dry-run wrapper: production runs with the founder guard split out (absent = off = None)."""
import runpy, sys
from osint_monitor.core.config import SituationPolicy
SituationPolicy.founder_same_occurrence_hours = None
assert "--apply" not in sys.argv
sys.argv = [sys.argv[1]] + sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
