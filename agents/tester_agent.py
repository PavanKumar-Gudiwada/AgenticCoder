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
            ["pytest", "-q", self.workspace],
            capture_output=True,
            text=True
        )
        return result.stdout or result.stderr

    def analyze_results(self, output: str) -> str:
        if "passed" in output.lower():
            return "✅ All tests passed!"
        elif "no tests ran" in output.lower():
            return "⚠️ No tests found in workspace."
        else:
            return f"❌ Tests failed. Details:\n{output}"
