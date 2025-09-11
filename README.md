# Approvals Concept: Parrots

**A parrot is an approved test double** that records function calls and replays them from approved snapshots. It combines the benefits of approval testing with function mocking.

## The Concept

When you "parrot" a function:
1. **Recording Mode**: The real function executes and its inputs/outputs are recorded
2. **Replay Mode**: The function returns previously approved outputs without executing

You can approval-test a function AND then reuse those approved results as a test double when testing its collaborators. This gives you:
- Approval testing for the function itself
- A verified and approved test double for testing code that depends on it
- One source of truth for both the function's behavior and its test double

## Example

```python
from verify_parrot import parrot, verify_parrot

# The function we want to test
def translate_to_spanish(text):
    # Complex translation logic
    return f"Spanish: {text}"

# Create a parrot by approval-testing the function
def test_translate():
    verify_parrot(translate_to_spanish, ["Hello"])
    verify_parrot(translate_to_spanish, ["Goodbye"])

# Now use the parrot as a test double for collaborators
def greeting_service(name):
    translation = translate_to_spanish(f"Hello {name}")
    return f"Greeting: {translation}"

def test_greeting_service():
    with parrot(translate_to_spanish):  # Uses approved results as test double
        result = greeting_service("Alice")
        assert result == "Greeting: Spanish: Hello Alice"
```

The workflow:
1. **Create the parrot**: Use `verify_parrot(fn, args)` to approval-test the function
2. **Use the parrot**: Use `with parrot(fn):` to replay approved results as a test double

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