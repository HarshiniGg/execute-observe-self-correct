import subprocess
import sys
import tempfile
from pathlib import Path


def execute_code(code, test_code, timeout=8):
    """
    Run generated code and its test assertions in a separate process.
    Returns the output, error, and whether the tests passed.
    """

    full_code = code + "\n\n" + test_code

    with tempfile.TemporaryDirectory() as temp_dir:
        script_path = Path(temp_dir) / "generated_test.py"
        script_path.write_text(full_code, encoding="utf-8")

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=temp_dir
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "passed": result.returncode == 0,
                "error": "" if result.returncode == 0 else result.stderr,
                "timed_out": False
            }

        except subprocess.TimeoutExpired as error:
            return {
                "stdout": error.stdout or "",
                "stderr": error.stderr or "",
                "passed": False,
                "error": f"Execution timed out after {timeout} seconds.",
                "timed_out": True
            }

        except Exception as error:
            return {
                "stdout": "",
                "stderr": str(error),
                "passed": False,
                "error": str(error),
                "timed_out": False
            }