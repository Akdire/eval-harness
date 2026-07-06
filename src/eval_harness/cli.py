import argparse
from eval_harness.storage import load_cases, save_results
from eval_harness.runner import run_eval
from eval_harness.reporting import summarize
from eval_harness.graders import exact_match, normalized_match, contains_match

GRADERS = {"exact": exact_match, "normalized": normalized_match, "contains": contains_match}

def example_system(text: str) -> str:
    """Trivial stand-in system — always returns a fixed string. Replace with your real system."""

    return "example output"

def print_summary(summary: dict) -> None:
    print(f"Total:  {summary['total']}")
    print(f"Passed:  {summary['passed']}")
    print(f"Failed:  {summary['failed']}")
    print(f"Errored:  {summary['errored']}")
    print(f"Pass_rate:  {summary['pass_rate'] * 100:.1f}%")

def main():
    parser = argparse.ArgumentParser(description="Run the eval harness")
    parser.add_argument("cases_path", help="Path to the JSON cases file")
    parser.add_argument("--grader", default="exact", choices=GRADERS.keys(), help="Grader to use: exact, normalized, contains")
    args = parser.parse_args()

    grader = GRADERS[args.grader]
   
    cases = load_cases(args.cases_path)
    results = run_eval(cases, example_system, grader)
    summary = summarize(results)
    print_summary(summary)
    save_results(results, "results.json", summary)
    print(f"Results saved to results.json") 


if __name__ == "__main__": main()


"""
1)One sentence: what is this project? (Resist listing features. Say what it does and for whom. "A small, focused Python library for evaluating AI system outputs against expected results, with pluggable graders." — something like that, in your words.)

2) The "why it exists" paragraph (2–3 sentences): what problem does it solve, why would a developer reach for it instead of writing their own? Your "small but important, install-don't-rebuild" framing goes here.

3) A "quick start" code block: the minimal import-and-use example — a developer imports run_eval, defines their system, picks a grader, runs it. Write the ~6 lines a user would copy.

Answer:1) this project is A small, focused Python library for running structured evaluations of AI system outputs against expected results, using pluggable graders — aimed at developers who need a lightweight, ready-to-use eval loop.

2) Writing a reliable eval loop from scratch is boilerplate most developers repeat — load cases, call a system, compare outputs, aggregate stats, save results. eval-harness packages that loop into a composable, install-ready library with validated I/O, structured result types, and three grading strategies out of the box. Reach for it when you want to focus on your system under test, not the scaffolding around it.

3) from eval_harness.storage import load_cases, save_results
from eval_harness.runner import run_eval
from eval_harness.reporting import summarize
from eval_harness.graders import normalized_match

def my_system(text: str) -> str:
    return call_your_model_here(text)  # replace with your real system

cases = load_cases("cases.json")
results = run_eval(cases, my_system, normalized_match)
summary = summarize(results)
save_results(results, "results.json", summary)
print(f"Pass rate: {summary['pass_rate'] * 100:.1f}%")




"""