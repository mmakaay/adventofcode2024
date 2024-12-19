#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import combinations


def read_input():
    antennas = defaultdict(list)
    for y, line in enumerate(map(str.strip, sys.stdin)):
        for x, frequency in enumerate(line):
            if frequency != ".":
                position = complex(x, y)
                antennas[frequency].append(position)
    w = x + 1
    h = y + 1
    return (w, h), antennas


def get_antinodes(grid_size, positions):
    for pair in combinations(positions, 2):
        yield from get_antinodes_for_pair(grid_size, *pair)


def get_antinodes_for_pair(grid_size, a, b):
    coefficient = a - b
    while is_inside_grid(grid_size, a):
        yield a
        a = a + coefficient
    while is_inside_grid(grid_size, b):
        yield b
        b = b - coefficient


def is_inside_grid(grid_size, position):
    x, y = position.real, position.imag
    w, h = grid_size
    return x >= 0 and y >= 0 and x < w and y < h


grid_size, antennas_by_frequency = read_input()
antinodes = set(
    antinode
    for positions in antennas_by_frequency.values()
    for antinode in get_antinodes(grid_size, positions)
)

print("Total number of antinodes:", len(antinodes))
