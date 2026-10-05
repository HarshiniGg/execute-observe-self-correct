# Execute, Observe, Self-Correct AI Agent

An AI-powered Python code generation agent that generates code from natural-language tasks, executes the generated code, observes the result, and automatically attempts to correct failures.

## Features

- Generates Python code using Groq LLM.
- Executes generated code in a separate Python subprocess.
- Captures stdout, stderr, errors, and timeout results.
- Tests generated code using Python assertions.
- Automatically asks the LLM to correct failed code.
- Supports up to 3 correction attempts.
- Logs every execution attempt.
- Records whether each attempt passed or failed.
- Uses `.env` for the Groq API key.
- Avoids `eval()` and `exec()` in the main application process.

## Project Structure

```text
Execute_Observe_Self_Correct/
│
├── main.py
├── agent.py
├── executor.py
├── prompts.py
├── requirements.txt
├── .gitignore
├── .env
├── generated_code/
└── logs/