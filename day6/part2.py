#!/usr/bin/env python3

import sys


def load_grid():
    grid = []
    for line in sys.stdin:
        grid.append(list(line.strip()))

    w = len(grid[0])
    h = len(grid)
    return (w, h), grid


def find_guard(grid):
    (w, h), matrix = grid
    return next(
        ((x, y), (0, -1))
        for x in range(w)
        for y in range(h)
        if matrix[y][x] == "^"
    )


def find_blocks_causing_loops(grid, guard):
    tried_blocks = set()
    for next_guard in walk(grid, guard):
        next_position, _ = next_guard
        if next_position in tried_blocks:
            continue
        tried_blocks.add(next_position)

        add_block(grid, next_position)
        if grid_contains_loop(grid, guard):
            yield next_position
        remove_block(grid, next_position)

        guard = next_guard


def walk(grid, guard):
    while guard := move_guard_one_step(grid, guard):
        yield guard


def move_guard_one_step(grid, guard):
    for _ in range(4):
        next_guard = move(guard)
        if is_off_grid(grid, next_guard):
            return None
        if not is_blocked(grid, next_guard):
            return next_guard
        guard = turn_right(guard)
    raise ValueError("Stuck!")


def move(guard):
    (x, y), (dx, dy) = guard
    return ((x + dx, y + dy), (dx, dy))


def is_off_grid(grid, guard):
    (w, h), _ = grid
    (x, y), _ = guard
    return x < 0 or y < 0 or x >= w or y >= h


def is_blocked(grid, guard):
    _, matrix = grid
    (x, y), _ = guard
    return matrix[y][x] == "#"


def turn_right(guard):
    position, direction = guard
    match direction:
        case (0, -1):
            return (position, (1, 0))
        case (1, 0):
            return (position, (0, 1))
        case (0, 1):
            return (position, (-1, 0))
        case (-1, 0):
            return (position, (0, -1))


def add_block(grid, position):
    _, matrix = grid
    (x, y) = position
    matrix[y][x] = "#"


def grid_contains_loop(grid, guard):
    seen = set()
    for guard in walk(grid, guard):
        if guard in seen:
            return True
        seen.add(guard)
    return False


def remove_block(grid, position):
    _, matrix = grid
    (x, y) = position
    matrix[y][x] = "."


grid = load_grid()
guard = find_guard(grid)
successful_blocks = list(find_blocks_causing_loops(grid, guard))

print("Number of block options:", len(successful_blocks))
