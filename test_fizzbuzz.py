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
        [1, 3], [1, 5],
        [2, 3], [2, 5],
        [3, 3], [3, 5],
        [4, 3], [4, 5],
        [5, 3], [5, 5],
        [6, 3], [6, 5],
        [7, 3], [7, 5],
        [8, 3], [8, 5],
        [9, 3], [9, 5],
        [10, 3], [10, 5],
        [11, 3], [11, 5],
        [12, 3], [12, 5],
        [13, 3], [13, 5],
        [14, 3], [14, 5],
        [15, 3], [15, 5]
    ])


def test_fizzbuzz_for():
    with parrot(is_divisible_by):
        assert fizzbuzz_for(1) == "1"
        assert fizzbuzz_for(2) == "2"
        assert fizzbuzz_for(3) == "Fizz"
        assert fizzbuzz_for(4) == "4"
        assert fizzbuzz_for(5) == "Buzz"
        assert fizzbuzz_for(6) == "Fizz"
        assert fizzbuzz_for(7) == "7"
        assert fizzbuzz_for(8) == "8"
        assert fizzbuzz_for(9) == "Fizz"
        assert fizzbuzz_for(10) == "Buzz"
        assert fizzbuzz_for(11) == "11"
        assert fizzbuzz_for(12) == "Fizz"
        assert fizzbuzz_for(13) == "13"
        assert fizzbuzz_for(14) == "14"
        assert fizzbuzz_for(15) == "FizzBuzz"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])