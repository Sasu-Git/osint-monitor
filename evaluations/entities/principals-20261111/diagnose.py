"""Principal-extraction diagnosis for the Situation-v2 upstream hardening (2026-11-11).

For every Development on a backup-API copy of the 2026-11-02 snapshot, re-derive the principal actors with the
running code (``development_actors``) and record, per Development, which state/org keys its own headlines name
that did not become principals, and why. The probe for "the headline names actor X" is deterministic: every
1-3 word n-gram of each title that the actor normaliser maps to a country or configured actor.

    python diagnose.py SNAPSHOT_DB OUT.json

Never writes the snapshot. Stage that lost a named key (headlines of round-up items are ignored):
  no_mention                  no role-bearing mention of that key (NER miss, unresolved name, no language model)
  no_mention:no_model         the naming headline's language has no trusted model
  no_mention:rejected:<why>   a span naming it was rejected as a candidate (``principals.rejection``)
  role:<r>                    mentioned, but its dominant role is <r>, not "actor" (semantic gating)
  actor_filtered              dominant role "actor" but dropped by the support threshold or the headline gate
"""
import json
import os
import sqlite3
import sys
import tempfile
from collections import Counter
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")


def main(snapshot: str, out: str) -> int:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from osint_monitor.core.database import Event, EventItem, RawItem
    from osint_monitor.processors.actors import ActorNormalizer
    from osint_monitor.processors.actor_roles import is_roundup
    from osint_monitor.processors.geography import Gazetteer
    from osint_monitor.processors.language import item_language
    from osint_monitor.processors.nlp import get_language_nlp
    from osint_monitor.processors.principals import _lead, development_actors, item_candidates, required_support
    from osint_monitor.processors.text_normalize import clean_text

    tmp = Path(tempfile.mkdtemp(prefix="prindiag-")) / "copy.db"
    src = sqlite3.connect(f"file:{snapshot}?mode=ro", uri=True)
    dst = sqlite3.connect(tmp)
    src.backup(dst)
    dst.close()
    src.close()
    s = sessionmaker(bind=create_engine(f"sqlite:///{tmp.as_posix()}"))()
    norm = ActorNormalizer.load()
    geo = Gazetteer.load()

    def probe_keys(title: str) -> dict[str, set[str]]:
        """state/org key -> surfaces of it that the title names (1-3 word n-grams)."""
        words = clean_text(title or "")[:500].replace("’", "'").split()
        found: dict[str, set[str]] = {}
        for n in (3, 2, 1):
            for i in range(len(words) - n + 1):
                gram = " ".join(words[i:i + n]).strip(",.;:!?\"'()[]")
                if not gram or (n == 1 and gram.lower() in ("us", "un", "eu") and gram != gram.upper()):
                    continue
                k = norm.key(gram)
                if k and (geo.is_country(k) or norm.is_known(gram)):
                    found.setdefault(k, set()).add(gram)
        return found

    per_dev, causes = {}, Counter()
    events = s.query(Event).order_by(Event.id).all()
    for n_done, ev in enumerate(events):
        rows = (s.query(RawItem).join(EventItem, EventItem.item_id == RawItem.id)
                .filter(EventItem.event_id == ev.id).all())
        items = [{"title": r.title or "", "lead": _lead(r.content),
                  "lang": item_language(r.source.name if r.source else None, r.title or ""),
                  "source": r.source.name if r.source else None} for r in rows]
        if not items:
            continue
        actors = development_actors(items, normalizer=norm)
        principal_keys = {k for k in (norm.key(h) or h for h in actors.principals) if k}
        holder_keys = {}                      # state/org key -> holders carrying it
        for h in actors.roles:
            k = norm.key(h) or h
            holder_keys.setdefault(k, []).append(h)
        non_roundup = [i for i in items if not is_roundup(i["title"])]
        named = {}
        for i in non_roundup:
            for k, surfaces in probe_keys(i["title"]).items():
                named.setdefault(k, set()).update(surfaces)
        missing = {}
        for k, surfaces in named.items():
            if k in principal_keys:
                continue
            if k in holder_keys:
                roles = {actors.roles[h] for h in holder_keys[k]}
                cause = "actor_filtered" if "actor" in roles else "role:" + "/".join(sorted(roles))
            else:
                cause = "no_mention"
                for i in non_roundup:
                    if not any(sf.lower() in i["title"].lower() for sf in surfaces):
                        continue
                    nlp = get_language_nlp(i.get("lang"))
                    if nlp is None:
                        cause = "no_mention:no_model"
                        break
                    rej = [c.rejected for c in item_candidates(nlp, i["title"], "", norm, i.get("lang") or "en")
                           if c.rejected and norm.key(c.text) == k]
                    if rej:
                        cause = f"no_mention:rejected:{rej[0]}"
                        break
            missing[k] = {"surfaces": sorted(surfaces), "cause": cause}
            causes[cause] += 1
        if missing:
            per_dev[str(ev.id)] = {
                "situation_id": ev.situation_id, "n_items": len(items),
                "langs": sorted({i["lang"] or "en" for i in items}),
                "titles": [i["title"][:160] for i in items[:6]],
                "principals": sorted(actors.principals), "principal_keys": sorted(principal_keys),
                "roles": {h: r for h, r in sorted(actors.roles.items())},
                "missing": missing,
            }
        if (n_done + 1) % 200 == 0:
            print(f"{n_done + 1}/{len(events)}", flush=True)
    summary = {"developments": len(events), "developments_with_missing": len(per_dev), "causes": dict(causes)}
    Path(out).write_text(json.dumps({"snapshot": snapshot, "summary": summary, "developments": per_dev},
                                    ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1], sys.argv[2]))
