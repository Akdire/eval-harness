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
| 2026-07-09 | v2 | g2 (fix+type=dict) | 10 | 5/5 | 5/5 | — | 4/5 | 5/5 | 8/10 | Added got/expected detail to correction_type and fix. Fix grader now passing all cases. Type still misses 'interessert på' (got: grammar, expected: collocation). |
| 2026-07-09 | v2 | g3 (all()+severity fix) | 10 | 5/5 | 5/5 | 4/5 | 4/5 | 5/5 | 9/10 | Fixed all() to read val["ok"] for dict fields. One remaining failure: 'interessert på musikk' — both severity and correction_type miss (collocation misclassified as grammar). |
| 2026-07-12 | v2 | g3 | 30 | 20/25 | 6/6 | 3/5 | 11/20 | 16/20 | 15/30 | Expanded to 30 cases (added collocation, naturalness, register, pragmatics, level sensitivity). Detection drops: 2 NoCoLA grammar cases missed ('Man må husker', 'Det kan skaper'). Type biggest gap: naturalness consistently misclassified as collocation (5/5 miss), register/pragmatics boundary blurry (1 miss each). Fix mostly clean (3 misses). Severity only on baseline cases — 2 misses (severity=high where medium expected). |
| 2026-07-12 | v3 | g3 | 30 | 21/25 | 5/6 | 3/5 | 17/23 | 20/23 | 20/30 | Prompt v3. Naturalness now almost fully resolved (5/5 type passes). Restraint drops 1: B1 level-sensitivity case fires incorrectly. 2 fix misses remain ('gjøre krav', 'kjipt'). Severity inflation unchanged (2 misses, both got:high expected:medium). 'Kan De' still misclassified as register instead of pragmatics. 2 NoCoLA detection misses persist. |
| 2026-07-12 | v4 | g3 | 30 | 20/25 | 5/6 | 2/5 | 16/23 | 20/23 | 20/30 | CEFR reference + grammar guard. No net improvement — same overall score as v3. Severity worse (3 misses vs 2: 'gleder meg for' and 'lyst på' now also inflated). 'interessert på' type reverted to grammar miss. Fix miss on 'gjøre krav' resolved but 'kjipt' and 'signere' still miss. NoCoLA detection and 'Kan De' pragmatics unchanged. |
| 2026-07-12 | v4 | g4 (harness fix) | 30 | 21/25 | 5/6 | 2/5 | 16/23 | 18/23 | 19/30 | Harness fix (run_engine_eval v2) — NoCoLA modal blindness resolved: 'Det kan skaper' now detected. 1 new fix miss ('er i en hast'). Prompt/engine unchanged — all movement attributed to harness correction. Remaining: severity inflation (3), 'interessert på' type, 4 fix misses, 'Kan De' pragmatics, level-sensitivity B1 restraint. |
| 2026-07-12 | v4 | g5 (5-run pass-rate) | 30×5 | — | — | — | — | — | 16/30 stable | Harness v3: 5 runs/case, pass-rate reporting. Reveals nondeterminism. 16 cases pass 100% of runs. 8 FLAKY. 6 FAIL 0%. Severity fields removed from all cases this run. |
| 2026-07-13 | v4 | g5 | 30×5 | — | — | — | — | — | 17/30 stable | Reverted temperature=0 (crashed all 30 cases). Severity=None on all cases confirmed stable. 17 stable passes (+1 vs prev). 8 FLAKY: 'lyst på' type (20%), 'Man må husker' (40%), 'kjipt' fix (40%), 'gjøre krav' fix (60%), 'betale oppmerksomhet' type (80%), 'Det kan skaper' fix (80%), 'er i en hast' fix (80%), 'liker boken' type (80%). 5 hard FAIL: 'gleder meg for' type, 'interessert på' type, 'Kan De' type, 'signere' fix, 'bestemte å' type+silence. |

## Milestones

- **2026-07-09** — First measured eval run. Engine catches every planted error (5/5) and stays silent on all clean sentences (5/5). Baseline established: 5/10 overall. Two failure clusters identified — a too-strict `fix` grader (cosmetic) and a real `[TYPES]` prompt ambiguity on preposition typing (Type 2/5).
- **2026-07-12 v2** — Expanded to 30 cases covering all 6 correction types + level sensitivity. Detection 20/25, restraint 6/6. Clear pattern: `naturalness` type invisible to engine — all 5 classified as `collocation`. Prompt v3 hypothesis: sharpen naturalness/collocation boundary.
- **2026-07-12 v3** — Naturalness resolved (5/5). Overall 20/30. Remaining clusters: severity inflation, 2 NoCoLA detection misses, register/pragmatics boundary, 2 fix misses, level-sensitivity B1 restraint miss.

## Known defects / open items

- **Nondeterminism on 8 cases** — pass-rate between 20%-80% across 5 runs. Root cause: temperature/sampling, not prompt logic. Fix: lower temperature or add majority-vote across N runs. (Engine config, pending.)
- **Detection misses on modal+infinitive errors** — 'Man må husker' 0% detection across 5 runs (hard fail). 'Det kan skaper' 80% (flaky). (Prompt v5, pending.)
- **register/pragmatics boundary** — 'Kan De' (archaic pronoun) still classified as register instead of pragmatics. (Prompt v4, pending.)
- **Severity inflation** — engine rates medium errors as high on 2 baseline cases ('gleder meg for', 'interessert på'). (Prompt v4, pending.)
- **Fix misses on short spans** — 'gjøre krav' → 'stille krav' and 'kjipt' → 'beklagelig' both miss. Fix grader may be too strict on short replacements. (Investigate g4.)
- **Level-sensitivity B1 restraint miss** — 'bestemte å' fires at B1 when it should stay silent. Engine not respecting level. (Prompt v4, pending.)
- ~~**`naturalness` invisible to engine**~~ — resolved in v3. All 5 naturalness cases now pass.
- ~~**`fix` grader too strict**~~ — resolved in g2.
- ~~**Report doesn't show got vs expected on a miss**~~ — resolved in g2.
- ~~**`correction_type` instability on collocations**~~ — resolved in v3.
