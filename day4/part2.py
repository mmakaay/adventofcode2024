#!/usr/bin/env python3

import sys


def load_grid():
    return [list(line.strip()) for line in sys.stdin]


def count_x_masses_in_grid(grid):
    return sum(grid_has_xmas_at(grid, x, y) for x, y in all_possible_mid_points(grid))


def all_possible_mid_points(grid):
    width = len(grid[0])
    height = len(grid)
    for coordinate in (
        (x, y) for y in range(1, height - 1) for x in range(1, width - 1)
    ):
        yield coordinate


def grid_has_xmas_at(grid, x, y):
    if grid[y][x] != "A":
        return False
    top_left = grid[y - 1][x - 1]
    top_right = grid[y - 1][x + 1]
    bottom_left = grid[y + 1][x - 1]
    bottom_right = grid[y + 1][x + 1]
    return {top_left, bottom_right} == {top_right, bottom_left} == {"M", "S"}


grid = load_grid()
word_count = count_x_masses_in_grid(grid)
print("Found:", word_count)
