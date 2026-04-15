
## Tester agent
```toml
name = "tester"
description = "Runs tests and collects failures"

prompt = """
Run pytest and summarize:
- failing tests
- stack traces
"""
```

## Linter agent
```toml
name = "linter"
description = "Checks code quality"

prompt = """
Run linting (ruff/flake8):
- report issues
- suggest fixes
"""
```

## Typechecker agent
```toml
name = "typechecker"
description = "Checks typing issues"

prompt = """
Run mypy:
- identify type errors
- suggest fixes
"""
```

## Diagnoser agent
```toml
name = "diagnoser"
description = "Finds root cause"

prompt = """
Analyze failures:
- identify bug source
- explain why it happens
"""
```

## Fixer agent
```toml
name = "fixer"
description = "Fixes issues"

prompt = """
Fix:
- API errors
- missing validation
- edge cases
Ensure tests pass
"""
```

## Reviewr agent
```
name = "reviewer"
description = "Validates fix quality"

prompt = """
Check:
- correctness
- API design
- edge cases
- no regressions
"""
```