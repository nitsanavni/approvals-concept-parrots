import re
from pathlib import Path
from parrot import register_missing_args_hook
import pytest
from approvaltests import set_default_reporter
from approvaltests.reporters import PythonNativeReporter


@pytest.fixture(scope="session", autouse=True)
def configure_approvaltests_reporter():
    set_default_reporter(PythonNativeReporter())


def hello_hook(function_name: str, file_path: str, args, cache_data: dict) -> None:
    """A friendly hook that prints info when uncached arguments are encountered or no cache exists."""
    if args is None:
        # No cache file exists at all
        print("\n🦜 Hello! Parrot found no cache file for this function:")
        print(f"   Function: {function_name}")
        print(f"   File: {file_path}")
    else:
        # Cache exists but these specific arguments aren't cached
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
        print("   Creating a new test file with verify_parrot...")
        
        # Get the module name from the file path
        module_path = Path(file_path)
        module_name = module_path.stem
        
        # Determine the import path for the function
        # Assuming the file is in the current directory or a subdirectory
        relative_path = module_path.relative_to(Path.cwd())
        import_path = str(relative_path.with_suffix("")).replace("/", ".")
        
        # Create test file name
        test_file_name = f"test_{module_name}_generated.py"
        test_file_path = Path.cwd() / test_file_name
        
        # Create the test file content
        if args is None:
            # No cache exists - create empty verify_parrot
            test_content = f'''"""Auto-generated test file for {function_name}"""
from parrot import verify_parrot
from {import_path} import {function_name}


def test_{function_name}():
    """Test for {function_name} - add your test arguments here."""
    verify_parrot(
        {function_name},
        [
            # Add your test cases here, e.g.:
            # [arg1, arg2],
        ],
    )
'''
        else:
            # Cache exists but args missing - create with the missing args
            test_content = f'''"""Auto-generated test file for {function_name}"""
from parrot import verify_parrot
from {import_path} import {function_name}


def test_{function_name}():
    """Test for {function_name} with auto-captured arguments."""
    verify_parrot(
        {function_name},
        [
            {list(args)},
        ],
    )
'''
        
        # Write the test file
        test_file_path.write_text(test_content)
        print(f"   Created test file: {test_file_path}")
        print(f"   💡 Consider renaming this file to something more descriptive!")
        print(f"   Run 'pytest {test_file_name}::test_{function_name}' to capture the result!")
    print()


# Register the hello hook when pytest starts
def pytest_configure(config):
    register_missing_args_hook(hello_hook)