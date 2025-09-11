#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///


def add(a: float, b: float) -> float:
    return a + b


def multiply(x: float, y: float) -> float:
    return x * y


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b