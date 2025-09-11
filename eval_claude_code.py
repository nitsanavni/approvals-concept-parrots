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

Important: Return ONLY executable Python code, nothing else."""


def eval_claude_code(intention_prompt: str) -> str:
    """
    Prompt Claude to generate Python code for the given intention and evaluate it.
    
    Args:
        intention_prompt: Description of what the Python code should do
        
    Returns:
        String containing both the generated code and its execution result
    """
    # Get code from Claude
    code_prompt = create_code_only_prompt(intention_prompt)
    code = prompt_claude_code(code_prompt).strip()
    
    # Remove any markdown code blocks if they somehow appear
    if code.startswith("```"):
        lines = code.split("\n")
        # Find start and end of code block
        code_lines = []
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
    
    # Execute the code and capture result
    try:
        # Create a namespace for execution
        namespace = {}
        exec(code, namespace)
        
        # Try to get a meaningful result
        # Check if there's a main function or last expression
        result = None
        if 'main' in namespace and callable(namespace['main']):
            result = namespace['main']()
        elif 'result' in namespace:
            result = namespace['result']
        else:
            # Try to evaluate the last line as an expression if possible
            lines = code.strip().split('\n')
            if lines:
                last_line = lines[-1].strip()
                try:
                    result = eval(last_line, namespace)
                except:
                    # Last line wasn't an expression
                    pass
        
        result_str = f"Code:\n{code}\n\nResult: {result}"
    except Exception as e:
        result_str = f"Code:\n{code}\n\nError: {e}"
    
    return result_str