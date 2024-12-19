#!/usr/bin/env python3

import sys


def load_scenario():
    warehouse = []
    program = []

    for row_nr, line in enumerate(sys.stdin):
        line = line.strip()
        if line.startswith("#"):
            row = list(line)
            warehouse.append(row) 
            if "@" in row:
                robot = (row.index("@"), row_nr)
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

    def can_move(robot, direction):
        path = []
        x, y = robot
        dx, dy = DIRECTIONS[direction]
        path.append((x, y))
        while True:
            x += dx
            y += dy
            path.append((x, y))
            state = warehouse[y][x]
            if state == ".":
                return path
            elif state == "#":
                return None

    def move(robot, path):
        for i, (x, y) in enumerate(path):
            if i == 0:
                warehouse[y][x] = "."
            elif i == 1:
                warehouse[y][x] = "@"
                robot = (x, y)
            else:
                warehouse[y][x] = "O"
        return robot
    
    for direction in program:
        if path := can_move(robot, direction):
            robot = move(robot, path)
    return warehouse


def all_gps_coordinates(warehouse):
    def gps_coordinate(x, y):
        return x + 100 * y

    return (
        gps_coordinate(x, y)
        for y, row in enumerate(warehouse)
        for x, item in enumerate(row)
        if item == "O"
    )


scenario = load_scenario()
warehouse = play_scenario(scenario)
total = sum(gps for gps in all_gps_coordinates(warehouse))

print("Total of GPS coordinates:", total)
