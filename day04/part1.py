#!/usr/bin/env python3

import sys


def load_grid():
    return [list(line.strip()) for line in sys.stdin]


def count_words_in_grid(grid, word):
    return sum(
        found
        for x, y in all_grid_coordinates(grid)
        for found in find_word_at(grid, x, y, word)
    )


def find_word_at(grid, x, y, word):
    if word[0] == grid[y][x]:
        for dir_x, dir_y in all_directions():
            yield find_in_direction(grid, x, y, dir_x, dir_y, word)


def all_grid_coordinates(grid):
    width = len(grid[0])
    height = len(grid)
    for coordinate in ((x, y) for y in range(0, height) for x in range(0, width)):
        yield coordinate


def all_directions():
    yield 1, 0
    yield 1, 1
    yield 0, 1
    yield -1, 1
    yield -1, 0
    yield -1, -1
    yield 0, -1
    yield 1, -1


def find_in_direction(grid, x, y, dir_x, dir_y, word):
    if word == "":
        return True
    if not is_inside_grid(grid, x, y):
        return False
    char_at_coordinate = grid[y][x]
    if word[0] == char_at_coordinate:
        return find_in_direction(grid, x + dir_x, y + dir_y, dir_x, dir_y, word[1:])
    return False


def is_inside_grid(grid, x, y):
    if x < 0 or y < 0:
        return False
    if x >= len(grid[0]):
        return False
    if y >= len(grid):
        return False
    return True


grid = load_grid()
word_count = count_words_in_grid(grid, "XMAS")
print("Found:", word_count)
