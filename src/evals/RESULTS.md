# Eval Results — Norsk Tutor Correction Engine

Running log of measured eval runs. **Append one row per run.** Never edit past rows.

## How to read this

- **Detection** — of the error cases, how many fired a correction on the right fragment. Product metric.
- **Restraint** — of the clean cases, how many correctly stayed silent (empty corrections). Product metric.
- **Severity / Type / Fix acc** — field-level label accuracy on the cases that expect a correction.
- **Prompt ver / Grader ver** — always record both. When a number moves, you must know whether the *prompt* or the *grader* changed, or you can't attribute the improvement.
- **Notes** — one line: what changed since the last row + the hypothesis being tested.

Keep Detection and Restraint separate from field accuracy — they are the behaviors that define whether the tutor is good. A drop there is a real regression.

## Runs

| Date | Prompt ver | Grader ver | Cases | Detection | Restraint | Severity acc | Type acc | Fix acc | Overall | Notes / what changed |
|------|-----------|-----------|-------|-----------|-----------|--------------|----------|---------|---------|----------------------|
| 2026-07-09 | v1 | g1 (fix=normalized) | 10 | 5/5 | 5/5 | 4/5 | 2/5 | 1/5 | 5/10 | Baseline. Detection + restraint perfect. `fix` grader too strict (normalized_match). `type` fails on preposition cases (grammar/collocation overlap). |
| 2026-07-09 | v1 | g2 (fix+type=dict) | 10 | 5/5 | 5/5 | — | 4/5 | 5/5 | 8/10 | Added got/expected detail to correction_type and fix. Fix grader now passing all cases. Type still misses 'interessert på' (got: grammar, expected: collocation). |
| 2026-07-09 | v1 | g3 (all()+severity fix) | 10 | 5/5 | 5/5 | 4/5 | 4/5 | 5/5 | 9/10 | Fixed all() to read val["ok"] for dict fields. One remaining failure: 'interessert på musikk' — both severity and correction_type miss (collocation misclassified as grammar). |

## Milestones

- **2026-07-09** — First measured eval run. Engine catches every planted error (5/5) and stays silent on all clean sentences (5/5). Baseline established: 5/10 overall. Two failure clusters identified — a too-strict `fix` grader (cosmetic) and a real `[TYPES]` prompt ambiguity on preposition typing (Type 2/5).

## Known defects / open items

- **`correction_type` instability on collocations** — 'interessert på' classified as `grammar` instead of `collocation`. Engine conflates preposition errors with collocations. Fix: clarify collocation definition in prompt to cover verb+preposition pairings. (Prompt v2, pending.)
- ~~**`fix` grader too strict**~~ — resolved in g2. All fix cases now passing.
- ~~**Report doesn't show got vs expected on a miss**~~ — resolved in g2. `correction_type` and `fix` now show got/expected detail.
