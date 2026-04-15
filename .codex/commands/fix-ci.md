Fix failing CI by making `uv run pytest -q` pass.

Rules:
- Do NOT modify files under `tests/`
- Prefer minimal diffs
- Keep existing function signatures when possible
- Prefer fixing application code, configuration, scripts, or documentation instead of changing test expectations

Steps:
1. Run tests: `uv run pytest -q`
2. Read failures and determine root cause
3. Use these repo-local agents in order:
   1. `tester`: collect failures
   2. `linter`: check style issues
   3. `typechecker`: check typing issues
   4. `diagnoser`: find root cause
   5. `fixer`: apply fixes
   6. `reviewer`: validate fixes
4. Patch only the smallest relevant repo areas needed to make CI green
5. Re-run `uv run pytest -q` until green

When done:
- Summarize what changed
- List the commands you ran
