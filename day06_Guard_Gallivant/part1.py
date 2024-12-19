#!/usr/bin/env python3

import sys


def load_grid():
    grid = []
    for line in sys.stdin:
        grid.append(list(line.strip()))
    return grid


def find_guard(grid):
    return next(
        (x, y)
        for x in range(0, len(grid[0]))
        for y in range(0, len(grid))
        if at(grid, (x, y)) == "^"
    )


def at(grid, position):
    x, y = position
    return grid[y][x]


def walk(grid, position, direction=(0, -1)):
    while True:
        mark_step(grid, position)
        next_position = move(position, direction)
        if is_off_grid(grid, next_position):
            return
        if at(grid, next_position) == "#":
            direction = turn_right(direction)
            next_position = move(position, direction)
        position = next_position


def is_off_grid(grid, position):
    x, y = position
    if x < 0 or y < 0:
        return True
    if x >= len(grid[0]):
        return True
    if y >= len(grid):
        return True
    return False


def mark_step(grid, position):
    x, y = position
    grid[y][x] = "X"


def move(position, direction):
    return (position[0] + direction[0], position[1] + direction[1])


def turn_right(direction):
    match direction:
        case (0, -1):
            return (1, 0)
        case (1, 0):
            return (0, 1)
        case (0, 1):
            return (-1, 0)
        case (-1, 0):
            return (0, -1)


def count_steps(grid):
    return sum(
        at(grid, (x, y)) == "X"
        for x in range(0, len(grid[0]))
        for y in range(0, len(grid))
    )


grid = load_grid()
position = find_guard(grid)
walk(grid, position)
steps = count_steps(grid)

print("Positions:", steps)
