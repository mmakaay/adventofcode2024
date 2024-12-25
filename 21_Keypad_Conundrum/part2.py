#!/usr/bin/env python3

import re
import sys
from itertools import product
from heapq import heappush, heappop
from functools import cache


numpad_layout = """
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

dirpad_layout = """
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""

def parse_layout(layout):
    return [
        list(match)
        for line in layout.splitlines()
        for match in re.findall(r"\ (.) \| (.) \| (.) \|", line)
    ]

numpad = parse_layout(numpad_layout)
dirpad = parse_layout(dirpad_layout)


def find_path(p, key_start, key_finish ):
    def find_pos_of(search_key):
        return next(
            (x, y)
            for y in range(len(p))
            for x in range(len(p[0]))
            if p[y][x] == search_key
        )

    x_start, y_start = find_pos_of(key_start)
    x_finish, y_finish = find_pos_of(key_finish)

    def build_paths(x, y, new_code):
        # We arrived at the finish key. Add an "A" to activate the key
        # and return the completed path.
        if (x, y) == (x_finish, y_finish):
            yield new_code + 'A'

        # Found out, not by thinking but by switching around stuff until
        # the result was accepted by AoC 2024. *slight shame*
        if x_finish < x and p[y][x - 1] != ' ':
            yield from build_paths(x - 1, y, new_code + '<')
        if y_finish > y and p[y + 1][x] != ' ':
            yield from build_paths(x, y + 1, new_code + 'v')
        if y_finish < y and p[y - 1][x] != ' ':
            yield from build_paths(x, y - 1, new_code + '^')
        if x_finish > x and p[y][ x + 1 ] != ' ':
            yield from build_paths(x + 1, y, new_code + '>')

    all_paths = build_paths(x_start, y_start, "")

    # Paths that use repeated characters are better than paths that don't.
    # Reason for this is that for example:
    # - "v<<A" is controlled using "v<A<AA" while
    # - "<v<A" is controlled using "v<<A>A<A"
    # The route with repeated characters gives us less work to do on the
    # controlling directional keypad.
    def score_path(path):
        return sum(a == b for (a, b) in zip(path, path[1:]))

    return max(all_paths, key=score_path)
    #lambda p: sum(a != b for a, b in zip(p, p[1 :])))

@cache
def find_code_length(code: str, intermediate_robots: int = 0, is_numpad=True) -> int:
    # < 0, because we start out with the numpad,
    # which is not controlling an intermediate robot.
    if intermediate_robots < 0:
        return len(code)

    keypad = numpad if is_numpad else dirpad
    parts = [
        find_code_length(
            find_path(
                keypad, key_start, key_finish
            ), intermediate_robots - 1, False
        )
        for key_start, key_finish in zip('A' + code, code)
    ]
    return sum(parts)


def load_codes():
    return sys.stdin.read().splitlines()


total = 0
for code in load_codes():
    parent_code = find_code_length(code, intermediate_robots=25)
    score = int(code[:-1]) * parent_code
    total += score

print("Total:", total)
