#!/usr/bin/env python3

import sys


def load_keys_and_locks():
    keys = []
    locks = []
    blocks = map(str.strip, sys.stdin.read().split("\n\n"))
    for block in blocks:
        lines = block.splitlines()
        first_line = lines[0]
        data = []
        for data_line in lines[1:-1]:
            data.append([c == "#" for c in data_line])
        heights = [sum(v) for v in list(zip(*data))]

        if "#" in first_line:
            locks.append(heights)
        elif "." in first_line:
            keys.append(heights)

    return keys, locks


def try_keys_with_locks(keys, locks):
    for key in keys:
        for lock in locks:
            does_fit = all(l + k <= 5 for l, k in zip(lock, key))
            if does_fit:
                yield key, lock


keys, locks = load_keys_and_locks()
fitting_pairs = sum(True for _ in try_keys_with_locks(keys, locks))

print("Fitting pairs:", fitting_pairs)
