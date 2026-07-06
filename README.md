# eval-harness

![tests](https://github.com/Akdire/eval-harness/actions/workflows/tests.yml/badge.svg)

A small, focused Python library for running structured evaluations of AI system
outputs against expected results, using pluggable graders — aimed at developers
who need a lightweight, ready-to-use eval loop.

## Why this exists

Writing a reliable eval loop from scratch is boilerplate most developers repeat:
load cases, call a system, compare outputs, aggregate stats, save results.
`eval-harness` packages that loop into a composable, install-ready library with
validated I/O, structured result types, and three grading strategies out of the
box. Reach for it when you want to focus on your system under test, not the
scaffolding around it.

## Install

```bash
pip install -e .
```

Requires Python 3.9+.

## Quick start

Point the harness at a set of cases, hand it *your* system and a grader, and it
runs the loop for you:

```python
from eval_harness import load_cases, run_eval, summarize, save_results, normalized_match

def my_system(text: str) -> str:
    return call_your_model_here(text)  # replace with your real system

cases = load_cases("cases.json")
results = run_eval(cases, my_system, normalized_match)
summary = summarize(results)

save_results(results, "results.json", summary)
print(f"Pass rate: {summary['pass_rate'] * 100:.1f}%")
```

The system under test is any callable of shape `(input: str) -> str`. Because
you inject it, the harness stays independent of any particular model or provider
— it evaluates whatever you hand it.

## Cases file format

Cases are a JSON array of objects, each with exactly two string keys, `input`
and `expected`:

```json
[
  { "input": "What is 2 + 2?", "expected": "4" },
  { "input": "What is the capital of France?", "expected": "Paris" },
  { "input": "Translate 'hello' to Spanish", "expected": "hola" }
]
```

Loading is strict by design: a missing file, invalid JSON, a non-array top
level, a missing key, or a non-string value each raises immediately rather than
silently producing a partial or empty run. An eval's value is a trustworthy
number, so bad input fails loudly instead of quietly corrupting the result.

## Graders

A grader is any callable of shape `(output: str, expected: str) -> bool`. Three
are included:

| Grader | Matches when |
|---|---|
| `exact_match` | `output` equals `expected` exactly (case- and whitespace-sensitive) |
| `normalized_match` | they match after trimming surrounding whitespace and lowercasing |
| `contains_match` | `expected` appears anywhere inside `output` (empty `expected` never matches) |

Because every grader shares the same shape, they are interchangeable — swap one
for another without touching the runner. You can also pass your own function; if
it takes `(output, expected)` and returns a `bool`, it works.

## Results

`run_eval` returns one `EvalResult` per case, each carrying its `EvalCase`, the
system's `actual_output`, and a `status`:

| Status | Meaning |
|---|---|
| `PASSED` | the system ran and the grader accepted the output |
| `FAILED` | the system ran but the grader rejected the output |
| `ERROR` | the system raised while producing the output |

The three states are a real distinction: a wrong answer and a crash are
different failures, and the harness keeps them separate. A system that raises on
one case does not stop the run — that case is recorded as `ERROR` and the loop
continues, so one bad case never invalidates the whole batch.

`summarize` rolls the results into totals and a pass rate:

```python
{"total": 3, "passed": 2, "failed": 1, "errored": 0, "pass_rate": 0.67}
```

## Command line

A thin CLI runs the full pipeline on a cases file against a built-in example
system — useful as a runnable demo:

```bash
python -m eval_harness cases.json --grader exact
```

`--grader` accepts `exact`, `normalized`, or `contains` (default: `exact`). The
CLI's `example_system` is a documented stand-in that always returns a fixed
string; for real evaluation, use the library and inject your own system as shown
in the quick start.

## Testing

The library ships with 26 tests across 7 test files, covering all three graders
(including edge cases like empty and whitespace-only inputs), the runner's
pass / fail / error branching, case and result serialization in both directions,
and the summarizer's counts and pass-rate calculation — including the empty-run
guard.

```bash
pytest
```

## Design notes

- **Injected dependencies.** The system under test and the grader are handed in,
  not built in. This keeps the runner independent of any model, makes every
  component testable in isolation, and lets graders be swapped freely.
- **Structured results over booleans.** Outcomes are a three-state enum, not a
  bool, because "wrong" and "errored" are genuinely different and a report needs
  to tell them apart.
- **Strict boundaries.** Input is validated where it enters the system; bad data
  fails loudly rather than propagating a silent, misleading result.

## Roadmap

Planned work is tracked in [ROADMAP.md](ROADMAP.md).
