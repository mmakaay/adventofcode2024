#!/usr/bin/env python3

import sys
from collections import Counter


def load_arragement():
    return Counter(next(sys.stdin).strip().split())


def blink(times, arrangement):
    for _ in range(times):
        arrangement = blink_once(arrangement)
    return arrangement


def blink_once(arrangement):
    new_arrangement = Counter()
    for n, c in arrangement.items():
        if n == "0":
            new_arrangement["1"] += c
        elif len(n) % 2 == 0:
            middle = len(n) // 2
            left, right = n[:middle], str(int(n[middle:]))
            new_arrangement[left] += c
            new_arrangement[right] += c
        else:
            n = str(int(n) * 2024)
            new_arrangement[n] += c

    return new_arrangement


arrangement = load_arragement()
arrangement = blink(75, arrangement)
print("Number of stones:", arrangement.total())
