"""
diagnose_grammar_blindness.py — open the black box on the two grammar misses.

The eval only tells us the engine returned no correction matching our expected fragment.
It does NOT tell us WHY. This script dumps the RAW CorrectionTurn so we can see the
difference between three very different failures:
  - BLINDNESS   : corrections == []  (engine sees nothing wrong)
  - MISDIRECTION: corrections on a DIFFERENT fragment (it corrected something else)
  - MISLABEL    : correct fragment, but our matcher missed it

Run from the eval-harness root:  python diagnose_grammar_blindness.py
"""

from dotenv import load_dotenv
load_dotenv()

from engine.models import Message
from engine.run_turn import run_turn

PROBES = [
    ("Man må husker at begge to er viktige!", "B2"),
    ("Det kan skaper mange problemer for mennesker.", "B2"),
    # a control: a grammar error the engine DID catch, to compare against
    ("Han mener at for mange karbohydrater fører til man utvikler diabetes.", "B2"),
]

for text, level in PROBES:
    print("=" * 70)
    print(f"INPUT ({level}): {text!r}")
    turn = run_turn([Message(role="user", content=text)], level=level)
    print(f"tutor_reply: {turn.tutor_reply}")
    if not turn.corrections:
        print(">>> BLINDNESS: engine returned ZERO corrections.")
    for i, c in enumerate(turn.corrections):
        print(f"  correction[{i}]:")
        print(f"    original_fragment : {c.original_fragment!r}")
        print(f"    corrected_version : {c.corrected_version!r}")
        print(f"    correction_type   : {c.correction_type.value}")
        print(f"    severity          : {c.severity.value}")
        print(f"    explanation       : {c.explanation}")
    print()
