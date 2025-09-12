from approvaltests import verify
from prompt_claude_code import prompt_claude_code
from eval_claude_code import create_code_only_prompt, eval_claude_code
from parrot import verify_parrot, parrot


def test_prompt_claude_code():
    verify_parrot(
        prompt_claude_code,
        [
            ["What is 2+2?"],
            ["What is the capital of France?"],
            ["Write a haiku about Python"],
            [
                create_code_only_prompt(
                    "Calculate the sum of 2 and 2 and print the result"
                )
            ],
            [
                create_code_only_prompt(
                    "Generate a list of the first 5 prime numbers and print it"
                )
            ],
            [
                create_code_only_prompt(
                    "Create a function that reverses a string and call it with 'hello' and print the result"
                )
            ],
        ],
    )


def test_eval_claude_code():
    with parrot(prompt_claude_code):
        verify(eval_claude_code("Generate a list of the first 5 prime numbers"))
