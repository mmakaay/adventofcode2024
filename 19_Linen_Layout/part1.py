#!/usr/bin/env python3

import sys
from functools import cache


def load_scenario():
    patterns = tuple(p.strip() for p in next(sys.stdin).split(","))
    assert next(sys.stdin).strip() == ""
    designs = list(map(str.strip, sys.stdin))
    max_pattern_length = max(len(p) for p in patterns)
    return patterns, max_pattern_length, designs


def count_feasible_designs(scenario):
    @cache
    def can_create_design(design):
        if design == "":
            return True
        for i in range(1, min(max_pattern_length, len(design)) + 1):
            chunk = design[:i]
            remainder = design[i:]
            if chunk in patterns and can_create_design(remainder):
                return True
        return False

    patterns, max_pattern_length, designs = scenario
    return sum(can_create_design(design) for design in designs)


scenario = load_scenario()
feasible_designs = count_feasible_designs(scenario)

print("Number of feasible designs:", feasible_designs)
