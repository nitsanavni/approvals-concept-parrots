#!/usr/bin/env python3
import subprocess
import sys

def lint():
    """Run ruff linter"""
    return subprocess.run(["ruff", "check", "."]).returncode

def typecheck():
    """Run mypy type checker"""
    return subprocess.run(["mypy", ".", "--exclude", "__pycache__"]).returncode

def typecheck_strict():
    """Run pyright type checker with strict mode"""
    return subprocess.run(["pyright", "."]).returncode

def test():
    """Run pytest"""
    return subprocess.run(["pytest"]).returncode

def check():
    """Run all checks: lint, typecheck, and test"""
    results = []
    print("Running lint...")
    results.append(lint())
    print("\nRunning typecheck...")
    results.append(typecheck())
    print("\nRunning tests...")
    results.append(test())
    return 1 if any(results) else 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "lint":
            sys.exit(lint())
        elif command == "typecheck":
            sys.exit(typecheck())
        elif command == "typecheck-strict":
            sys.exit(typecheck_strict())
        elif command == "test":
            sys.exit(test())
        elif command == "check":
            sys.exit(check())
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    else:
        print("Usage: python scripts.py [lint|typecheck|typecheck-strict|test|check]")
        sys.exit(1)