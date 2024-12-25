#!/usr/bin/env python3

import re
import sys
from itertools import product
from heapq import heappush, heappop
from functools import cache


def instantiate_keypads():
    def parse_layout(layout):
        return [
            list(match)
            for line in layout.splitlines()
            for match in re.findall(r"^.* (.) \| (.) \| (.) \|", line)
        ]

    return {
        "numeric": parse_layout("""
            +---+---+---+
            | 7 | 8 | 9 |
            +---+---+---+
            | 4 | 5 | 6 |
            +---+---+---+
            | 1 | 2 | 3 |
            +---+---+---+
                | 0 | A |
                +---+---+
        """),
        "directional": parse_layout("""
                +---+---+
                | ^ | A |
            +---+---+---+
            | < | v | > |
            +---+---+---+
        """),
    }


def find_sequence(keypad_type, key_start, key_finish):
    p = keypads[keypad_type]
    w = len(p[0])
    h = len(p)

    def find_pos_of(search_key):
        return next(
            (x, y)
            for y in range(len(p))
            for x in range(len(p[0]))
            if p[y][x] == search_key
        )

    x_start, y_start = find_pos_of(key_start)
    x_finish, y_finish = find_pos_of(key_finish)

    dirkeys = {(0, -1): "^", (1, 0): ">", (0, 1): "v", (-1, 0): "<"}
    shortest_sequences = []
    queue = []
    heappush(queue, (0, x_start, y_start, ""))
    minimal_length = float("inf")
    while queue:
        length, x, y, route = heappop(queue)
        if length > minimal_length:
            continue
        if (x, y) == (x_finish, y_finish):
            minimal_length = len(route)
            shortest_sequences.append(route + "A")
            continue
        length += 1
        for dx, dy in ((-1, 0), (0, 1), (0, -1), (1, 0)):
            x2, y2 = x + dx, y + dy
            if 0<=x2<w and 0<=y2<h and p[y2][x2] != " ":
                dirkey = dirkeys[(dx, dy)]
                heappush(queue, (length, x2, y2, route + dirkey))

    # See README.md why this scoring function was implemented to find
    # the best sequence amongs a number of sequences.
    def get_sequence_quality(sequence):
        # TODO ^> is actually > at start of string, not what I expected.
        score = -1 * len(re.findall(r"(>v|^>|v<)", sequence))
        score += 2 * sum((a == b) for (a, b) in zip(sequence, sequence[1:]))
        return score

    best = max(shortest_sequences, key=get_sequence_quality)
    return best


@cache
def find_best_controlling_sequence_length(
    sequence: str, intermediate_robots: int = 0, keypad_type="numeric"
):
    # < 0, because we start out with the numpad,
    # which is not controlling an intermediate robot.
    if intermediate_robots < 0:
        return len(sequence)

    keypad = keypads[keypad_type]
    parts = [
        find_best_controlling_sequence_length(
            find_sequence(
                keypad_type, key_start, key_finish
            ),
            intermediate_robots - 1,
            "directional",
        )
        for key_start, key_finish in zip('A' + sequence, sequence)
    ]
    return sum(parts)


def load_codes():
    return sys.stdin.read().splitlines()


total = 0
keypads = instantiate_keypads()
for sequence in load_codes():
    sequence_length = find_best_controlling_sequence_length(
        sequence,
        intermediate_robots=25
    )
    score = int(sequence[:-1]) * sequence_length
    total += score

print("Total:", total)
