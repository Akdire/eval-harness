from dataclasses import dataclass


@dataclass
class ExpectedCorrection:
    severity: str | None = None
    correction_type: str | None = None
    fragment: str | None = None
    fix: str | None = None


@dataclass
class ExpectedSilence:
    pass


ExpectedOutcome = ExpectedCorrection | ExpectedSilence


@dataclass
class EvalCase:
    input: str
    level: str
    expected: ExpectedOutcome


CASES: list[EvalCase] = [
    # --- Detection + classification: a clear error SHOULD fire ---
    EvalCase(
        input="Jeg gleder meg for helgen.",
        level="B2",
        expected=ExpectedCorrection(
            fragment="gleder meg for", fix="gleder meg til helgen",
            correction_type="grammar", severity="medium"),
    ),
    EvalCase(
        input="Jeg har lyst på å reise.",
        level="B2",
        expected=ExpectedCorrection(
            fragment="lyst på å reise", fix="lyst til å reise",
            correction_type="grammar", severity="medium"),
    ),
    EvalCase(
        input="Han er interessert på musikk.",
        level="B2",
        expected=ExpectedCorrection(
            fragment="interessert på", fix="interessert i musikk",
            correction_type="collocation", severity="medium"),
    ),
    EvalCase(
        input="Jeg gjør en beslutning.",
        level="B2",
        expected=ExpectedCorrection(
            fragment="gjør en beslutning", fix="tar en beslutning",
            correction_type="collocation", severity="medium"),
    ),
    EvalCase(
        input="Jeg er enig med at det er sant.",
        level="B2",
        expected=ExpectedCorrection(
            fragment="enig med at", fix="enig i at det er sant",
            correction_type="grammar", severity="medium"),
    ),
    # --- Restraint: correct Norwegian must produce NO correction ---
    EvalCase(input="Jeg gleder meg til helgen.", level="B2", expected=ExpectedSilence()),
    EvalCase(input="Kan du hjelpe meg med dette?", level="B2", expected=ExpectedSilence()),
    EvalCase(input="Jeg har bodd i Norge i tre år.", level="B2", expected=ExpectedSilence()),
    EvalCase(input="Jeg er enig med deg.", level="B2", expected=ExpectedSilence()),
    EvalCase(input="Jeg synes at filmen var veldig bra.", level="B2", expected=ExpectedSilence()),
]