#!/usr/bin/env python3
import subprocess
import sys


def main():
    """Run all checks: lint, typecheck, and test"""
    results = []
    
    print("Running lint...")
    results.append(subprocess.run(["uv", "run", "ruff", "check", "."]).returncode)
    
    print("\nRunning typecheck...")
    results.append(subprocess.run(["uv", "run", "mypy", ".", "--exclude", "__pycache__"]).returncode)
    
    print("\nRunning tests...")
    results.append(subprocess.run(["uv", "run", "pytest"]).returncode)
    
    sys.exit(1 if any(results) else 0)


if __name__ == "__main__":
    main()