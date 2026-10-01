"""Render evaluations/identity/phase2-baseline.md from runs/phase2-baseline.json (no replay, no runtime code)."""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pct(n, d):
    return f"{n}/{d} ({100 * n / d:.0f}%)" if d else f"{n}/0 (–)"


def main() -> int:
    r = json.loads((ROOT / "runs" / "phase2-baseline.json").read_text(encoding="utf-8"))
    W = r["windows"]
    T = Counter()
    for w in W:
        T.update(w["tally"])

    def metrics(t, w=None):
        split_fail = t["together"] - t["together_and_same"]
        merge_fail = t["gold_same"] - t["together_and_same"]
        diff = t["pairs"] - t["gold_same"]
        return [pct(t["together_and_same"], t["together"]), pct(t["together_and_same"], t["gold_same"]),
                pct(split_fail, diff), pct(merge_fail, t["gold_same"]),
                pct(t.get("cross_tick_same_retained", 0), t.get("cross_tick_same", 0))]

    mixed = sum(len(w["mixed"]) for w in W)
    labelled = sum(len(w["labelled_developments"]) for w in W)
    multi = sum(w["multi_item"] for w in W)
    dups = sum(len(w["duplicate_memberships"]) for w in W)
    in_devs = sum(w["items_in_developments"] for w in W)
    ledger = [dict(e, window=w["window"]) for w in W for e in w["ledger"]]
    classes = Counter(e["error_class"] for e in ledger)
    by_fail = defaultdict(Counter)
    for e in ledger:
        by_fail[e["failure"]][e["error_class"]] += 1

    out = ["# Phase 2 baseline: current Development identity on gold revision 2", "",
           "What the **current** runtime (Phase 1 branch, no change) does with Development identity before any Phase 2 "
           "code exists. Gold: revision 2 (`gold/manifest.yaml`, sha256 " + r["gold_sha256"][:12] + "...).",
           "",
           "Method:",
           "- the three **development** windows are replayed tick by tick (4 × 12 h) twice, each in a clean temporary DB, by "
           "`scripts/phase2_baseline.py`;",
           "- the **holdout window is neither replayed nor scored**;",
           "- a gold pair counts as *kept together* when, after the later item's tick, both items share a Development ID. "
           "The current code never deletes, splits or merges Developments, so final membership plus each membership's "
           "tick is the full history;",
           "- AMBIGUOUS cases (1) are excluded.",
           "",
           "**Scope caveat.** These are rates over the gold's candidate pairs (chosen by the candidate rules), not over "
           "every pair in the windows. They measure the decisions the gold covers.", "",
           "## Baseline metrics", "",
           "| Window | Pairs scored | Continuity precision | Continuity recall | Split failures (DIFFERENT kept together) "
           "| Merge failures (SAME kept apart) | ID stability (cross-tick SAME retained) |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    for w in W:
        out.append(f"| {w['window']} | {w['tally']['pairs']} | " + " | ".join(metrics(w["tally"])) + " |")
    out.append(f"| **all development** | **{T['pairs']}** | " + " | ".join(f"**{m}**" for m in metrics(T)) + " |")
    out += ["",
            "Definitions:",
            "- **Continuity precision:** of the gold pairs the runtime keeps under one ID, the share that are SAME.",
            "- **Continuity recall:** of the SAME pairs, the share kept under one ID.",
            "- **Split failure rate:** over DIFFERENT pairs.",
            "- **Merge failure rate:** over SAME pairs.",
            "- **ID stability:** SAME pairs whose items arrive at different ticks and where the later item joined the "
            "earlier item's Development.",
            "",
            "| Development-level | Result |", "|---|---:|",
            f"| Mixed-Development rate (Developments containing a gold DIFFERENT pair / Developments containing any "
            f"gold pair) | {pct(mixed, labelled)} |",
            f"| Mixed Developments / all multi-item Developments | {pct(mixed, multi)} |",
            f"| Duplicate-membership rate (items in more than one Development / items in any Development) | "
            f"{pct(dups, in_devs)} |",
            f"| Memberships added after their Development was created (overlap extensions) | "
            f"{sum(w['late_memberships'] for w in W)} memberships in {sum(w['overlap_extensions'] for w in W)} Developments |",
            "", "## Determinism result", ""]
    for d in r["determinism"]:
        out.append(f"- **{d['window']}**: run 1 vs run 2 {'identical' if d['identical'] else 'DIFFERENT'}; run 1 vs the "
                   f"committed review trace {'identical' if d['identical_to_review_trace'] else 'DIFFERENT'}"
                   + (f" ({'; '.join(d['run1_vs_run2'][:3] or d['run1_vs_review_trace'][:3])})"
                      if not (d['identical'] and d['identical_to_review_trace']) else ""))
    out += ["",
            "**Findings (this run and the investigation before it):**",
            "- Development IDs, memberships and the tick of every membership were identical in every replay of every "
            "development window: 2026-08-21 was replayed 7 times, the others 4 times each.",
            "- **One order difference was observed.** In an earlier baseline run, 2026-08-21's pre-segmentation cluster "
            "list and cut list at tick 2 came out in a different **order** in one of two runs. Contents (as sets) and the "
            "resulting Developments were the same.",
            "- **Reproduced:** replaying the window as if 30 minutes more had passed between ticks gives the same "
            "tick-2 difference.",
            "- **Exact source, part 1:** `clustering.recent_items` (`osint_monitor/processors/clustering.py:43-53`) "
            "selects items with `cutoff = datetime.utcnow() - 48 h`. Identical inputs processed at a different wall-clock "
            "moment can therefore drop an edge item from the candidate set, which renumbers HDBSCAN's labels and reorders "
            "the clusters.",
            "- **Exact source, part 2:** `persist_clusters` is order-dependent. It walks clusters in list order, extends "
            "the first existing Development an overlapping cluster meets (`_find_overlapping_event`, unordered `.first()`, "
            "`clustering.py:548-557`), and allocates new Development IDs in that order.",
            "- **Impact:** no identity difference was observed in these windows, but the mechanism can change which "
            "Development an overlapping cluster joins, and which ID a new Development gets, between runs of identical "
            "input.",
            "- **This replay is not the daemon.** In the daemon the window cutoff is a real input, a time; the replay "
            "harness only makes it visible. Phase 2's identity rule must not depend on the order clusters are produced "
            "in, nor on `.first()`.",
            "", "## Error ledger", "",
            f"{len(ledger)} failures: "
            + ", ".join(f"{k} {v}" for k, v in sorted(Counter(e['failure'] for e in ledger).items())) + ".",
            "", "| Error class | Split failures | Merge failures |", "|---|---:|---:|"]
    for cls in sorted(classes, key=lambda c: -classes[c]):
        out.append(f"| {cls} | {by_fail['split failure (DIFFERENT kept together)'][cls]} | "
                   f"{by_fail['merge failure (SAME kept apart)'][cls]} |")
    out += ["", "| Case | Gold | Current | Development IDs | Ticks | Items | Error class | Likely root cause |",
            "|---|---|---|---|---|---|---|---|"]
    for e in sorted(ledger, key=lambda e: e["case"]):
        devs = " / ".join(",".join(f"D{x}" for x in d) or "–" for d in e["developments"])
        items = "<br>".join(f"`{i['id']}` [{i['source']}, {i['lang']}] {i['title'][:70]}" for i in e["items"])
        out.append(f"| {e['case']} | {e['gold'].split('_')[0]} | {e['current']} | {devs} | t{e['ticks'][0]}/t{e['ticks'][1]} "
                   f"| {items} | {e['error_class']} | {e['root_cause']} |")
    out += ["", "## Duplicate membership findings", ""]
    if dups:
        for w in W:
            for i, ds in w["duplicate_memberships"].items():
                out.append(f"- {w['window']}: `{i}` in {', '.join('D' + d for d in ds)}")
    else:
        out += ["- **No item belongs to more than one Development** in any development window: 0 of "
                f"{in_devs} items in Developments.",
                "- The mechanism that produced the 24 double memberships in the real snapshot (audit S1) needs a cluster "
                "that bridges two existing Developments across runs. These short replays did not trigger it.",
                "- The schema now forbids a duplicate *pair*, UNIQUE(event, item) from Phase 1, but **not** one item in "
                "two Developments."]
    out += ["", "## Single-source findings", "",
            "Product rule: *single-source evidence stays below the Development layer until independently "
            "corroborated.* Not implemented. Developments formed from one outlet only:", ""]
    singles = [(w["window"], s) for w in W for s in w["single_source"]]
    for wid, s in singles:
        out.append(f"- {wid} D{s['development']}: {s['items']} items, all {s['source']}: \"{s['summary'][:110]}\"")
    if not singles:
        out.append("- none")
    out += ["",
            f"**{len(singles)} single-source Development(s) in the development windows.** The runtime creates them "
            "(minimum cluster size 2, same-outlet links allowed when headlines are near-identical) and only flags them "
            "SINGLE_SOURCE. The real 2026-09-30 snapshot had more (INV E53, SX E17, audit section 6).",
            "", "## Roundup findings", ""]
    rdevs = [(w["window"], x) for w in W for x in w["roundups"]]
    out += ["| Window / Development | Members | Roundup item | Sources with / without roundup | Corroboration | "
            "Summary is the roundup headline | Gold DIFFERENT pairs among the other members |", "|---|---:|---|---:|---|---|---|"]
    for wid, x in rdevs:
        out.append(f"| {wid} D{x['development']} | {x['members']} | {', '.join(x['roundup_items'])} | "
                   f"{x['sources_with']} / {x['sources_without']} | {x['corroboration']} | "
                   f"{'**yes**' if x['summary_is_roundup_with_reports_present'] else 'no'} | "
                   f"{', '.join(x['gold_different_pairs_among_non_roundup_members']) or 'none'} |")
    inflated = sum(1 for _, x in rdevs if x["source_count_inflated"])
    summ = sum(1 for _, x in rdevs if x["summary_is_roundup_with_reports_present"])
    out += ["",
            f"- **False corroboration:** {inflated} of {len(rdevs)} Developments with a roundup item would have one "
            "source fewer without it. The roundup is counted as an independent source (both are rated PROBABLE).",
            f"- **Roundup as summary:** in {summ} of {len(rdevs)} the Development's summary is the roundup headline, "
            "although a normal report of the occurrence is a member.",
            "- **Roundup forcing unrelated occurrences together:** no gold DIFFERENT pair among the non-roundup members "
            "of these Developments. The one roundup-driven split failure (C080) is the roundup item itself grouped "
            "with a report of one of its many stories.",
            "", "## Main structural failure modes", ""]
    out += [
        f"1. **Whole-storyline overmerge ({classes.get('whole-storyline overmerge', 0)}) and late attachment "
        f"({classes.get('late attachment', 0)}) are the split failures.**",
        "   - Distinct actions of one storyline are linked by similar language: the Ebola warning vs the vaccine trial "
        "vs the dose arrival; settlers vs activists; the Trump AI order vs the self-regulation accord vs the expert "
        "commentary.",
        "   - Persisted Developments then absorb later clusters by overlap. D6 in the multilingual window holds the AI "
        "order, the self-regulation accord and the expert commentary at creation (tick 3). At tick 4 it absorbs an "
        "interpreter feature, the strategic oil loan and a diesel export ban.",
        "   - Segmentation cuts only within a batch, and overlap-merge undoes its cuts at persistence.",
        f"2. **Segmentation interaction ({classes.get('segmentation interaction', 0)}) is the main merge failure.**",
        "   - Guards cut links between reports of one occurrence: the FlyDubai incident across Italian outlets; the "
        "Pentagon release vs the Raytheon contract report; the UN live coverage vs the UN press summary.",
        "   - Most of these pairs differ in headline wording, language, or report vs official release.",
        f"3. **Missed continuation and grouping ({classes.get('missed continuation', 0)} + "
        f"{classes.get('other', 0)} other).**",
        "   - SAME items stay outside the Development, or form a second one.",
        "   - Examples: the Commission proposal vs its Q&A and factsheet (C034, C103); a Security Council meeting record "
        "vs its briefing (C064); the drone crash vs the same attack (C076); cross-language pairs.",
        "   - Contributing factor: the embedding model is English-only.",
        f"4. **Single-source promotion ({classes.get('single-source promotion', 0)}) and roundup contamination "
        f"({classes.get('roundup contamination', 0)}).**",
        "   - These are few in the ledger, but they are policy gaps rather than tuning issues:",
        "     - a single-source Development exists;",
        "     - roundups count as sources and become summaries.",
        "5. **Order dependence.** Identity can depend on cluster order and on `.first()`; see *Determinism result*.",
        "",
        "Nothing in this document proposes a change; Phase 2 design starts from these failure modes and the contract "
        "(`development-identity-contract.md`).", "", "PHASE 2 BASELINE COMPLETE", ""]
    (ROOT / "phase2-baseline.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    print("wrote phase2-baseline.md;", len(ledger), "ledger rows;", dict(classes))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
