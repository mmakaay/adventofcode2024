#!/usr/bin/env python3

import re
import sys
from collections import defaultdict
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


@cache
def find_sequences_for_key_transition(keypad_type, key_a, key_b):
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

    x_start, y_start = find_pos_of(key_a)
    x_finish, y_finish = find_pos_of(key_b)

    dirkeys = {(0, -1): "^", (1, 0): ">", (0, 1): "v", (-1, 0): "<"}

    queue = []
    sequences = []
    costs = defaultdict(lambda: defaultdict(lambda: float("inf")))
    heappush(queue, (0, x_start, y_start, ""))

    while queue:
        cost, x, y, route = heappop(queue)
        if cost > costs[y][x]:
            continue
        costs[y][x] = cost
        if (x, y) == (x_finish, y_finish):
            sequences.append(route)
            continue
        for dx, dy in ((-1, 0), (0, 1), (0, -1), (1, 0)):
            x2, y2 = x + dx, y + dy
            if 0<=x2<w and 0<=y2<h and p[y2][x2] != " ":
                dirkey = dirkeys[(dx, dy)]
                heappush(queue, (cost + 1, x2, y2, route + dirkey))

    return sequences


@cache
def find_controls_for_sequence(keypad_type, sequence):
    key_transition_sequences = []
    for i, (key_a, key_b) in enumerate(zip("A" + sequence, sequence)):
        s = find_sequences_for_key_transition(keypad_type, key_a, key_b)
        key_transition_sequences.append(s)
        key_transition_sequences.append(["A"])
    return ["".join(s) for s in product(*key_transition_sequences)]


@cache
def find_best_controls_for_sequence(keypad_type, sequence):
    best = None
    min_len = float("inf")
    for c1 in find_controls_for_sequence(keypad_type, sequence):
        for c2 in find_controls_for_sequence("directional", c1):
            #for c3 in find_controls_for_sequence("directional", c2):
            m = min(len(x) for x in c2)
            if m < min_len:
                min_len = m
                best = c1
    return best


def find_best_multi_level_control_length_for_sequence(
    sequence, intermediate_robots=0, keypad_type="numeric"
):
    # < 0, because we start out with the numpad,
    # which is not controlling an intermediate robot.
    if intermediate_robots < 0:
        return len(sequence)

    controls = find_best_controls_for_sequence(keypad_type, sequence)
    print(sequence,"->",controls)
    return find_best_multi_level_control_length_for_sequence(
        controls,
        intermediate_robots - 1,
        "directional",
    )


def load_codes():
    return sys.stdin.read().splitlines()


keypads = instantiate_keypads()

print(find_best_multi_level_control_length_for_sequence("01", 25, "numeric"))

#total = 0
#for sequence in load_codes():
#    sequence_length = find_best_controlling_sequence_length(
#        sequence,
#        intermediate_robots=25
#    )
#    score = int(sequence[:-1]) * sequence_length
#    total += score

##print("Total:", total)
