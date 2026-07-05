import json
from eval_harness.models import EvalCase, EvalResult


def save_results(results: list[EvalResult], path: str, summary: dict) -> None:
    with open(path, "w") as f:
        json.dump({"summary": summary, "results": [r.to_dict() for r in results]}, f, indent=2)

def load_cases(path: str) -> list[EvalCase]:
    try:
        with open(path, "r") as f:
            data = json.load(f)
            cases = []
            for d in data:
                if not isinstance(d, dict):
                    raise ValueError(f"Expected a dict in cases file, got {type(d).__name__}: {d}")
                if "input" not in d or "expected" not in d:
                    raise ValueError(f"Case is missing 'input' or 'expected' keys: {d}")
                if not isinstance(d["input"], str):
                    raise ValueError(f" 'input' must be a string, got {type(d['input']).__name__}: {d}") 
                if not isinstance(d["expected"], str ):
                    raise ValueError(f" 'expected' must be a string, got {type(d['expected']).__name__}: {d}") 
                cases.append(EvalCase.from_dict(d))
                
        return cases
    except FileNotFoundError:
        raise FileNotFoundError(f"Cases file not found: {path}") from None
    except json.JSONDecodeError as e:
        raise ValueError(f"Cases file is not valid JSON: {path}\n{e}") from None



