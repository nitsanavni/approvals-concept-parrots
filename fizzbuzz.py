#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///


def is_divisible_by(n: int, divisor: int) -> bool:
    return n % divisor == 0


def fizzbuzz(n: int) -> list[str]:
    result: list[str] = []
    for i in range(1, n + 1):
        if is_divisible_by(i, 3) and is_divisible_by(i, 5):
            result.append("FizzBuzz")
        elif is_divisible_by(i, 3):
            result.append("Fizz")
        elif is_divisible_by(i, 5):
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


if __name__ == "__main__":
    import sys

    n = 15
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            print(f"Error: '{sys.argv[1]}' is not a valid number")
            sys.exit(1)

    results = fizzbuzz(n)
    for item in results:
        print(item)
