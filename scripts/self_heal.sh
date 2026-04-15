#!/bin/bash
set -e

MAX_RETRIES=3

for i in $(seq 1 $MAX_RETRIES); do
  echo "🔁 Attempt $i..."

  if uv run --group dev pytest -q; then
    echo "✅ All checks passed"
    exit 0
  fi

  echo "⚠️ Running self-healing agents..."

  codex "
  Modify the code in app/ in order to pass the failing tests in tests/. Deploy the
  following agents in the given order:  
  1. tester: collect failures
  2. linter: check style issues
  3. typechecker: check typing issues
  4. diagnoser: find root cause
  5. fixer: apply fixes
  6. reviewer: validate fixes
  "

done

echo "❌ Failed after retries"
exit 1
