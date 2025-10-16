import subprocess
import os


class TesterAgent:
    def __init__(self, workspace="workspace"):
        self.workspace = workspace

    def run_tests(self) -> str:
        print("🧪 Running tests...")
        if not os.path.exists(self.workspace):
            return "No workspace found."

        # Run pytest in the workspace directory
        result = subprocess.run(
            ["pytest", "-q", self.workspace], capture_output=True, text=True
        )
        return result.stdout or result.stderr

    def analyze_results(self, output: str) -> str:
        # Convert output to lowercase for case-insensitive checks
        output_lower = output.lower()

        # 1. Check for failure summary first
        # This specifically looks for the "FAILED" keyword and "failed, X passed" pattern
        if "failed" in output_lower:
            # Check if 0 tests failed (e.g., if the word 'failed' appears in a traceback)
            # This is a robust way to check the summary line.
            import re

            # Regex to find the summary line like "X failed, Y passed"
            match = re.search(r"(\d+)\s+failed,", output_lower)

            if match and int(match.group(1)) > 0:
                return f"❌ Tests failed. Details:\n{output}"

            # Fall through if the failure count is 0, or if the failure was in "no tests ran"

        # 2. Check for "No tests ran"
        if "no tests ran" in output_lower or "no tests found" in output_lower:
            return "⚠️ No tests found in workspace."

        # 3. Check for successful completion (only if no failures were detected)
        # The output summary "X passed in Ys" often implies success if "failed" wasn't present.
        if "passed" in output_lower:
            return "✅ All tests passed!"

        # 4. Default fallback if output is unexpected
        return f"❓ Test results were ambiguous or incomplete. Raw output:\n{output}"
