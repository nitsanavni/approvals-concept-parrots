from verify_parrot import verify_parrot
from eval_claude_code import generate_claude_code


def test_generate_claude_code():
    verify_parrot(
        generate_claude_code,
        [
            ["Write a function that returns the string 'Hello, World!'"],
            ["Create a simple calculator that adds two numbers: 5 + 3"],
            ["Generate a list comprehension that squares numbers from 1 to 5"],
        ],
    )
