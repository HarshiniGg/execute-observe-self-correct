SYSTEM_PROMPT = """
You are a Python code generation assistant.

Rules:
1. Return only valid Python code.
2. Do not include Markdown code fences.
3. Write the function requested by the user.
4. Use clear and simple Python.
5. Do not use input() or require interactive input.
"""


def build_generation_prompt(task):
    return f"""
Write Python code for this task:

{task}

Return only the complete Python code.
"""


def build_correction_prompt(task, previous_code, error, output):
    return f"""
The Python code you generated failed its test.

Original task:
{task}

Previous code:
{previous_code}

Error:
{error}

Program output:
{output}

Fix the code so it passes the test.

Return only the complete corrected Python code.
"""