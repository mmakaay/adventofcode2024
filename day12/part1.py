#!/usr/bin/env python3

import sys
from collections import defaultdict


def load_garden():
    plots = [list(line.strip()) for line in sys.stdin]
    width = len(plots[0])
    height = len(plots)
    return width, height, plots


def all_coordinates(garden):
    width, height, _ = garden
    for y in range(height):
        for x in range(width):
            yield (x, y)


def find_regions(garden):
    width, height, plots = garden
    seen = set()

    def inspect_plot(position, region):
        seen.add(position)
        region["plots"] += 1
        x, y = position
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            x2, y2 = x + dx, y + dy
            if is_same_plant(x, y, x2, y2):
                if (x2, y2) not in seen:
                    inspect_plot((x2, y2), region)
            else:
                region["boundaries"] += 1

    def is_same_plant(x, y, x2, y2):
        return is_inside_garden(x2, y2) and plots[y][x] == plots[y2][x2]

    def is_inside_garden(x, y):
        return 0 <= x < width and 0 <= y < height

    for position in all_coordinates(garden):
        if position not in seen:
            region = {"boundaries": 0, "plots": 0}
            inspect_plot(position, region)
            yield region


def compute_fence_price(regions):
    return sum(
        region["plots"] * region["boundaries"]
        for region in regions
    )


garden = load_garden()
regions = find_regions(garden)
price = compute_fence_price(regions)

print("Fence price:", price)
