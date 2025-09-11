from prompt_claude_code import prompt_claude_code
from verify_parrot import verify_parrot


def test_prompt_claude_code():
    verify_parrot(prompt_claude_code, [
        ["What is 2+2?"],
        ["What is the capital of France?"],
        ["Write a haiku about Python"]
    ])