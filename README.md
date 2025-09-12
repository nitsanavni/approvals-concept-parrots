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
from parrot import parrot, verify_parrot

# The function we want to test
def is_divisible_by(n, divisor):
    return n % divisor == 0

# Create a parrot by approval-testing the function
def test_is_divisible_by():
    verify_parrot(is_divisible_by, [
        [3, 3], [3, 5],
        [5, 3], [5, 5],
        [7, 3], [7, 5],
        [9, 3], [9, 5],
        [15, 3], [15, 5]
    ])

# Now use the parrot as a test double for testing fizzbuzz_for
def fizzbuzz_for(n):
    if is_divisible_by(n, 3) and is_divisible_by(n, 5):
        return "FizzBuzz"
    elif is_divisible_by(n, 3):
        return "Fizz"
    elif is_divisible_by(n, 5):
        return "Buzz"
    else:
        return str(n)

def test_fizzbuzz_for():
    with parrot(is_divisible_by):  # Uses approved results as test double
        numbers = [3, 5, 7, 9, 15]
        results = [f"{n} -> {fizzbuzz_for(n)}" for n in numbers]
        verify("\n".join(results))
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