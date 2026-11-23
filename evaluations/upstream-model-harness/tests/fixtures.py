"""Synthetic gold, features and snapshot fixtures (tmp dirs only; nothing here touches real gold or labels)."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import yaml

HARNESS = Path(__file__).resolve().parents[1]
REAL_SPLIT_PY = HARNESS.parent / "upstream-gold-20261123" / "split.py"   # code only, copied verbatim

TOPIC_TYPES = ["sanctions", "military_action", "other"]
COUNTRIES = ["FRA", "UKR", "RUS", "ISR", "PSE"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def topic_label(i: int, shift: int = 0) -> dict:
    return {"action_type": (TOPIC_TYPES + ["unknown", "out_of_scope"])[(i + shift) % 5], "intent": "occurred",
            "agent": [], "target": [], "speaker": [], "speaker_is_political": "n.a.", "note": None}


def loc_label(i: int, role_items: list[int] | None, shift: int = 0) -> dict:
    lab = {"event_country": (COUNTRIES + ["NONE", "MULTI"])[(i + shift) % 7], "event_place": None, "note": None}
    if role_items is not None:
        lab["place_mentions"] = {str(it): [{"place": "Paris", "role": "event"}] for it in role_items}
    return lab


def make_gold(root: Path, n: int = 20, *, label: str = "all", frozen: bool = True, revise: tuple[int, ...] = (),
              crlf: bool = False) -> Path:
    """label: "all" | "partial" (every other case unlabelled) | "none". revise: case ids whose FIRST answer differs from
    the final one (so the primary and secondary bases differ)."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "sample.py").write_text("# synthetic\n", encoding="utf-8", newline="\n")
    (root / "split.py").write_bytes(REAL_SPLIT_PY.read_bytes().replace(b"\r\n", b"\n"))
    ids_t = [1000 + k for k in range(n)]
    ids_l = [2000 + k for k in range(n)]
    for track, ids in (("topic", ids_t), ("location", ids_l)):
        d = root / track
        d.mkdir(exist_ok=True)
        roles = set(ids[::5]) if track == "location" else set()
        cases = [{"development_id": i, "members": 2,
                  "items": [{"item_id": i * 10 + j, "source": "S", "published_at": "2026-11-01", "title": "t", "text": "x"}
                            for j in range(2)],
                  **({"role_labels": i in roles} if track == "location" else {})} for i in ids]
        manifest = {"snapshot_sha256": "0" * 64, "role_subset": sorted(roles),
                    "cases": [{"development_id": i, "stratum": "a" if k % 2 else "b",
                               **({"role_labels": i in roles} if track == "location" else {})}
                              for k, i in enumerate(ids)]}
        (d / "cases.json").write_text(json.dumps({"cases": cases}), encoding="utf-8", newline="\n")
        (d / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8", newline="\n")
        (d / "label_server.py").write_text("# synthetic\n", encoding="utf-8", newline="\n")
        if track == "topic":
            (d / "taxonomy.json").write_text(json.dumps({"action_types": TOPIC_TYPES, "extra": ["out_of_scope", "unknown"]}),
                                             encoding="utf-8", newline="\n")
        else:
            (d / "countries-iso3.json").write_text(json.dumps([{"id": c, "name": c} for c in COUNTRIES]),
                                                   encoding="utf-8", newline="\n")
    subprocess.run([sys.executable, "-I", str(root / "split.py")], check=True, cwd=root, capture_output=True)
    for track, ids in (("topic", ids_t), ("location", ids_l)):
        d = root / track
        cases = {c["development_id"]: c for c in json.loads((d / "cases.json").read_text(encoding="utf-8"))["cases"]}
        labels, hist = {}, []
        for k, i in enumerate(ids):
            if label == "none" or (label == "partial" and k % 2):
                continue
            items = [it["item_id"] for it in cases[i]["items"]]
            mk = (lambda s: topic_label(i, s)) if track == "topic" else \
                 (lambda s: loc_label(i, items if cases[i].get("role_labels") else None, s))
            final = mk(0)
            first = mk(1) if i in revise else final
            hist.append({"at": "2026-11-24T00:00:00+00:00", "case": i, **first})
            if first is not final:
                hist.append({"at": "2026-11-24T00:01:00+00:00", "case": i, **final})
            labels[i] = final
        (d / "labels.yaml").write_text(yaml.safe_dump(labels, sort_keys=False) if labels else "{}\n", encoding="utf-8",
                                       newline="\n")
        if hist:
            (d / "label-history.jsonl").write_text("".join(json.dumps(h) + "\n" for h in hist), encoding="utf-8", newline="\n")
        if frozen:
            rec = {"frozen_at": "2026-11-25T00:00:00+00:00", "labels_sha256": hashlib.sha256((d / "labels.yaml").read_bytes()).hexdigest(),
                   "history_sha256": hashlib.sha256((d / "label-history.jsonl").read_bytes()).hexdigest() if hist else None,
                   "cases": len(ids)}
            (d / "labels-freeze.json").write_text(json.dumps(rec), encoding="utf-8", newline="\n")
    lines = ["# synthetic FREEZE", "```sha256"]
    for rel in ("sample.py", "split.py", *[f"{t}/{f}" for t in ("topic", "location")
                                           for f in ("cases.json", "manifest.json", "split.json", "label_server.py")]):
        lines.append(f"{sha(root / rel)}  {rel}")
    lines.append("```")
    (root / "FREEZE.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    if crlf:   # simulate a Windows autocrlf checkout of the frozen text files
        for p in root.rglob("*"):
            if p.is_file() and p.suffix in (".py", ".json", ".md") and p.name != "labels-freeze.json":
                p.write_bytes(p.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    return root


def make_features_file(root: Path, gold_root: Path, track: str, out: Path) -> dict:
    """Features file for a synthetic gold (fake embeddings, no parses), valid content hash."""
    from upstream_harness.common import canonical, sha256_bytes
    from upstream_harness.features import write_features
    cases = json.loads((gold_root / track / "cases.json").read_text(encoding="utf-8"))["cases"]
    body_cases = {str(c["development_id"]): {"development_id": c["development_id"], "lang": ["en", "es", "it"][c["development_id"] % 3],
                                             "members": 2, "items": []} for c in cases}
    header = {"schema": 1, "track": track, "snapshot_sha256": "0" * 64, "n_cases": len(cases)}
    body = {"header": header, "cases": body_cases}
    body["content_hash"] = sha256_bytes(canonical({"header": header, "cases": body_cases}))
    write_features(body, out)
    return body


def make_snapshot(path: Path, case_rows: dict[int, list[tuple]]) -> str:
    """Tiny sqlite with the tables features.py reads. case_rows: event_id -> [(item_id, source, published, title, content)]"""
    db = sqlite3.connect(path)
    db.executescript("create table sources(id integer primary key, name text);"
                     "create table raw_items(id integer primary key, source_id int, title text, content text, published_at text);"
                     "create table event_items(id integer primary key, event_id int, item_id int);")
    names = {}
    for ev, rows in case_rows.items():
        for rid, source, pub, title, content in rows:
            sid = names.setdefault(source, len(names) + 1)
            db.execute("insert or ignore into sources values (?,?)", (sid, source))
            db.execute("insert into raw_items values (?,?,?,?,?)", (rid, sid, title, content, pub))
            db.execute("insert into event_items(event_id,item_id) values (?,?)", (ev, rid))
    db.commit()
    db.close()
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
