#!/bin/bash
set -e

MAX_RETRIES=3
PROMPT_FILE=".codex/commands/fix-ci.md"

if [ ! -f "$PROMPT_FILE" ]; then
  echo "❌ Missing prompt file: $PROMPT_FILE"
  exit 1
fi

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
