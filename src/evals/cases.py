"""
Eval cases for the Norwegian correction engine.

GROUND-TRUTH STATUS (MVP): grammar/collocation baseline is high-confidence.
The advanced cases (register/pragmatics/naturalness) are LLM-CONSENSUS
(Gemini drafted, Grok reviewed, both agreed) and are marked `teacher-review pending`.
They test "does the engine agree with LLM consensus", not "with a Norwegian teacher" —
good enough to catch regressions and gross failures for the MVP.

CONTEXT IS FIRST-CLASS. Register/pragmatics/naturalness errors often cannot be judged
from a lone sentence — the situation decides. So EvalCase carries an optional `context`:
the prior conversation turns that establish the setting. The runner feeds context + input
to the engine as history, exactly as a live conversation would.
"""

from dataclasses import dataclass, field


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
    # prior (role, content) turns that set the situation. Empty = context-free case.
    context: tuple[tuple[str, str], ...] = ()
    tags: tuple[str, ...] = ()


# ===========================================================================
# GROUP 1 — Baseline: grammar / collocation detection (high confidence)
# ===========================================================================
BASELINE = [
    EvalCase("Jeg gleder meg for helgen.", "B2",
             ExpectedCorrection(fragment="gleder meg for", fix="gleder meg til",
                                correction_type="grammar", severity=None),
             tags=("detection", "grammar")),
    EvalCase("Jeg har lyst på å reise.", "B2",
             ExpectedCorrection(fragment="lyst på å reise", fix="lyst til å reise",
                                correction_type="grammar", severity=None),
             tags=("detection", "grammar")),
    EvalCase("Han er interessert på musikk.", "B2",
             ExpectedCorrection(fragment="interessert på", fix="interessert i",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation")),
    EvalCase("Jeg gjør en beslutning.", "B2",
             ExpectedCorrection(fragment="gjør en beslutning", fix="tar en beslutning",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation")),
    EvalCase("Jeg er enig med at det er sant.", "B2",
             ExpectedCorrection(fragment="enig med at", fix="enig i at",
                                correction_type="grammar", severity=None),
             tags=("detection", "grammar")),
    # --- NoCoLA native-verified (real learner errors, corrected by native speakers) ---
    EvalCase("Man må husker at begge to er viktige!", "B2",
             ExpectedCorrection(fragment="må husker at", fix="må huske at",
                                correction_type="grammar", severity=None),
             tags=("detection", "grammar", "native_verified")),
    EvalCase("Det kan skaper mange problemer for mennesker.", "B2",
             ExpectedCorrection(fragment="kan skaper mange", fix="kan skape mange",
                                correction_type="grammar", severity=None),
             tags=("detection", "grammar", "native_verified")),
    EvalCase("Han mener at for mange karbohydrater fører til man utvikler diabetes.", "B2",
             ExpectedCorrection(fragment="til man", fix="til at man",
                                correction_type="grammar", severity=None),
             tags=("detection", "grammar", "native_verified")),
]

# ===========================================================================
# GROUP 2 — Collocation (context-free; the error holds regardless of situation)
# LLM-consensus, teacher-review pending.
# ===========================================================================
COLLOCATION = [
    EvalCase("Det er vanskelig å betale oppmerksomhet i lange forelesninger.", "C1",
             ExpectedCorrection(fragment="betale oppmerksomhet", fix="følge med",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),
    EvalCase("Statsministeren skal gi en tale under åpningen.", "C1",
             ExpectedCorrection(fragment="gi en tale", fix="holde en tale",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),
    EvalCase("Jeg har lyst til å spørre et spørsmål om kontrakten.", "C1",
             ExpectedCorrection(fragment="spørre et spørsmål", fix="stille et spørsmål",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),
    EvalCase("Fagforeningen valgte å gjøre krav om bedre vilkår.", "C1",
             ExpectedCorrection(fragment="gjøre krav", fix="stille krav",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),

    EvalCase("Han valgte å gjøre et forslag om å utsette prosjektet.", "C1",
             ExpectedCorrection(fragment="gjøre et forslag", fix="komme med et forslag",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),

     EvalCase("Vi burde ha en titt på rapporten før møtet.", "C1",
             ExpectedCorrection(fragment="ha en titt", fix="ta en titt",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),

     EvalCase("Jeg liker denne nye boken din veldig mye.", "C1",
             ExpectedCorrection(fragment="veldig mye", fix="veldig godt",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),
    EvalCase("Forklaringen din gjør ikke helt mening for meg.", "C1",
             ExpectedCorrection(fragment="gjør ikke helt mening", fix="gir ikke helt mening",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "teacher_pending")),
]

# ===========================================================================
# GROUP 3 — Naturalness (context-free calques). LLM-consensus, teacher-review pending.
# ===========================================================================
NATURALNESS = [
    
    EvalCase("Det er billig, men på den andre hånden kan det bli dyrt.", "C1",
             ExpectedCorrection(fragment="på den andre hånden", fix="på den andre siden",
                                correction_type="naturalness", severity=None),
             tags=("detection", "naturalness", "teacher_pending")),
   
    EvalCase("Unnskyld, men jeg er i en hast og må løpe.", "C1",
             ExpectedCorrection(fragment="er i en hast", fix="har det travelt",
                                correction_type="naturalness", severity=None),
             tags=("detection", "naturalness", "teacher_pending")),
]

# ===========================================================================
# GROUP 4 — Register (CONTEXT-DEPENDENT: prior turns set the formality).
# The context establishes the situation; the learner's turn violates its register.
# LLM-consensus, teacher-review pending.
# ===========================================================================
REGISTER = [
    # Casual invitation to a friend -> bureaucratic 'angående' is too stiff.
    EvalCase("Hei! Har du lyst til å ta en øl og snakke angående ferieplanene?", "C1",
             ExpectedCorrection(fragment="angående", fix="om",
                                correction_type="register", severity=None),
             context=(("assistant", "Hei! Så hyggelig å høre fra deg. Hva skjer?"),),
             tags=("detection", "register", "teacher_pending")),
    # Formal business email -> slang 'kjipt' is too casual.
    EvalCase("Det er kjipt at leveransen ble forsinket på grunn av streiken.", "C1",
             ExpectedCorrection(fragment="kjipt", fix="beklagelig",
                                correction_type="register", severity=None),
             context=(("assistant", "God dag. Kan du oppdatere oss om leveransen til kunden?"),),
             tags=("detection", "register", "teacher_pending")),
    # Casual message to a colleague -> legalistic 'såfremt' is too formal.
    EvalCase("Jeg kan sende deg rapporten i morgen, såfremt du trenger den raskt.", "C1",
             ExpectedCorrection(fragment="såfremt", fix="hvis",
                                correction_type="register", severity=None),
             context=(("assistant", "Hei! Rekker du å sende meg rapporten snart?"),),
             tags=("detection", "register", "teacher_pending")),
]

# ===========================================================================
# GROUP 5 — Pragmatics (CONTEXT-DEPENDENT: politeness is relative to situation).
# Kept small and defensible; culturally heavier cases held for teacher review.
# ===========================================================================
PRAGMATICS = [
    # 'De' as a formal pronoun is outdated in modern Norwegian -> use 'du'.
    EvalCase("Kan De fortelle meg hvor kontoret til direktøren er?", "C1",
             ExpectedCorrection(fragment="De", fix="du",
                                correction_type="pragmatics", severity=None),
             tags=("detection", "pragmatics", "teacher_pending")),
    # Professional setting -> blunt imperative is too demanding; soften.
    EvalCase("Du må signere her nå.", "C1",
             ExpectedCorrection(fragment="Du må signere her nå",
                                fix="Fint om du kan signere her",
                                correction_type="pragmatics", severity=None),
             context=(("assistant", "Hei, jeg er saksbehandleren din. Er det noe jeg kan hjelpe med?"),),
             tags=("detection", "pragmatics", "teacher_pending")),
]

# ===========================================================================
# GROUP 6 — Restraint (correct Norwegian -> the engine MUST stay silent)
# ===========================================================================
RESTRAINT = [
    EvalCase("Jeg gleder meg til helgen.", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Kan du hjelpe meg med dette?", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Jeg har bodd i Norge i tre år.", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Jeg er enig med deg.", "B2", ExpectedSilence(), tags=("restraint",)),
    EvalCase("Jeg synes at filmen var veldig bra.", "B2", ExpectedSilence(), tags=("restraint",)),
]

# ===========================================================================
# GROUP 7 — Level sensitivity (SAME sentence, different level -> different outcome).
# The product-defining behavior: flag a subtle slip at C1, stay silent at B1.
# ===========================================================================
LEVEL_SENSITIVITY = [
    EvalCase("Jeg bestemte å dra tidlig.", "C1",
             ExpectedCorrection(fragment="bestemte å", fix="bestemte meg for å",
                                correction_type="collocation", severity=None),
             tags=("detection", "collocation", "level_sensitivity", "teacher_pending")),
    EvalCase("Jeg bestemte å dra tidlig.", "B1", ExpectedSilence(),
             tags=("restraint", "level_sensitivity")),
]


CASES: list[EvalCase] = (
    BASELINE + COLLOCATION + NATURALNESS + REGISTER + PRAGMATICS + RESTRAINT + LEVEL_SENSITIVITY
)
