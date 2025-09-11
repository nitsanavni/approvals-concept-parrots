import subprocess
from filecache import filecache


@filecache
def prompt_claude_code(prompt: str) -> str:
    """
    Call Claude Code via bunx with the given prompt.

    Args:
        prompt: The prompt to send to Claude Code

    Returns:
        The output from Claude Code as a string
    """
    cmd = ["bunx", "--bun", "claude", "--dangerously-skip-permissions", "-p", prompt]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    return result.stdout
