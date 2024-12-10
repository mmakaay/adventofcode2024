#!/usr/bin/env python3

import sys


def load_topography():
    heights = [list(map(int, line.strip())) for line in sys.stdin]
    return (len(heights[0]), len(heights), heights)


def find_trailheads(topography):
    w, h, heights = topography
    return ((x, y) for y in range(h) for x in range(w) if heights[y][x] == 0)


def hike_to_all_tops(topography, start):
    w, h, heights = topography
    x, y = start
    current_height = heights[y][x]

    if current_height == 9:
        yield (x, y)
        return

    if x > 0 and heights[y][x - 1] == current_height + 1:
        yield from hike_to_all_tops(topography, (x - 1, y))
    if x < w - 1 and heights[y][x + 1] == current_height + 1:
        yield from hike_to_all_tops(topography, (x + 1, y))
    if y > 0 and heights[y - 1][x] == current_height + 1:
        yield from hike_to_all_tops(topography, (x, y - 1))
    if y < h - 1 and heights[y + 1][x] == current_height + 1:
        yield from hike_to_all_tops(topography, (x, y + 1))


total = 0

topography = load_topography()
for trailhead in find_trailheads(topography):
    tops = set(hike_to_all_tops(topography, trailhead))
    total += len(tops)

print("Total score:", total)
