#!/usr/bin/env python3

import sys


def random_number_generator(s):
    while True:
        s ^= (s << 6) & 0xFFFFFF
        s ^= (s >> 5) & 0xFFFFFF
        s ^= (s << 11) & 0xFFFFFF
        yield s


total = 0
secrets = map(int, sys.stdin)
for secret in secrets:
    rng = random_number_generator(secret)
    for _ in range(2000):
        number = next(rng)
    total += number

print("Total:", total)
