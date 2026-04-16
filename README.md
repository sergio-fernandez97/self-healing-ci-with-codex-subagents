# Self-Healing CI With Codex Subagents

This repository is a small FastAPI project for a live session on GitHub Actions CI, Codex CLI custom commands, reusable skills, and self-healing pipelines.

## Prerequisites

Before the live session, make sure you have:

- Python 3.11+
- `uv` installed locally
- Codex CLI installed locally
- local Codex authentication already configured

For the GitHub Actions auto-fix flow, add this repository secret:

- `OPENAI_API_KEY`

The workflow logs the CLI in non-interactively from that secret before it runs `codex exec`.

In GitHub:

1. Open the repository.
2. Go to `Settings -> Secrets and variables -> Actions`.
3. Add a new repository secret named `OPENAI_API_KEY`.

If the auto-fix workflow logs `401 Unauthorized: Missing bearer or basic authentication in header`, GitHub Actions did not provide a usable `OPENAI_API_KEY` to the job. Re-check the repository secret name and where the workflow is running from.

## Local Setup

From the repository root:

```bash
uv python install
uv venv
source .venv/bin/activate
uv sync --group dev
uv run --group dev pytest -q
```

## Live Session Guide

### 1. Review the code first

Start by reading the files that define the app and the expected behavior:

- `app/main.py`
- `app/api/routes_users.py`
- `app/services/user_service.py`
- `app/models/user.py`
- `tests/api/test_users.py`
- `tests/services/test_user_service.py`

Current structure:

- `app/` contains the FastAPI app, routes, models, and service layer.
- `tests/` contains API and service tests.
- `scripts/self_heal.sh` shows the intended local self-healing loop.
- `.github/workflows/ci.yml` runs CI on GitHub.
- `.github/workflows/codex-autofix.yml` is the self-healing workflow.
- `.github/workflows/grade.yml` posts an automatic PR grade.

### 2. Baseline: run tests locally

Run:

```bash
uv sync --group dev
uv run --group dev pytest -q
```

For the demo, the tests should fail first. That failing output is the input to the repair workflow.

### 3. Show CI failing through a pull request

Create a branch:

```bash
git checkout -b demo/break-ci
```

Commit and push the current failing state:

```bash
git add -A
git commit -m "demo: break CI"
git push -u origin demo/break-ci
```

Open a pull request from `demo/break-ci` to `main` and confirm that the CI workflow turns red.

### 4. Fix locally with Codex

Create a Codex custom command named `/fix-ci` with this prompt:

```text
Fix failing CI by making `uv run --group dev pytest -q` pass.

Rules:
- Do NOT modify files under `tests/`
- Prefer minimal diffs
- Keep existing function signatures

Steps:
1) Run tests: `uv run --group dev pytest -q`
2) Read failures and determine root cause
3) Patch only `app/` code
4) Re-run `uv run --group dev pytest -q` until green

When done:
- Summarize what changed
- List the commands you ran
```

For this repo, use these subagent roles during the local fix:

- `tester`: collect failures
- `linter`: check style issues
- `typechecker`: check typing issues
- `diagnoser`: find root cause
- `fixer`: apply fixes
- `reviewer`: validate fixes

Then run this prompt locally in Codex:

```text
Modify the code in app/ in order to pass the failing tests in tests/. Deploy the following agents in the given order:
1. tester: collect failures
2. linter: check style issues
3. typechecker: check typing issues
4. diagnoser: find root cause
5. fixer: apply fixes
6. reviewer: validate fixes
```

Verify locally:

```bash
uv run --group dev pytest -q
```

Commit and push the fix:

```bash
git add -A
git commit -m "fix: make tests pass"
git push -u origin demo/break-ci
```

### 5. Run the local self-heal script

Before moving to GitHub Actions, demonstrate the local repair loop from the repository itself.

Run:

```bash
chmod +x scripts/self_heal.sh
uv run ./scripts/self_heal.sh
```

Expected behavior:

- the script runs tests locally with `uv`
- if tests fail, it invokes `codex exec` non-interactively with the self-healing prompt
- it retries until tests pass or the retry limit is reached

This is the local version of the same repair flow later automated in GitHub Actions.

### 6. Run the self-healing CI workflow in GitHub Actions

Now demonstrate the non-interactive repair flow.

First, break the app again with a small source-only change under `app/`, then commit and push:

```bash
git add -A
git commit -m "demo: break CI again"
git push -u origin demo/break-ci
```

Then run the workflow manually:

1. Go to `GitHub -> Actions`.
2. Select `Codex Auto-fix`.
3. Click `Run workflow`.
4. Set the `branch` input to `demo/break-ci`.
5. Start the workflow.

Expected behavior:

- the workflow checks out the branch
- runs tests and captures output
- runs Codex non-interactively
- commits a patch back to the same branch
- re-runs tests

