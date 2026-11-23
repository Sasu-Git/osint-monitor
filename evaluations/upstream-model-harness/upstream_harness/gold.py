"""Gold loading: cases, split, vocabulary, label records (primary = first answer, secondary = final answer).

Label record format (from each track's label_server.py): ``labels.yaml`` maps case id -> label (final answers);
``label-history.jsonl`` has one line per save ``{"at", "case", **label}``; the first line per case is the blind primary
basis. ``labels-freeze.json`` is written by ``label_server.py --freeze``.

Reading label files is only done through this module, and only after the completion checker has passed (see
``checker.require_complete``); nothing here prints label values.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from .common import sha256_file

INTENTS = ["occurred", "announced_planned", "threatened", "called_for", "hypothetical", "denied", "reported_allegation"]
POLITICAL = ["yes", "no", "n.a."]
LOC_SPECIAL = ["NONE", "MULTI", "SEA_OR_REGION", "DISPUTED"]
ISO3 = re.compile(r"^[A-Z]{3}$")
ROLES = ["event", "target", "origin", "actor_location", "venue", "reporting", "mentioned"]
FREEZE_SHA_LINE = re.compile(r"^([0-9a-f]{64})\s+(\S+)\s*$", re.M)


class GoldError(RuntimeError):
    pass


@dataclass
class GoldTrack:
    root: Path
    track: str

    @property
    def dir(self) -> Path:
        return self.root / self.track

    # -- files
    @property
    def cases_path(self): return self.dir / "cases.json"
    @property
    def manifest_path(self): return self.dir / "manifest.json"
    @property
    def split_path(self): return self.dir / "split.json"
    @property
    def labels_path(self): return self.dir / "labels.yaml"
    @property
    def history_path(self): return self.dir / "label-history.jsonl"
    @property
    def freeze_path(self): return self.dir / "labels-freeze.json"

    # -- frozen inputs (not labels)
    def cases(self) -> dict[int, dict]:
        return {c["development_id"]: c for c in json.loads(self.cases_path.read_text(encoding="utf-8"))["cases"]}

    def case_ids(self) -> list[int]:
        return sorted(self.cases())

    def split(self) -> dict:
        return json.loads(self.split_path.read_text(encoding="utf-8"))

    def split_ids(self, which: str) -> list[int]:
        s = self.split()
        if which == "all":
            return sorted(s["development"] + s["acceptance"])
        return sorted(s[which])

    def role_subset_ids(self) -> set[int]:
        return {i for i, c in self.cases().items() if c.get("role_labels")}

    def vocabulary(self) -> dict:
        if self.track == "topic":
            tax = json.loads((self.dir / "taxonomy.json").read_text(encoding="utf-8"))
            return {"action_types": list(tax["action_types"]) + list(tax["extra"])}
        ctry = json.loads((self.dir / "countries-iso3.json").read_text(encoding="utf-8"))
        return {"countries": sorted(c["id"] for c in ctry)}

    # -- label files
    def load_final(self) -> dict[int, dict]:
        if not self.labels_path.exists():
            return {}
        raw = yaml.safe_load(self.labels_path.read_text(encoding="utf-8")) or {}
        return {int(k): v for k, v in raw.items()}

    def load_primary(self) -> dict[int, dict]:
        """First saved answer per case (blind primary basis)."""
        out: dict[int, dict] = {}
        if not self.history_path.exists():
            return out
        for line in self.history_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            c = int(rec["case"])
            if c not in out:
                out[c] = {k: v for k, v in rec.items() if k not in ("at", "case")}
        return out

    def label_file_sha(self) -> str | None:
        return sha256_file(self.labels_path) if self.labels_path.exists() else None


def label_problems(track: GoldTrack, vocab: dict, case_id: int, label: dict, role_ids: set[int],
                   items: list[int]) -> list[str]:
    """Validity problems, never including label values."""
    if not isinstance(label, dict):
        return [f"D{case_id}: label is not a mapping"]
    out = []
    if track.track == "topic":
        at = label.get("action_type")
        if at not in vocab["action_types"]:
            out.append(f"D{case_id}: action_type not in taxonomy")
        if at != "out_of_scope" and label.get("intent") not in INTENTS:
            out.append(f"D{case_id}: intent not in enum")
        if label.get("intent") not in INTENTS + [None]:
            out.append(f"D{case_id}: intent not in enum")
        if label.get("speaker_is_political") not in POLITICAL:
            out.append(f"D{case_id}: speaker_is_political not in enum")
        for k in ("agent", "target", "speaker"):
            if not isinstance(label.get(k), list):
                out.append(f"D{case_id}: {k} must be a list")
    else:
        ec = str(label.get("event_country", ""))
        if not (ec in LOC_SPECIAL or (ISO3.match(ec) and ec in vocab["countries"])):
            out.append(f"D{case_id}: event_country not in vocabulary")
        if case_id in role_ids:
            pm = label.get("place_mentions") or {}
            for it in items:
                if str(it) not in pm:
                    out.append(f"D{case_id}: item {it}: place mentions missing")
                else:
                    for m in pm[str(it)]:
                        if not isinstance(m, dict) or m.get("role") not in ROLES or not m.get("place"):
                            out.append(f"D{case_id}: item {it}: bad place mention")
    return out


def parse_freeze_md(root: Path) -> dict[str, str]:
    """path (relative to gold root) -> sha256, from every ```sha256 block in FREEZE.md; later blocks win."""
    txt = (root / "FREEZE.md").read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for sha, path in FREEZE_SHA_LINE.findall(txt):
        out[path] = sha
    return out
