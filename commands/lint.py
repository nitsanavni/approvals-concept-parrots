#!/usr/bin/env python3
import subprocess
import sys


def main():
    """Run ruff linter"""
    result = subprocess.run(["uv", "run", "ruff", "check", "."])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()