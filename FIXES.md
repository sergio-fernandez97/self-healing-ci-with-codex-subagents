# Autofix workflow changes

## 1. Pin `uv` to version `0.9.13`

In both CI workflows, we install `uv` with:

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v1
  with:
    version: "0.9.13"
```

Why this change is needed:

- This repository defines test dependencies in the standardized `[dependency-groups]` table in [pyproject.toml](/Users/sergio.fernandez/Documents/AI-Initiative/AI-Literacy-Culture-Sales/courses/Coding-Assistants-&-AI-Agents/april-26/self-healing-ci-with-codex-subagents/pyproject.toml), not in `requirements.txt` and not as a published extra:

```toml
[dependency-groups]
dev = [
  "httpx>=0.27,<1.0",
  "pytest>=8.0,<9.0",
]
```

- The workflow commands rely on `uv` understanding dependency groups:

```bash
uv sync --group dev
uv run --group dev pytest -q
```

- Dependency groups are a relatively recent standardized feature in the Python packaging ecosystem. The `uv` documentation explicitly notes that `dependency-groups` are "recently standardized" and may not be supported consistently across tools.
- Because the workflow depends on that feature, using an unspecified `uv` version in CI is risky. If GitHub Actions installs an older or behaviorally different `uv` build, the workflow may not understand `--group dev` correctly or may resolve groups differently than expected.
- Pinning `uv` to `0.9.13` makes the workflow deterministic. Every runner gets the same CLI behavior, the same parsing of `[dependency-groups]`, and the same `uv sync` / `uv run` semantics that we validated locally.
- This is especially important in CI because the autofix flow is already diagnosing test failures. We do not want the repair workflow itself to fail because the package manager changed underneath it.

Why `--group dev` may fail depending on the `uv` version:

- In this project, `dev` is not an arbitrary string. It is the dependency group name declared under `[dependency-groups]`.
- The `--group <name>` flag tells `uv` to include that named dependency group when syncing or running commands.
- If the installed `uv` version does not fully support the current dependency-group feature set, the workflow can fail before tests even start, because `pytest` and `httpx` live in that `dev` group.
- In other words, when `--group dev` is unavailable or behaves differently, the CI job is not merely "missing a flag"; it is missing access to the very dependencies required to run the test suite.

Important nuance:

- According to current `uv` behavior, the `dev` group is special-cased and included by default during `uv sync` and `uv run`.
- That means that on `uv 0.9.13`, commands like these are generally equivalent for this repository:

```bash
uv sync --group dev
uv sync
```

and:

```bash
uv run --group dev pytest -q
uv run pytest -q
```

- So the main reason to keep `--group dev` is clarity, not necessity. It makes the workflow self-documenting by showing that the test tools come from the `dev` dependency group.
- If you hit an environment where `--group dev` is not accepted, the practical fallback for this repository is usually to rely on the default `dev` group behavior instead of the explicit flag, provided the installed `uv` still supports `[dependency-groups]`.

Why we still pin the version even if `dev` is default:

- Relying on defaults is not the same as relying on stable tooling behavior.
- The pin is not only about the existence of `--group dev`; it is about keeping the whole dependency-resolution and command-execution model stable across local runs, CI runs, and the autofix workflow.
- `0.9.13` is the known-good version for this repository, so pinning it removes one class of CI failures that has nothing to do with the application being repaired.

## 2. Run the self-heal script directly in GitHub Actions

Before:

```bash
uv run ./scripts/self_heal.sh
```

After:

```bash
./scripts/self_heal.sh
```

Why this change is needed:

- `self_heal.sh` is a shell script, not a Python entrypoint, so wrapping it in `uv run` adds an unnecessary execution layer.
- The autofix workflow already installs dependencies earlier with `uv sync --group dev`, so the script does not need `uv` to start.
- Running the script directly keeps the CI step simpler and avoids coupling the shell-script launch path to `uv` runtime behavior.

## 3. Run Codex without its internal sandbox inside CI

Before:

```bash
codex exec --enable child_agents_md --full-auto --skip-git-repo-check - < "$PROMPT_FILE"
```

After:

```bash
codex exec --enable child_agents_md --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check - < "$PROMPT_FILE"
```

Why this change is needed:

- `--full-auto` implies Codex runs commands in its own `workspace-write` sandbox.
- On GitHub Actions, that internal sandbox was failing with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, so the agent could not run even basic commands like `ls` or `pytest`.
- `--dangerously-bypass-approvals-and-sandbox` disables Codex's internal sandbox and approval prompts, which is appropriate here because the workflow is already running inside an isolated GitHub Actions runner.
- Without this change, the autofix agent fails before it can inspect the repository or apply a repair.

What `--enable child_agents_md` means here:

- `--enable` turns on an optional Codex feature for this run.
- Here it enables `child_agents_md`, so the CI repair prompt can use the child-agent workflow described in `AGENTS.md`.
- It is written explicitly so the workflow does not depend on that feature being enabled globally.

What `--skip-git-repo-check` means here:

- `--skip-git-repo-check` tells Codex not to stop and verify the Git repository before starting.
- In CI, that avoids an unnecessary preflight check because the workflow already knows which checkout it is running on.
- The flag does not change the repo; it only lets the repair run start more directly.
