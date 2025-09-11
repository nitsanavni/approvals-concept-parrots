from approvaltests import verify
from eval_claude_code import eval_claude_code
from verify_parrot import parrot
from prompt_claude_code import prompt_claude_code


def test_eval_claude_code_hello_world():
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code(
                "Write a function that returns the string 'Hello, World!' and call it"
            )
        )


def test_eval_claude_code_calculator():
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code("Create a simple calculator that adds two numbers: 5 + 3")
        )


def test_eval_claude_code_list_comprehension():
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code(
                "Generate a list comprehension that squares numbers from 1 to 5"
            )
        )


def test_eval_claude_code_fibonacci():
    with parrot(prompt_claude_code):
        verify(eval_claude_code("Print the first 10 Fibonacci numbers"))


def test_eval_claude_code_dictionary():
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code(
                "Create a dictionary with keys 'a', 'b', 'c' and values 1, 2, 3, then print it"
            )
        )


def test_eval_claude_code_factorial():
    with parrot(prompt_claude_code):
        verify(eval_claude_code("Calculate the factorial of 5"))
