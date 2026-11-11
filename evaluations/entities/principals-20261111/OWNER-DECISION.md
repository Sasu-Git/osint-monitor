# Owner decision (2026-11-11): not merged

The fix in `74cdaea` (support counted per actor across its names) is **rejected for now** and kept as research
evidence. It fails its frozen gate (benchmark principal precision 20/25 → 22/28) and changes no outcome in the
126-case Situation replay, which is not enough leverage to change principal semantics.

The underlying problem is real: support split across names and representatives of one actor (Russia + Kremlin,
Ukraine + Zelensky). It needs a better formulation, for example deciding whether a representative's support counts
for the state at all, and when. That is a design question, not an accepted implementation.
