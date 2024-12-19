#!/usr/bin/env python3

import sys


def load_garden():
    plots = [list(line.strip()) for line in sys.stdin]
    width = len(plots[0])
    height = len(plots)
    return width, height, plots


def find_regions(garden):
    width, height, plots = garden
    seen = set()

    def all_coordinates():
        for y in range(height):
            for x in range(width):
                yield (x, y)

    def inspect_plot(position, region):
        x, y = position
        region["plots"] += 1
        seen.add(position)

        # Count circumference corners to find the number of sides.
        # See README.md for logic.
        for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            side_same = is_same_plant(x, y, x + dx, y)
            below_same = is_same_plant(x, y, x, y + dy)
            diag_same = is_same_plant(x, y, x + dx, y + dy)
            if side_same and below_same and not diag_same:
                region["sides"] += 1
            elif not side_same and not below_same:
                region["sides"] += 1

        # Recursively visit the plots in the same region.
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            x2, y2 = x + dx, y + dy
            if is_same_plant(x, y, x2, y2):
                if (x2, y2) not in seen:
                    inspect_plot((x2, y2), region)

    def is_same_plant(x, y, x2, y2):
        return is_inside_garden(x2, y2) and plots[y][x] == plots[y2][x2]

    def is_inside_garden(x, y):
        return 0 <= x < width and 0 <= y < height

    # Visit and inspect all plots to find the regions and their properties.
    for position in all_coordinates():
        if position not in seen:
            region = ({"sides": 0, "plots": 0})
            inspect_plot(position, region)
            yield region


def compute_fence_price(regions):
    return sum(
        region["plots"] * region["sides"]
        for region in regions
    )


garden = load_garden()
regions = find_regions(garden)
price = compute_fence_price(regions)

print("Fence price:", price)
