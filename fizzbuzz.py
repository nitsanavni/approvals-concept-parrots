#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///


def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
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
