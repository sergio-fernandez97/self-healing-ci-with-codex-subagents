#!/bin/bash
set -e

MAX_RETRIES=3
PROMPT=".codex/commands/fix-ci.md"

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "❌ OPENAI_API_KEY is not set. Configure the repository secret in GitHub Actions before running the auto-fix workflow."
  exit 1
fi

for i in $(seq 1 $MAX_RETRIES); do
  echo "🔁 Attempt $i..."

  if uv run --group dev pytest -q; then
    echo "✅ All checks passed"
    exit 0
  fi

  echo "⚠️ Running self-healing agents..."

  codex exec --full-auto --skip-git-repo-check "$PROMPT"

done

echo "❌ Failed after retries"
exit 1
