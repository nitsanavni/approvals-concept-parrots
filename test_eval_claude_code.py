from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions
from eval_claude_code import eval_claude_code
from verify_parrot import parrot
from prompt_claude_code import prompt_claude_code


def test_eval_claude_code_hello_world():
    """
    Code:
    def hello_world():
        return 'Hello, World!'
    
    print(hello_world())
    
    Result: Hello, World!
    """
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code(
                "Write a function that returns the string 'Hello, World!' and call it"
            ),
            options=Options().inline(InlineOptions.automatic())
        )


def test_eval_claude_code_calculator():
    """
    Code:
    print(5 + 3)
    
    Result: 8
    """
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code("Create a simple calculator that adds two numbers: 5 + 3"),
            options=Options().inline(InlineOptions.automatic())
        )


def test_eval_claude_code_list_comprehension():
    """
    Code:
    print([x**2 for x in range(1, 6)])
    
    Result: [1, 4, 9, 16, 25]
    """
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code(
                "Generate a list comprehension that squares numbers from 1 to 5"
            ),
            options=Options().inline(InlineOptions.automatic())
        )


def test_eval_claude_code_fibonacci():
    """
    Code:
    a, b = 0, 1
    for _ in range(10):
        print(a)
        a, b = b, a + b
    
    Result: 0
    1
    1
    2
    3
    5
    8
    13
    21
    34
    """
    with parrot(prompt_claude_code):
        verify(eval_claude_code("Print the first 10 Fibonacci numbers"), options=Options().inline(InlineOptions.automatic()))


def test_eval_claude_code_dictionary():
    """
    Code:
    dictionary = {'a': 1, 'b': 2, 'c': 3}
    print(dictionary)
    
    Result: {'a': 1, 'b': 2, 'c': 3}
    """
    with parrot(prompt_claude_code):
        verify(
            eval_claude_code(
                "Create a dictionary with keys 'a', 'b', 'c' and values 1, 2, 3, then print it"
            ),
            options=Options().inline(InlineOptions.automatic())
        )


def test_eval_claude_code_factorial():
    """
    Code:
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    print(factorial(5))
    
    Result: 120
    """
    with parrot(prompt_claude_code):
        verify(eval_claude_code("Calculate the factorial of 5"), options=Options().inline(InlineOptions.automatic()))
