---
description: Fix failing CI in this repository by using the configured subagents in sequence and keeping changes minimal.
---

Fix failing CI by making `uv run --group dev pytest -q` pass.

Rules:
- Do NOT modify files under `tests/`
- Prefer minimal diffs
- Keep existing function signatures unless the failure clearly requires a change
- Prefer fixing application code, configuration, scripts, or documentation over changing expectations

Steps:
1. Run tests: `uv run --group dev pytest -q`
2. Read failures and determine root cause
3. Patch only the necessary files, prioritizing `app/`
4. Re-run `uv run --group dev pytest -q` until green

Deploy the following agents in the given order:
1. `tester`: collect failures
2. `linter`: check style issues
3. `typechecker`: check typing issues
4. `diagnoser`: find root cause
5. `fixer`: apply fixes
6. `reviewer`: validate fixes

When done:
- Summarize what changed
- List the commands you ran
