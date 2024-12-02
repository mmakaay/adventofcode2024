#!/usr/bin/env python3

import sys

SAFE_STEP_SIZES = [1, 2, 3]

def evaluate_reports():
    for report in sys.stdin:
        yield from evaluate_report(report)


def evaluate_report(report):
    values = list(map(int, report.split()))
    yield (
        assess_for_safety(values, +1, True) or
        assess_for_safety(values, -1, True) or
        assess_for_safety(values[1:], +1, False) or
        assess_for_safety(values[1:], -1, False)
    )


def assess_for_safety(values, direction, apply_safety_once):
    previous_value = values[0]
    for value in values[1:]:
        step_size = value - previous_value
        if step_size * direction in SAFE_STEP_SIZES:
            previous_value = value
        elif apply_safety_once:
            apply_safety_once = False
        else:
            return False
    return True


safe_count = sum(is_safe for is_safe in evaluate_reports())
print(f"Number of safe reports: {safe_count}")

