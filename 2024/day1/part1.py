#!/usr/bin/env python3

import sys

lefts, rights = [], []
for line in sys.stdin:
    [left, right] = map(int, line.split())
    lefts.append(left) 
    rights.append(right) 

joined = zip(sorted(lefts), sorted(rights))
diffs = (abs(a - b) for a, b in joined)
summed_diffs = sum(diffs)

print("Solution:", summed_diffs)
