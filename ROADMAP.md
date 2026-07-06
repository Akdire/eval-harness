# Roadmap

`eval-harness` v0.1 is a complete, tested core: cases, three graders, a runner
with error isolation, structured results, reporting, storage, and a demo CLI.
The items below are planned extensions, deliberately deferred so the core stays
small and shippable rather than half-built and broad.

## Planned

### LLM-as-judge grader
A grader that delegates the verdict to a language model — "given this output and
this reference answer, is the output acceptable?" — for evaluating open-ended,
semantic output that string comparison cannot judge (e.g. many valid phrasings
of the same correct answer).

It slots into the existing architecture unchanged: it conforms to the same
`(output, expected) -> bool` grader shape and is injected like any other. It is
deliberately planned *last* because, unlike the current graders, it is
non-deterministic, costs money per call, and is harder to test — so it is added
only on top of a foundation that is already proven with deterministic graders.

### CLI model integration
Extend the CLI beyond its built-in example system so it can evaluate a real
model behind an API — selecting a provider/model via arguments, handling
authentication, and managing rate limits and request errors.

This is scoped as CLI-layer work rather than core work: the library already
supports real systems today (inject any callable). The CLI extension is a
convenience layer for the common "point it at a hosted model" case, and it is
deferred because provider integration (auth, secrets, rate limiting) is a
self-contained project of its own.

## Non-goals (for now)

- Becoming a general-purpose evaluation platform. The aim is a focused,
  dependable eval loop for Python developers — install and use, rather than
  build from scratch — not a sprawling framework.
- Multi-language or multi-format case support beyond the current JSON contract.

## Sequencing

Roadmap work resumes after the primary consuming project (a language-learning
app whose correction engine this harness is intended to evaluate) reaches the
point of needing systematic evaluation. At that point the LLM-as-judge grader
becomes the natural next build, since it is what lets the harness score
open-ended, natural-language output.
