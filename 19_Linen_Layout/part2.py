#!/usr/bin/env python3

import sys
from functools import cache


def load_scenario():
    patterns = tuple(p.strip() for p in next(sys.stdin).split(","))
    assert next(sys.stdin).strip() == ""
    designs = list(map(str.strip, sys.stdin))
    max_pattern_length = max(len(p) for p in patterns)
    return patterns, max_pattern_length, designs


def count_total_arrangements(scenario):
    @cache
    def count_possible_arrangements(design, count=0):
        if design == "":
            return count + 1
        for i in range(1, min(max_pattern_length, len(design)) + 1):
            chunk = design[:i]
            remainder = design[i:]
            if chunk in patterns:
                count += count_possible_arrangements(remainder)
        return count

    patterns, max_pattern_length, designs = scenario
    return sum(count_possible_arrangements(design) for design in designs)


scenario = load_scenario()
total = count_total_arrangements(scenario)

print("Total of possible arrangements:", total)
