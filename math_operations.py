#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///


def add(a, b):
    return a + b


def multiply(x, y):
    return x * y


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b