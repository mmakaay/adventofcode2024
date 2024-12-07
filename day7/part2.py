#!/usr/bin/env python3

import sys


def read_equations():
    for line in sys.stdin:
        [test_value, numbers] = line.split(":")
        yield int(test_value), list(map(int, numbers.split()))


def is_possible_equation(test_value, numbers):
    for result in recurse_equation(numbers[0], numbers[1:]):
        if result == test_value:
            return True
    return False


def recurse_equation(total, numbers):
    if not numbers:
        yield total
        return

    next_number = numbers[0]
    remaining = numbers[1:]
    yield from recurse_equation(total * next_number, remaining)
    yield from recurse_equation(total + next_number, remaining)
    yield from recurse_equation(int(f"{total}{next_number}"), remaining)


total = 0
for test_value, numbers in read_equations():
    if is_possible_equation(test_value, numbers):
        total += test_value

print("Calibration value:", total)
