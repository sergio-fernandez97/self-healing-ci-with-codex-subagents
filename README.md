# Self-Healing CI With Codex Subagents

This repository contains a small FastAPI app and a simple retry loop in `scripts/self_heal.sh` that sketches a self-healing CI workflow.

## uv Setup

This repository is configured for `uv` via `pyproject.toml`.

Create the virtual environment:

```bash
uv venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project and dev dependencies:

```bash
uv sync --dev
```

Run the test suite:

```bash
uv run pytest
```

If you want `uv` to use the pinned Python version from `.python-version`, install it first:

```bash
uv python install
```

## Agent Definitions

Agent prompts live in `.agents/`.

- `tester`: reproduces failures with `pytest`, summarizes failing tests, and hands off a factual report to the next debugging stage.

The first scaffolded agent is available at `.agents/tester.md`.
