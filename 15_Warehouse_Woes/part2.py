#!/usr/bin/env python3

import sys


def load_scenario():
    warehouse = []
    program = []

    for row_nr, line in enumerate(sys.stdin):
        line = line.strip()
        if line.startswith("#"):
            row = ""
            for col_nr, p in enumerate(line):
                if p == "@":
                    item = "@."
                    robot = (2 * col_nr, row_nr)
                elif p == "#":
                    item = "##"
                elif p == ".":
                    item = ".."
                else:
                    item = "[]"
                row += item
            warehouse.append(list(row))
        elif line == "":
            continue
        else:
            program.extend(list(line))

    return warehouse, robot, program


DIRECTIONS = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def play_scenario(scenario):
    warehouse, robot, program = scenario

    # Variables used for collecting the moves that are
    # required for a single program step.
    moves = []
    seen = set()

    def can_move(position, direction, is_fork=False):
        # Do not process items twice.
        if position in seen:
            return False
        seen.add(position)

        # Get the item to move.
        x, y = position
        item = warehouse[y][x]

        # When moving a block vertically, then fork to process both sides.
        if not is_fork and item in "[]" and direction in "v^":
            other_side = x + (-1 if item == "]" else +1)
            if not can_move((other_side, y), direction, True):
                return False

        # Compute the position to move the item to.
        dx, dy = DIRECTIONS[direction]
        to_x, to_y = x + dx, y + dy
        target_item = warehouse[to_y][to_x]

        # Walls block movement.
        if target_item == "#":
            return False

        # Moving to a free spot is always possible. Moving to an occupied
        # spot is possible, when the item at that spot can be moved itself.
        if target_item == "." or can_move((to_x, to_y), direction):
            moves.append((x, y, to_x, to_y))
            return True

        # The item cannot be moved.
        return False

    def perform_moves():
        for x, y, to_x, to_y in moves:
            warehouse[to_y][to_x] = warehouse[y][x]
            warehouse[y][x] = "."
            if warehouse[to_y][to_x] == "@":
                robot = (to_x, to_y)
        return robot

    def reset():
        moves.clear()
        seen.clear()

    for direction in program:
        reset()
        if can_move(robot, direction):
            robot = perform_moves()

    return warehouse


def all_gps_coordinates(warehouse):
    def gps_coordinate(x, y):
        return x + 100 * y

    return (
        gps_coordinate(x, y)
        for y, row in enumerate(warehouse)
        for x, item in enumerate(row)
        if item == "["
    )


scenario = load_scenario()
warehouse = play_scenario(scenario)
total = sum(gps for gps in all_gps_coordinates(warehouse))

print("Total of GPS coordinates:", total)
