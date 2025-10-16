import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from agents.coder_agent import CoderAgent

if __name__ == "__main__":
    plan = {
        "modules": [
            {
                "name": "utils.py",
                "tasks": [
                    "Implement validate_inputs(total_apples: int, num_people: int) -> None that verifies both parameters are integers, total_apples >= 0, num_people >= 1; raise ValueError with clear messages on invalid input.",
                    "Implement format_distribution(distribution: list[int], output_format: str = 'text') -> str supporting 'text' and 'json' outputs. For 'text', return a human-readable per-person list and totals; for 'json', return a JSON string.",
                    "Add type hints and comprehensive docstrings to both functions with examples.",
                    "Include lightweight internal checks (assertions) to ensure distribution sums match total when used in integrated flows.",
                ],
            },
            {
                "name": "divide_apples.py",
                "tasks": [
                    "Implement distribute_apples(total_apples: int, num_people: int) -> list[int] that returns a list of length num_people describing how many apples each person gets.",
                    "Algorithm: compute base = total_apples // num_people, remainder = total_apples % num_people. Give base apples to each person, then distribute the remainder by adding +1 to the first 'remainder' people (left-to-right).",
                    "Ensure the function validates inputs by calling utils.validate_inputs and raises ValueError for invalid values.",
                    "Ensure the returned list sums to total_apples (include an assertion as a safety check).",
                    "Add type hints, a docstring describing behavior and examples (including the 100 apples / 10 people example where each person gets 10).",
                    "Include a __main__ demo block that prints the distribution for 100 apples among 10 people using utils.format_distribution with both text and json examples.",
                ],
            },
            {
                "name": "cli.py",
                "tasks": [
                    "Implement a command-line interface using argparse that accepts positional arguments total_apples (int) and num_people (int) and an optional flag --json to output JSON.",
                    "Validate inputs via utils.validate_inputs and call divide_apples.distribute_apples to compute the distribution.",
                    "Format and print the result using utils.format_distribution; exit with non-zero status on input validation errors and print helpful usage/error messages.",
                    "Add examples in the help text showing the command to divide 100 apples among 10 people.",
                ],
            },
            {
                "name": "tests/test_divide_apples.py",
                "tasks": [
                    "Write pytest unit tests importing distribute_apples from divide_apples and validate_inputs from utils.",
                    "Test case: test_equal_division_100_10 - dividing 100 apples among 10 people returns [10,10,10,10,10,10,10,10,10,10].",
                    "Test case: test_remainder_distribution - dividing 101 apples among 10 people returns a distribution with sum 101 and the first person(s) receiving the extra apples (e.g., first 1 person gets 11, rest 10).",
                    "Test case: test_zero_apples - dividing 0 apples among N people returns a list of zeros of length N.",
                    "Test case: test_one_person - dividing any positive number among 1 person returns [total_apples].",
                    "Test case: test_invalid_inputs_raise - non-integer or negative apples or num_people < 1 should raise ValueError from validate_inputs.",
                    "Ensure tests assert both per-person values and that sum(distribution) == total_apples for each scenario.",
                ],
            },
        ]
    }

    coder = CoderAgent()
    generated = coder.generate_code(plan)

    for filename, code in generated.items():
        print(f"\n--- {filename} ---\n{code[:300]}...")
