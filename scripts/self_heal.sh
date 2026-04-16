#!/bin/bash
set -e

MAX_RETRIES=3
PROMPT_FILE=".codex/commands/fix-ci.md"

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "❌ OPENAI_API_KEY is not set. Configure the repository secret in GitHub Actions before running the auto-fix workflow."
  exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
  echo "❌ Missing prompt file: $PROMPT_FILE"
  exit 1
fi

# Ensure the CLI has an authenticated session in CI before calling `codex exec`.
printf '%s' "$OPENAI_API_KEY" | codex login --with-api-key

for i in $(seq 1 $MAX_RETRIES); do
  echo "🔁 Attempt $i..."

  if uv run --group dev pytest -q; then
    echo "✅ All checks passed"
    exit 0
  fi

  echo "⚠️ Running self-healing agents..."

  codex exec --enable child_agents_md --full-auto --skip-git-repo-check - < "$PROMPT_FILE"

done

echo "❌ Failed after retries"
exit 1
