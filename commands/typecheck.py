#!/usr/bin/env python3
import subprocess
import sys


def main():
    """Run mypy type checker"""
    result = subprocess.run(["uv", "run", "mypy", ".", "--exclude", "__pycache__"])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()