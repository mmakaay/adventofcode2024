#!/usr/bin/env python3

import sys
from heapq import heappush, heappop


def load_warzone():
    impacts = [tuple(map(int, line.strip().split(","))) for line in sys.stdin]
    width = max(x for x, _ in impacts) + 1
    height = max(y for _, y in impacts) + 1
    return width, height, impacts


def get_number_of_impacts_to_simulate():
    try:
        return int(sys.argv[1])
    except IndexError:
        print(f"Usage: {sys.argv[0]} <nr of bytes to simulate> < input")
        sys.exit(1)


def plan_safe_route(warzone, start, end, number_of_impacts):
    width, height, impacts = warzone
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    # A priority queue, used for queueing routes to poll, and
    # processing them from lowest to highest cost so far.
    queue = []

    # Cost mapping storage, used to keep track of the lowest possible
    # cost that was found to reach the states in the maze.
    costs = {}

    def is_impact_zone(x, y, number_of_impacts):
        return (x, y) in impacts[:number_of_impacts]

    def enqueue(cost, state):
        if state not in costs or cost < costs[state]:
            costs[state] = cost
            heappush(queue, (cost, state))

    # Initialize state.
    costs[start] = 0
    heappush(queue, (0, start))

    while queue:
        cost, (x, y) = heappop(queue)

        if (x, y) == end:
            return cost

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < width and 0 <= new_y < height:
                if not is_impact_zone(new_x, new_y, number_of_impacts):
                    enqueue(cost + 1, (new_x, new_y))


number_of_impacts = get_number_of_impacts_to_simulate()
warzone = width, height, _ = load_warzone()
start = (0, 0)
end = (width - 1, height - 1)
shortest_path_length = plan_safe_route(warzone, start, end, number_of_impacts)

print("Shortest path at", number_of_impacts, "impacts:", shortest_path_length)
