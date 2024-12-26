#!/usr/bin/env python3

import sys
from collections import defaultdict, deque
from itertools import pairwise


def random_number_generator(s):
    while True:
        s = s ^ (s << 6) & 0xFFFFFF
        s = s ^ (s >> 5) & 0xFFFFFF
        s = s ^ (s << 11) & 0xFFFFFF
        yield s


seller_secrets = map(int, sys.stdin.read().splitlines())

# Sums the yields for all possible sequences for all sellers.
yield_per_sequence = defaultdict(int)

# For each seller, find the all possible yields and record
# the sequences leading up to them in the above dict.
for secret in seller_secrets:
    rng = random_number_generator(secret)

    # The first offer counts, so keep track of seen sequences.
    seen_diffs = set()

    # Used to look at groups of 5 diffs in a sequence. With 5
    # diffs, we get 4 diffs, which is what is needed as input
    # for the translation monkey.
    sliding_view = deque([secret])

    # Get cracking!
    for _ in range(2000):
        # Extend sliding view with next secret.
        secret = next(rng)
        sliding_view.append(secret)

        # Skip processing when we don't have 5 secrets. This will
        # take care of buffering 5 secrets at the start, and draining
        # 5 secrets at the end of the 2000 iterations.
        if len(sliding_view) < 5:
            continue

        # Process and register the yield and its leading sequence.
        yields = tuple(s % 10 for s in sliding_view)
        diffs = tuple(b - a for a, b in pairwise(yields))
        if diffs not in seen_diffs:
            seen_diffs.add(diffs)
            yield_per_sequence[diffs] += yields[-1]

        # This is a sliding view, we can drop the leftmost yield.
        sliding_view.popleft()

best_sequence = max(yield_per_sequence, key=yield_per_sequence.get)
print("Highest yield:", best_sequence, "->", yield_per_sequence[best_sequence])
