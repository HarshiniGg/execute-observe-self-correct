import os

from dotenv import load_dotenv
from groq import Groq

from prompts import (
    SYSTEM_PROMPT,
    build_generation_prompt,
    build_correction_prompt,
)

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found. Check that your .env file exists "
        "and contains your API key."
    )

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-120b"


def get_ai_response(prompt):
    """Send a prompt to Groq and return the generated text."""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def remove_code_fences(code):
    """Remove Markdown fences if the AI includes them."""

    code = code.strip()

    if code.startswith("```"):
        lines = code.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        code = "\n".join(lines).strip()

    return code


def generate_code(task):
    """Generate Python code for the given task."""

    prompt = build_generation_prompt(task)
    code = get_ai_response(prompt)

    return remove_code_fences(code)


def correct_code(task, previous_code, error, output):
    """Ask the AI to correct code that failed its test."""

    prompt = build_correction_prompt(
        task,
        previous_code,
        error,
        output,
    )

    code = get_ai_response(prompt)

    return remove_code_fences(code)