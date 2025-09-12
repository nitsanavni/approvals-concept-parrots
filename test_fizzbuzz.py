#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pytest", "approvaltests"]
# ///

from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions
from fizzbuzz import fizzbuzz_for, is_divisible_by
from parrot import parrot, verify_parrot


def test_is_divisible_by():
    verify_parrot(is_divisible_by, [
        [3, 3], [3, 5],
        [5, 3], [5, 5],
        [7, 3], [7, 5],
        [9, 3], [9, 5],
        [15, 3], [15, 5]
    ])


def test_fizzbuzz_for():
    """
    3 -> Fizz
    5 -> Buzz
    7 -> 7
    9 -> Fizz
    15 -> FizzBuzz
    """
    with parrot(is_divisible_by):
        numbers = [3, 5, 7, 9, 15]
        results = [f"{n} -> {fizzbuzz_for(n)}" for n in numbers]
        verify("\n".join(results), options=Options().inline(InlineOptions.automatic()))


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])