Back in the pull request, you should see:

- a new bot commit
- CI turning green again

### 7. Review the automatic grade

The `Grade` workflow runs automatically on every pull request update and comments a score.

Typical rubric:

- tests pass: 6 points
- `tests/` unchanged: 2 points
- diff small enough: 2 points

You should see a PR comment with:

- the score, for example `10/10`
- the public test exit code
- whether `tests/` changed
- the changed files
- the approximate line count

## How the Self-Healing Workflow Works

This repository demonstrates two repair modes:

1. Local repair with Codex CLI:
   Review code, run `uv run --group dev pytest -q`, invoke Codex with the subagent sequence, patch only `app/`, and re-run tests until green.
2. GitHub Actions auto-fix:
   Trigger `.github/workflows/codex-autofix.yml`, let Codex run non-interactively, push the patch back to the branch, and let CI validate the result.

Important rule for both modes:

- do not modify `tests/`

## Challenge for Students

### Objective

Build your own tiny self-healing CI repository from scratch in any programming language.

Your repository must include:

1. source code with 2 to 4 small functions
2. tests that can fail
3. a CI workflow that runs tests on pull requests
4. a Codex auto-fix workflow that can repair failures and push a patch
5. a grading workflow that comments an automatic score on the pull request

### Deliverables

Submit a repository containing:

- `README.md` explaining:
  - how to run tests locally
  - how to run CI
  - how to run the auto-fix workflow
  - how grading works
- `.github/workflows/ci.yml`
- `.github/workflows/codex-autofix.yml`
- `.github/workflows/grade.yml`
- a Codex prompt file used by the auto-fix workflow, for example `.codex/commands/fix-ci.md`

### Step-by-Step Assignment

#### 1. Create a new repository

```bash
git clone <repo-url>
cd <repo-name>
```

#### 2. Choose a minimal project skeleton

Examples:

- Python: `src/`, `tests/`, `pyproject.toml`
- Node or TypeScript: `src/`, `test/`, `package.json`
- Go: `*.go`, `_test.go`
- Java: a minimal Maven or Gradle project
- Rust: `src/lib.rs`, `tests/`

Keep it small. Two to four functions is enough.

#### 3. Write your own functions

Good candidates:

- string utilities
- math helpers
- parsing helpers
- date formatting helpers

At least one function should be easy to break so you can demonstrate the repair flow.

#### 4. Write deterministic tests

Your tests must run with one command and should be deterministic.

Examples:

- Python: `uv run pytest -q`
- Node: `npm test`
- Go: `go test ./...`

#### 5. Verify locally with passing tests first

Before adding CI, make sure the baseline is green locally.

#### 6. Add CI

Create `.github/workflows/ci.yml` that:

- runs on `pull_request`
- runs on pushes to `main`
- checks out code
- installs dependencies
- runs the test command for your language

#### 7. Add Codex Auto-fix

Create `.github/workflows/codex-autofix.yml` that:

- runs via `workflow_dispatch`
- accepts a `branch` input
- checks out the target branch
- runs tests and captures logs
- runs Codex non-interactively
- re-runs tests
- commits and pushes the fix

#### 8. Add a Codex prompt file

Create a prompt file such as `.codex/commands/fix-ci.md` and adapt it to your language and test command.

It should tell Codex:

- the goal is to make tests pass
- do not weaken or delete tests
- prefer minimal diffs
- fix the root cause in source code
- run the tests again after changes

#### 9. Add grading

Create `.github/workflows/grade.yml` that:

- runs on pull requests
- runs tests
- checks quality gates
- comments a score on the pull request

Adjust path checks if your repo does not use `tests/` or `src/`.

### Student Flow

#### A. Push the initial green version

```bash
git add -A
git commit -m "init: add code, tests, CI, autofix, grading"
git push -u origin main
```

Confirm CI is green on `main`.

#### B. Create a failing pull request

```bash
git checkout -b challenge/break-ci
git add -A
git commit -m "break: introduce failing tests"
git push -u origin challenge/break-ci
```

Open a pull request to `main` and confirm CI fails.

#### C. Run auto-fix

From GitHub Actions, run the `Codex Auto-fix` workflow with:

```text
branch = challenge/break-ci
```

Confirm:

- a new commit is pushed to the branch
- CI turns green

#### D. Check the PR grade

Confirm that the grading workflow comments a score on the pull request.

### Success Criteria

You pass the assignment if your repository demonstrates all of the following:

- CI runs on pull requests and can fail
- auto-fix runs and pushes a patch
- CI turns green after auto-fix
- grading comments a score
- tests were not weakened or deleted

### Bonus

Add a pull request summary comment after the auto-fix workflow pushes its patch.

## Reference

- [How AI assistance impacts the formation of coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills)
