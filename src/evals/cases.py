"""
Eval cases for the Norwegian correction engine.

Ground-truth fixtures. Each EvalCase is either:
  - ExpectedCorrection : an error that SHOULD fire, with the expected label/fix
  - ExpectedSilence    : correct Norwegian that should produce NO correction

Cases are grouped by intent so coverage gaps are visible at a glance.
As the set grows, keep the grouping and keep the ground truth verified — a wrong
expected answer silently poisons the measurement.
"""

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
    tags: tuple[str, ...] = ()   # e.g. ("detection", "grammar") — used for per-category reporting


# ---------------------------------------------------------------------------
# GROUP 1 — Original baseline set (grammar / collocation detection + restraint)
# ---------------------------------------------------------------------------
BASELINE_CASES: list[EvalCase] = [
    EvalCase("Jeg gleder meg for helgen.", "B2",
             ExpectedCorrection(fragment="gleder meg for", fix="gleder meg til helgen",
                                correction_type="grammar", severity="medium"),
             tags=("detection", "grammar")),
    EvalCase("Jeg har lyst på å reise.", "B2",
             ExpectedCorrection(fragment="lyst på å reise", fix="lyst til å reise",
                                correction_type="grammar", severity="medium"),
             tags=("detection", "grammar")),
    EvalCase("Han er interessert på musikk.", "B2",
             ExpectedCorrection(fragment="interessert på", fix="interessert i musikk",
                                correction_type="collocation", severity="medium"),
             tags=("detection", "collocation")),
    EvalCase("Jeg gjør en beslutning.", "B2",
             ExpectedCorrection(fragment="gjør en beslutning", fix="tar en beslutning",
                                correction_type="collocation", severity="medium"),
             tags=("detection", "collocation")),
    EvalCase("Jeg er enig med at det er sant.", "B2",
             ExpectedCorrection(fragment="enig med at", fix="enig i at det er sant",
                                correction_type="grammar", severity="medium"),
             tags=("detection", "grammar")),
    EvalCase("Jeg gleder meg til helgen.", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Kan du hjelpe meg med dette?", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Jeg har bodd i Norge i tre år.", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Jeg er enig med deg.", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Jeg synes at filmen var veldig bra.", "B2", ExpectedSilence(), tags=("restraint",)),
]


# ---------------------------------------------------------------------------
# GROUP 2 — Vocabulary (wrong word / false friend — replacing ONE word fixes it)
# ---------------------------------------------------------------------------
# NOTE: verify these against a native speaker before trusting the numbers.
VOCABULARY_CASES: list[EvalCase] = [
    # "eventuelt" (possibly) is a false friend for "eventually" (til slutt).
    EvalCase("Eventuelt kom han hjem klokka ti.", "B2",
             ExpectedCorrection(fragment="Eventuelt", fix="Til slutt",
                                correction_type="vocabulary", severity="high"),
             tags=("detection", "vocabulary")),
    # "føle" vs "kjenne": "kjenner mange folk" = know people; "føler" is wrong here.
    EvalCase("Jeg føler mange folk i Oslo.", "B2",
             ExpectedCorrection(fragment="føler mange folk", fix="kjenner mange folk",
                                correction_type="vocabulary", severity="high"),
             tags=("detection", "vocabulary")),
]


# ---------------------------------------------------------------------------
# GROUP 3 — Register (grammatically fine, wrong level of formality)
# ---------------------------------------------------------------------------
REGISTER_CASES: list[EvalCase] = [
    # Overly bureaucratic phrasing in a casual "how are you" — register mismatch.
    EvalCase("Jeg vil med dette meddele at jeg har det bra.", "C1",
             ExpectedCorrection(fragment="vil med dette meddele",
                                fix="vil bare si", correction_type="register", severity="medium"),
             tags=("detection", "register")),
]


# ---------------------------------------------------------------------------
# GROUP 4 — Naturalness (all correct, just not how a native would phrase it)
# ---------------------------------------------------------------------------
NATURALNESS_CASES: list[EvalCase] = [
    # Literal translation of "I take a shower" — Norwegians say "dusjer".
    EvalCase("Jeg tar en dusj hver morgen.", "C1",
             ExpectedCorrection(fragment="tar en dusj", fix="dusjer",
                                correction_type="naturalness", severity="low"),
             tags=("detection", "naturalness")),
]


# ---------------------------------------------------------------------------
# GROUP 5 — Level sensitivity (SAME sentence, different level -> different outcome)
# The whole product thesis: a low-severity naturalness slip is flagged at C1
# but should be left alone at B1 (correcting it there just buries bigger errors).
# ---------------------------------------------------------------------------
LEVEL_SENSITIVITY_CASES: list[EvalCase] = [
    EvalCase("Jeg tar en dusj hver morgen.", "B1", ExpectedSilence(),
             tags=("restraint", "level_sensitivity")),   # too minor to flag at B1
    EvalCase("Jeg vil med dette meddele at jeg har det bra.", "B1", ExpectedSilence(),
             tags=("restraint", "level_sensitivity")),   # register nuance not a B1 priority
]


# ---------------------------------------------------------------------------
# GROUP 6 — Hard restraint (correct-but-unusual; must NOT over-correct)
# ---------------------------------------------------------------------------
HARD_RESTRAINT_CASES: list[EvalCase] = [
    # Correct, slightly formal, but perfectly fine — must stay silent.
    EvalCase("Jeg setter stor pris på hjelpen din.", "C1", ExpectedSilence(),
             tags=("restraint", "hard")),
    EvalCase("Det er ingenting i veien med det.", "C1", ExpectedSilence(),
             tags=("restraint", "hard")),
]


# ---------------------------------------------------------------------------
# The full set the runner imports.
# ---------------------------------------------------------------------------
CASES: list[EvalCase] = (
    BASELINE_CASES
    + VOCABULARY_CASES
    + REGISTER_CASES
    + NATURALNESS_CASES
    + LEVEL_SENSITIVITY_CASES
    + HARD_RESTRAINT_CASES
)