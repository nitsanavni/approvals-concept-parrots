import re
from pathlib import Path
from parrot import register_missing_args_hook


def hello_hook(function_name: str, file_path: str, args, cache_data: dict) -> None:
    """A friendly hook that prints info when uncached arguments are encountered."""
    print("\n🦜 Hello! Parrot encountered uncached arguments:")
    print(f"   Function: {function_name}")
    print(f"   File: {file_path}")
    print(f"   Arguments: {args}")
    print(f"   Cached args count: {len(cache_data.get('results', []))}")
    
    # Search for verify_parrot calls for this function in the codebase
    # Pattern looks for verify_parrot( followed by optional whitespace, then the function name
    pattern = rf"verify_parrot\s*\(\s*{re.escape(function_name)}"
    found_matches = []
    
    # Search in Python files in the current directory and subdirectories
    for py_file in Path.cwd().rglob("*.py"):
        try:
            content = py_file.read_text()
            # Search across multiple lines since verify_parrot can be multiline
            if re.search(pattern, content, re.MULTILINE | re.DOTALL):
                # Find the line numbers
                for i, line in enumerate(content.splitlines(), 1):
                    if re.search(r"verify_parrot\s*\(", line):
                        # Check if this is the right verify_parrot by looking ahead
                        lines_ahead = content.splitlines()[i-1:i+3]
                        block = "\n".join(lines_ahead)
                        if re.search(pattern, block):
                            found_matches.append(f"{py_file}:{i}")
                            break
        except Exception:
            pass  # Skip files we can't read
    
    if found_matches:
        print(f"\n   Found verify_parrot({function_name}) in:")
        for match in found_matches:
            print(f"     - {match}")
        print("\n   You can add the new arguments to the existing verify_parrot call!")
    else:
        print(f"\n   No verify_parrot({function_name}) found in codebase.")
        print("   Consider creating a test with verify_parrot to cache these arguments!")
    print()


# Register the hello hook when pytest starts
def pytest_configure(config):
    register_missing_args_hook(hello_hook)