#!/usr/bin/env python3
import subprocess
import sys


def main():
    """Run pyright type checker with strict mode"""
    result = subprocess.run(["uv", "run", "pyright", "."])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()