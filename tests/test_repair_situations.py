"""scripts/repair_situations.py: created Situations whose actor identity is invalid under the current normaliser
are retired (closed, renamed, members detached); seeds and valid Situations are untouched; the dry run cannot
write; --apply backs up first."""

import hashlib
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from osint_monitor.core.database import Base, Event, Situation

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import repair_situations as R  # noqa: E402


def _db(path: Path) -> Path:
    engine = create_engine(f"sqlite:///{path.as_posix()}")
    Base.metadata.create_all(engine)
    s = sessionmaker(bind=engine)()
    now = datetime(2026, 10, 6, 12)
    rows = [("estados-unidos-united-states", ["Estados Unidos", "United States"]),
            ("bolsonaro-fl-vio-bolsonaro", ["Bolsonaro", "Flávio Bolsonaro"]),
            ("nato-russia", ["Nato", "Russia"]),
            ("russia-ukraine-war", ["Russia", "Ukraine"])]                  # a seed in config/situations.yaml
    for i, (slug, actors) in enumerate(rows, 1):
        s.add(Situation(id=i, slug=slug, title=slug, status="active", primary_actors=actors, created_at=now,
                        updated_at=now))
        s.add(Event(id=i, summary=f"e{i}", situation_id=i, first_reported_at=now, last_updated_at=now))
    s.commit()
    s.close()
    engine.dispose()
    return path


def test_dry_run_reports_the_invalid_situations_and_writes_nothing(tmp_path, capsys):
    db = _db(tmp_path / "s.db")
    before = hashlib.sha256(db.read_bytes()).hexdigest()
    assert R.main(["--db", str(db), "--out", str(tmp_path / "r.json")]) == 0
    out = capsys.readouterr().out
    assert "INVALID estados-unidos-united-states: actors collapse" in out
    assert "INVALID bolsonaro-fl-vio-bolsonaro: no longer actors" in out
    assert "nato-russia" not in out and "russia-ukraine-war" not in out
    assert hashlib.sha256(db.read_bytes()).hexdigest() == before


def test_apply_retires_detaches_and_backs_up(tmp_path):
    db = _db(tmp_path / "s.db")
    assert R.main(["--db", str(db), "--apply", "--backup-dir", str(tmp_path / "b")]) == 0
    assert list((tmp_path / "b").glob("s.pre-situation-repair-*.db"))
    s = sessionmaker(bind=create_engine(f"sqlite:///{db.as_posix()}"))()
    by_id = {x.id: x for x in s.query(Situation)}
    assert by_id[1].status == "closed" and by_id[1].slug.startswith("estados-unidos-united-states--retired-")
    assert by_id[2].status == "closed" and "invalid actor identity" in by_id[2].short_description
    assert by_id[3].status == "active" and by_id[3].slug == "nato-russia"
    assert by_id[4].slug == "russia-ukraine-war" and by_id[4].status == "active"
    members = {e.id: e.situation_id for e in s.query(Event)}
    assert members == {1: None, 2: None, 3: 3, 4: 4}
