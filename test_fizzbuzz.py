#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pytest", "approvaltests"]
# ///

from approvaltests import verify
from fizzbuzz import fizzbuzz


def test_fizzbuzz():
    result = fizzbuzz(15)
    verify("\n".join(result))


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])