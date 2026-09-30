"""Internal-consistency audit of the frozen entity gold set (evaluations/entities/gold/), run before rescoring.

Checks (numbering follows the owner-review task):
 1 every principal alternative set contains an entity whose role is actor (or a representative of one)
 2 no entity has two roles in a Development (duplicate keys in the roles mapping)
 3 state/person equivalence: every representative has `represents`, the represented entity acts, and a person
   accepted as a principal alternative is an actor or representative of the state it stands for
 4 accepted names of distinct identities do not overlap (parent/child institutions stay distinct)
 5 no target is a principal
 6 no location is a principal
 7 an actor that is also an item's publisher is named in the item text, not only as its source
 8 roundup items contribute no evidence: each principal is mentioned in a non-roundup item
 9 secondary actors have role actor and are not principals
10 principals match the owner-reviewed sheet exactly

Usage: python evaluations/entities/scripts/gold_audit.py [--prefreeze]   (exit 1 on any failure;
       --prefreeze skips the hash check, for a revision not yet frozen)
"""
import json
import sys
from pathlib import Path

import yaml

from osint_monitor.benchmark import entities as eb
from osint_monitor.processors.actor_roles import is_roundup

ROOT = eb.GOLD_DIR

# Approved principal(s) column of entity-resolution-evaluation-sheet-owner-reviewed.md: one entry per principal,
# alternatives separated by "|" where the sheet writes "A / B".
OWNER = {
    "D01": ["Spain"], "D02": ["Pete Hegseth"], "D03": ["U.S. Navy", "US Department of Defense"], "D04": [],
    "D05": ["Saudi Arabia"], "D06": ["Israel"], "D07": ["United States", "United Kingdom"], "D08": ["Russia"],
    "D09": [], "D10": ["Argentina"], "D11": ["Estonia"], "D12": ["Estonia"], "D13": ["Italy|Italian government"],
    "D14": [], "D15": ["Russia|Vladimir Putin"], "D16": ["U.S. Customs and Border Protection"], "D17": ["Israel"],
    "D18": ["United States|Donald Trump"], "D19": ["United States"], "D20": ["Malaysia"], "D21": ["Malaysia"],
    "D22": ["U.S. Court of Appeals for the D.C. Circuit"], "D23": ["Donald Trump|United States"],
    "D24": ["Iran", "United States"], "D25": ["European Commission", "Council of the European Union"],
}


class _NoDuplicates(yaml.SafeLoader):
    pass


def _mapping(loader, node, deep=False):
    keys = [loader.construct_object(k, deep=deep) for k, _ in node.value]
    dup = {k for k in keys if keys.count(k) > 1}
    if dup:
        raise ValueError(f"duplicate keys {sorted(dup)} at line {node.start_mark.line + 1}")
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


_NoDuplicates.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def roles_of(dev, name):
    return set((dev.roles.get(name) or "").split("|")) - {""}


