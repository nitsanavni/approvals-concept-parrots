# Approvals Concept: Parrots

**A parrot is an approved test double** that records function calls and replays them from approved snapshots. It combines the benefits of approval testing with function mocking.

## The Concept

When you "parrot" a function:
1. **Recording Mode**: The real function executes and its inputs/outputs are recorded
2. **Replay Mode**: The function returns previously approved outputs without executing

The key insight: You can approval-test a function AND then reuse those approved results as a test double when testing its collaborators. This gives you:
- Approval testing for the function itself
- A verified test double for testing code that depends on it
- One source of truth for both the function's behavior and its test double

## Example Usage

```python
from verify_parrot import parrot
from approvaltests import verify

# The function we want to test
def translate_to_spanish(text):
    # Complex translation logic
    return f"Spanish: {text}"

# Test the function itself with approval testing
def test_translate():
    with parrot(translate_to_spanish):
        result = translate_to_spanish("Hello")
        verify(result)  # Approves: "Spanish: Hello"

# Now test a collaborator that uses translate_to_spanish
def greeting_service(name):
    translation = translate_to_spanish(f"Hello {name}")
    return f"Greeting: {translation}"

def test_greeting_service():
    with parrot(translate_to_spanish):  # Reuse approved results as test double
        result = greeting_service("Alice")
        assert result == "Greeting: Spanish: Hello Alice"
```

The parrot serves dual purpose:
1. First test: Approval-tests `translate_to_spanish` 
2. Second test: Uses approved results as a test double for `greeting_service`

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

- **Single Source of Truth**: The same approved results serve both as test verification and test doubles
- **Transparent**: See exactly what was called and returned in approval files
- **Version Controlled**: Changes to function behavior are tracked in git
- **Verified Test Doubles**: Your test doubles are guaranteed to match the actual function's behavior