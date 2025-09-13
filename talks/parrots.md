---
theme: default
highlighter: shiki
lineNumbers: false
info: |
  ## Parrots: Approved Test Doubles
  
  A lightning talk about combining approval testing with test doubles
drawings:
  persist: false
title: Parrots - Approved Test Doubles
---

# Parrots 🦜

## Approved Test Doubles

A lightning talk about combining<br/>approval testing with test doubles

---

# The Problem

Testing functions that depend on other functions

```python
def fizzbuzz_for(n):
    if is_divisible_by(n, 3) and is_divisible_by(n, 5):
        return "FizzBuzz"
    elif is_divisible_by(n, 3):
        return "Fizz"
    elif is_divisible_by(n, 5):
        return "Buzz"
    else:
        return str(n)
```

How do we test `fizzbuzz_for` in isolation?

---

# Traditional Approach: Mocking

```python
def test_fizzbuzz_for():
    with patch('is_divisible_by') as mock:
        mock.side_effect = [True, True]  # divisible by 3 and 5
        assert fizzbuzz_for(15) == "FizzBuzz"
```

**Problems:**
- Mock behavior might not match reality
- Mocks are disconnected from actual function tests
- Hard to maintain when function behavior changes

---

# The Parrot Concept

**A parrot is an approved test double**

1. **Record**: Test the real function, approve results
2. **Replay**: Use approved results as test double

```python
# Step 1: Create the parrot
def test_is_divisible_by():
    verify_parrot(is_divisible_by, [
        [15, 3], [15, 5],  # Test with real inputs
        [7, 3], [7, 5]
    ])
```

---

# Using the Parrot

```python
# Step 2: Use as test double
def test_fizzbuzz_for():
    with parrot(is_divisible_by):  # Replays approved results
        numbers = [3, 5, 7, 9, 15]
        results = [f"{n} -> {fizzbuzz_for(n)}" for n in numbers]
        verify("\n".join(results))
```

The parrot automatically:
- Returns recorded results for known inputs
- Fails if called with unexpected inputs
- Keeps test doubles in sync with real behavior

---

# Approved Files

Two files are generated:

**Human-readable** (`is_divisible_by.approved.txt`):
```
Function: is_divisible_by
Args: [15, 3] -> Result: True
Args: [15, 5] -> Result: True
Args: [7, 3] -> Result: False
Args: [7, 5] -> Result: False
```

**Machine-readable** (`is_divisible_by.approved.pickle`)

Both are version controlled!

---

# Benefits

✅ **Single Source of Truth**
- Same approved results for testing AND mocking

✅ **Transparent**
- See exactly what was called and returned

✅ **Version Controlled**
- Track behavior changes in git

✅ **Verified Test Doubles**
- Guaranteed to match actual behavior

---

# When to Use Parrots

**Perfect for:**
- Functions with deterministic outputs
- External API responses (record once, replay many)
- Complex calculations
- Database queries

**Not ideal for:**
- Non-deterministic functions (random, time-based)
- Functions with side effects
- Very simple functions

---

# Key Insight

> Your test doubles should be as carefully tested<br/>as your production code

Parrots achieve this by making your<br/>test doubles **BE** your tested code!

---

# Thank You! 🦜

Questions?

<br/>

GitHub: [nitsanavni/approvals-concept-parrots](https://github.com/nitsanavni/approvals-concept-parrots)