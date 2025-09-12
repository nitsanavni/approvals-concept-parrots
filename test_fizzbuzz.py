from approvaltests import verify, Options
from approvaltests.inline.inline_options import InlineOptions
from fizzbuzz import fizzbuzz_for, is_divisible_by
from parrot import parrot


def test_fizzbuzz_for():
    """
    3 -> Fizz
    4 -> 4
    5 -> Buzz
    7 -> 7
    9 -> Fizz
    15 -> FizzBuzz
    """
    with parrot(is_divisible_by):
        numbers = [3, 4, 5, 7, 9, 15]
        results = [f"{n} -> {fizzbuzz_for(n)}" for n in numbers]
        verify("\n".join(results), options=Options().inline(InlineOptions.automatic()))