def main() -> int:
    failures, notes = [], []

    def check(n, ok, msg):
        if not ok:
            failures.append(f"[{n}] {msg}")

    # 2: duplicate keys anywhere (a YAML mapping silently keeps the last one)
    try:
        yaml.load((ROOT / "gold.yaml").read_text(encoding="utf-8"), Loader=_NoDuplicates)
    except ValueError as e:
        check(2, False, str(e))
    devs, names = eb.load_gold(ROOT, check_hashes="--prefreeze" not in sys.argv)
    raw = yaml.safe_load((ROOT / "gold.yaml").read_text(encoding="utf-8"))

    # 4: accepted-name overlap between identities
    seen = {}
    for canonical, accepted in names.items():
        for n in accepted:
            other = seen.setdefault(n, canonical)
            check(4, other == canonical, f"'{n}' accepted for both {other} and {canonical}")

    for dev in devs:
        k = dev.key
        for name, role in dev.roles.items():
            for r in role.split("|"):
                check(0, r in eb.ROLES, f"{k} {name}: unknown role {r}")
        for name, pr in dev.principal_roles.items():
            check(0, pr in eb.PRINCIPAL_ROLES, f"{k} {name}: unknown principal_role {pr}")
        principal_names = {a for alts in dev.principals for a in alts}
        # 1, 5, 6
        for alts in dev.principals:
            acting = [a for a in alts if "actor" in roles_of(dev, a)
                      or ("representative" in roles_of(dev, a) and "actor" in roles_of(dev, dev.represents.get(a, "")))]
            check(1, bool(acting), f"{k} principal {'|'.join(alts)} has no actor role")
            for a in alts:
                r = roles_of(dev, a)
                check(5, not (r and r <= {"target"}), f"{k} principal {a} is a target")
                check(6, not (r and r <= {"location"}), f"{k} principal {a} is a location")
                stands_for = any(dev.represents.get(b) == a for b in alts)    # "Trump|United States"
                check(1, not r or "actor" in r or "representative" in r or stands_for,
                      f"{k} principal alternative {a} has role {dev.roles.get(a)}")
        # 3
        for name, role in dev.roles.items():
            if "representative" in role.split("|"):
                check(3, name in dev.represents, f"{k} representative {name} has no `represents`")
        for person, entity in dev.represents.items():
            check(3, "actor" in roles_of(dev, entity) or entity in principal_names,
                  f"{k} {person} represents {entity}, which neither acts nor is a principal")
            check(3, "representative" in roles_of(dev, person) or "actor" in roles_of(dev, person),
                  f"{k} {person} has `represents` but role {dev.roles.get(person)}")
        # 9
        for name, pr in dev.principal_roles.items():
            if pr == "secondary":
                check(9, name not in principal_names, f"{k} secondary actor {name} is a principal")
                check(9, "actor" in roles_of(dev, name), f"{k} secondary actor {name} has role {dev.roles.get(name)}")
            elif pr in ("lead", "co_principal"):
                check(9, name in principal_names, f"{k} {pr} {name} is not among the principals")
        leads = [n for n, pr in dev.principal_roles.items() if pr == "lead"]
        check(9, len(leads) <= 1, f"{k} has {len(leads)} lead principals")
        # 7, 8: evidence per item
        mentioned = {}          # canonical -> set of item ids naming it in headline/lead
        for item_id, ms in dev.mentions.items():
            for m in ms:
                mentioned.setdefault(m.canonical, set()).add(item_id)
        roundups = set(dev.roundup_items) | {i["id"] for i in dev.items if is_roundup(i["title"] or "")}
        for extra in sorted(roundups - set(dev.roundup_items)):
            notes.append(f"{k} item {extra} is a roundup by headline (runtime is_roundup), not listed in roundup_items")
        for alts in dev.principals:
            items_naming = set().union(*(mentioned.get(a, set()) for a in alts))
            check(8, bool(items_naming - roundups),
                  f"{k} principal {'|'.join(alts)} is named only in roundup items {sorted(items_naming)}")
        sources = {i["id"]: i["source"] for i in dev.items}
        for name, role in dev.roles.items():
            if "actor" not in role.split("|"):
                continue
            accepted = names.get(name, {eb.norm(name)})
            for item_id, src in sources.items():
                s = eb.norm(src)
                if any(a and (s == a or s.startswith(a + " ")) for a in accepted):
                    check(7, bool(mentioned.get(name)), f"{k} actor {name} appears only as publisher ({src})")
                    notes.append(f"{k} actor {name} is also item {item_id}'s publisher ({src}); named in items "
                                 f"{sorted(mentioned.get(name, ()))}")
        # 10
        gold = sorted(tuple(sorted(a)) for a in dev.principals)
        owner = sorted(tuple(sorted(p.split("|"))) for p in OWNER[k])
        check(10, gold == owner, f"{k} principals {gold} != owner sheet {owner}")
    check(10, set(OWNER) == {d.key for d in devs}, "Development set differs from the owner sheet")
    check(0, set(raw["developments"]) == {d.key for d in devs}, "loader dropped a Development")

    print(f"{len(devs)} Developments, {sum(len(d.principals) for d in devs)} principals, "
          f"{sum(len(d.roles) for d in devs)} roles")
    for n in notes:
        print("note:", n)
    for f in failures:
        print("FAIL", f)
    print("audit:", "FAILED" if failures else "passed (checks 1-10)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
