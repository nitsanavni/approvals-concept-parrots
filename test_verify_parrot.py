#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pytest", "approvaltests"]
# ///

from verify_parrot import verify_parrot
from math_operations import add, multiply, divide


def test_verify_parrot_with_add():
    verify_parrot(add, [[1, 2], [3, 4], [10, -5]])


def test_verify_parrot_with_multiply():
    verify_parrot(multiply, [[2, 3], [0, 5], [-2, -3]])


def test_verify_parrot_with_exceptions():
    verify_parrot(divide, [[10, 2], [8, 0], [15, 3]])


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])