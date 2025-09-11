# Approvals Concept: Parrots

A parrot is a test double that records function calls and replays them from approved snapshots. It combines the benefits of approval testing with function mocking.

## The Concept

When you "parrot" a function:
1. **Recording Mode**: The real function executes and its inputs/outputs are recorded
2. **Replay Mode**: The function returns previously approved outputs without executing

This is useful for:
- Testing code that depends on external services (APIs, LLMs, databases)
- Creating deterministic tests from non-deterministic functions
- Speeding up tests by avoiding expensive operations

## Example Usage

```python
from verify_parrot import parrot
from approvaltests import verify

def expensive_api_call(prompt):
    # Imagine this calls an external API
    return "API response for: " + prompt

def test_with_parrot():
    with parrot(expensive_api_call):
        result = expensive_api_call("Hello")
        verify(result)
```

First run: The real `expensive_api_call` executes and records the interaction.
Subsequent runs: The parrot replays the approved response instantly.

## Creating Your Own Parrot

```python
from verify_parrot import parrot
import json

def my_external_service(data):
    # Your actual implementation
    return {"processed": data}

# Use it in tests
with parrot(my_external_service):
    result = my_external_service("test data")
    assert result == {"processed": "test data"}
```

The parrot automatically:
- Captures function arguments and return values
- Stores them in approval files
- Replays them on future test runs
- Fails if inputs change unexpectedly

## Benefits

- **Deterministic**: Non-deterministic functions become predictable
- **Fast**: Expensive operations only run once
- **Transparent**: See exactly what was called and returned
- **Version controlled**: Changes to function behavior are tracked in git