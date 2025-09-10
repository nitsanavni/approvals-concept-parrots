#!/usr/bin/env python3
import subprocess
import sys


def main():
    """Run pytest"""
    result = subprocess.run(["uv", "run", "pytest"])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()