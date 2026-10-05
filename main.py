import json
from datetime import datetime
from pathlib import Path

from agent import generate_code, correct_code
from executor import execute_code


BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "logs" / "attempts.json"

MAX_ATTEMPTS = 3


def save_attempt(task, attempt_number, code, result):
    """Save each code attempt and its execution result."""

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "task": task,
        "attempt": attempt_number,
        "code": code,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": result["error"],
        "passed": result["passed"],
        "timed_out": result["timed_out"],
    }

    if LOG_FILE.exists():
        try:
            history = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            history = []
    else:
        history = []

    history.append(record)

    LOG_FILE.write_text(
        json.dumps(history, indent=4),
        encoding="utf-8"
    )


def run_task(task, test_code):
    """Generate, execute, observe, and correct code up to 3 attempts."""

    print("\n" + "=" * 60)
    print(f"Task: {task}")
    print("=" * 60)

    code = generate_code(task)
  

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n--- Attempt {attempt} of {MAX_ATTEMPTS} ---")
        if "DEMO_FAIL" in task and attempt == 1:
            code = "def add(a, b):\n    return a - b"
               

        print("\nGenerated code:")
        print(code)
        result = execute_code(code, test_code)

        

        print("\nProgram output:")
        print(result["stdout"] or "(No output)")

        if result["passed"]:
            print("\n" + "✅ TEST PASSED!")
        else:
            print("\n" + "❌ TEST FAILED!")
            print("Error:")
            print(result["error"] or result["stderr"])

        save_attempt(task, attempt, code, result)

        if result["passed"]:
            return True

        if attempt < MAX_ATTEMPTS:
            print("\nAsking AI to correct the code...")
            code = correct_code(
                task,
                code,
                result["error"] or result["stderr"],
                result["stdout"],
            )

    print("\n❌ Task did not pass after 3 attempts.")
    return False


if __name__ == "__main__":
    task = input("Enter your Python task: ").strip()

    if not task:
        print("Please enter a task.")
    else:
        test_code = input(
            "\nEnter Python test code (example: assert add(2, 3) == 5):\n"
        ).strip()

        if not test_code:
            print("Please provide a test assertion.")
        else:
            run_task(task, test_code)