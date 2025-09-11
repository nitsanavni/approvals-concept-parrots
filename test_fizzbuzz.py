#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pytest", "approvaltests"]
# ///

from approvaltests import verify
from fizzbuzz import fizzbuzz_for, is_divisible_by
from verify_parrot import parrot, verify_parrot


def test_is_divisible_by():
    verify_parrot(is_divisible_by, [
        [3, 3], [3, 5],
        [5, 3], [5, 5],
        [7, 3], [7, 5],
        [9, 3], [9, 5],
        [15, 3], [15, 5]
    ])


def test_fizzbuzz_for():
    with parrot(is_divisible_by):
        assert fizzbuzz_for(3) == "Fizz"
        assert fizzbuzz_for(5) == "Buzz"
        assert fizzbuzz_for(7) == "7"
        assert fizzbuzz_for(9) == "Fizz"
        assert fizzbuzz_for(15) == "FizzBuzz"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])