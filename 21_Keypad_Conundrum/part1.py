#!/usr/bin/env python3

import sys
from itertools import product
from heapq import heappush, heappop
from functools import cache


def build_keypad_specs(keypad):
    """Builds a mapping for (keyA, keyB) to a list of all possible navigation
    steps from keyA to keyB that take the least amount of steps."""

    key2position = {
        key: (x, y)
        for y, row in enumerate(keypad)
        for x, key in enumerate(row)
    }

    position2key = {position: key for key, position in key2position.items()}

    def get_best_navigation_options(start_key, finish_key):
        queue = []
        start = key2position[start_key]
        heappush(queue, (0, *start, []))
        minimal_length = float("inf")
        while queue:
            length, x, y, route = heappop(queue)
            length += 1

            # Skip position if it is not a best route candidate.
            if length > minimal_length:
                continue

            # Route found! The first time we get here, we found the best
            # route in terms of the number of steps. Any other route candidates
            # must have the same amount of steps.
            if position2key[(x, y)] == finish_key:
                minimal_length = length
                yield route
                continue

            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                x2, y2 = x + dx, y + dy
                if (x2, y2) in position2key and position2key[(x2, y2)] != " ":
                    heappush(queue, (length, x2, y2, route + [(dx, dy)]))

    navigation_options = {}
    key_names = list(key2position.keys())
    for start_key, finish_key in product(key_names, key_names):
        if start_key != " " and finish_key != " ":
            best_navigation_options = list(get_best_navigation_options(start_key, finish_key))
            navigation_options[(start_key, finish_key)] = best_navigation_options

    return navigation_options

numpad_specs = build_keypad_specs((("7", "8", "9"), ("4", "5", "6"), ("1", "2", "3"), (" ", "0", "A")))
dirpad_specs = build_keypad_specs(((" ", "^", "A"), ("<", "v", ">")))


def nav_steps_to_dirpad_code(route):
    """Translate a list of navigation directions into dirpad button presses."""
    direction_to_controller_press = {
        (1, 0): ">",
        (-1, 0): "<",
        (0, -1): "^",
        (0, 1): "v",
        "A": "A",
    }
    return "".join(
        direction_to_controller_press[direction] for direction in route
    )
        

def load_codes():
    return sys.stdin.read().splitlines()


@cache
def get_dirpad_navigation(code):
    if any(c in code for c in "<^V>"):
        keypad_specs = dirpad_specs
    else:
        keypad_specs = numpad_specs

    # Compose a list of key transitions for the provided code.
    # All robots start at "A", so prepending an implicit transition from A.
    transitions = [("A", code[0])] + list(zip(code, code[1:]))

    # Collect possible navigation options for each of the transitions.
    # For each transition, there can be multiple navigation options.
    nav_steps_per_transition = [
        keypad_specs[transition] for transition in transitions
    ]

    # Create a product of the navigation options for each transition.
    # This will provide us with all the possible overall navigation options.
    dirpad_codes = []
    for navigation_product in product(*nav_steps_per_transition):
        # Flatten the navigation steps, and add "A" after each tansition to
        # add an A step for the key that was navigated to, to activate
        # the selected key.
        full_navigation = tuple(
            d for group in navigation_product for d in group + ["A"]
        )
        dirpad_codes.append(nav_steps_to_dirpad_code(full_navigation))
    return tuple(dirpad_codes)


total = 0

for code in load_codes():
    shortest = None
    for code2 in get_dirpad_navigation(code):
        for code3 in get_dirpad_navigation(code2):
            for code4 in get_dirpad_navigation(code3):
                if shortest is None or len(shortest) > len(code4):
                    shortest = code4
    score = int(code[0:-1]) * len(shortest)
    print(code, "-->", code4, "score=", score)
    total += score

print("Total:", total)
