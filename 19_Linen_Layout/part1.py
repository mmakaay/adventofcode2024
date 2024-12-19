#!/usr/bin/env python3

import sys
from functools import cache


def load_scenario():
    patterns = tuple(p.strip() for p in next(sys.stdin).split(","))
    assert next(sys.stdin).strip() == ""
    designs = list(map(str.strip, sys.stdin))
    return patterns, designs


def count_possible_designs(scenario):
    patterns, designs = scenario
    possible_count = 0
    for design in designs:
        if can_create_design(patterns, design):
            possible_count += 1
    return possible_count


@cache
def can_create_design(patterns, design):
    if design == "":
        return True
    for pattern in patterns:
        if design.startswith(pattern):
            rest = design[len(pattern) :]
            if can_create_design(patterns, rest):
                return True
    return False


scenario = load_scenario()
possible_count = count_possible_designs(scenario)

print("Number of possible designs:", possible_count)
