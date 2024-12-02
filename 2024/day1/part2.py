#!/usr/bin/env python3

import sys
from collections import Counter

lefts, rights = Counter(), Counter()
for line in sys.stdin:
    [left, right] = map(int, line.split())
    lefts.update([left])
    rights.update([right])

similarity_scores = (
    left_count * left * rights.get(left, 0)
    for left, left_count in lefts.items()
)
summed_similary_scores = sum(similarity_scores)

print("Solution:", summed_similary_scores)
