import pytest
from parrot import register_missing_args_hook


def hello_hook(function_name: str, file_path: str, args, cache_data: dict) -> None:
    """A friendly hook that prints info when uncached arguments are encountered."""
    print(f"\n🦜 Hello! Parrot encountered uncached arguments:")
    print(f"   Function: {function_name}")
    print(f"   File: {file_path}")
    print(f"   Arguments: {args}")
    print(f"   Cached args count: {len(cache_data.get('results', []))}")
    print("   Consider running verify_parrot with these arguments to cache them!\n")


# Register the hello hook when pytest starts
def pytest_configure(config):
    register_missing_args_hook(hello_hook)