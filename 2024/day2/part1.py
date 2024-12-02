#!/usr/bin/env python3

import sys

SAFE_STEP_SIZES = [1, 2, 3]


def assess_for_safety(report):
    values = map(int, report.split())
    direction, previous = 0, next(values)
    for value in values:
        step_size = value - previous
        previous = value
        if not direction:
            direction = +1 if step_size > 0 else -1
        if direction * step_size not in SAFE_STEP_SIZES:
            return False
    return True


def evaluate_reports():
    for report in sys.stdin:
        is_safe = assess_for_safety(report)
        yield is_safe


safe_count = sum(is_safe for is_safe in evaluate_reports())
print(f"Number of safe reports: {safe_count}")
