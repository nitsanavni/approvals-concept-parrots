import subprocess

from prompt_claude_code import prompt_claude_code


def create_code_only_prompt(intention_prompt: str) -> str:
    """
    Create a prompt that instructs Claude to return only valid Python code.

    Args:
        intention_prompt: Description of what the Python code should do

    Returns:
        Formatted prompt string for Claude
    """
    return f"""Return ONLY valid Python code with no explanations, no markdown, no decorations.
Just the raw Python code that accomplishes this:
{intention_prompt}

The code will be executed, so use print for key outputs.
Important: Return ONLY executable Python code, nothing else."""


def generate_claude_code(intention_prompt: str) -> str:
    """
    Generate Python code from Claude based on the given intention.

    Args:
        intention_prompt: Description of what the Python code should do

    Returns:
        Generated Python code as a string
    """
    # Get code from Claude
    code_prompt = create_code_only_prompt(intention_prompt)
    code = prompt_claude_code(code_prompt).strip()
    return code


def eval_claude_code(intention_prompt: str) -> str:
    """
    Prompt Claude to generate Python code for the given intention and evaluate it.

    Args:
        intention_prompt: Description of what the Python code should do

    Returns:
        String containing both the generated code and its execution result
    """
    code = generate_claude_code(intention_prompt)

    # Remove any markdown code blocks if they somehow appear
    if code.startswith("```"):
        lines = code.split("\n")
        # Find start and end of code block
        code_lines: list[str] = []
        in_block = False
        for line in lines:
            if line.startswith("```") and not in_block:
                in_block = True
                continue
            elif line.startswith("```") and in_block:
                break
            elif in_block:
                code_lines.append(line)
        code = "\n".join(code_lines)

    # Execute the code using subprocess
    try:
        result = subprocess.run(
            ["uv", "run", "python", "-c", code],
            capture_output=True,
            text=True,
            check=True,
        )
        result_str = f"Code:\n{code}\n\nResult: {result.stdout.strip() if result.stdout else 'None'}"
    except subprocess.CalledProcessError as e:
        result_str = f"Code:\n{code}\n\nError: {e.stderr if e.stderr else str(e)}"
    except Exception as e:
        result_str = f"Code:\n{code}\n\nError: {e}"

    return result_str
