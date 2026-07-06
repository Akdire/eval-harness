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



