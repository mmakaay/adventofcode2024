#!/usr/bin/env python3

import sys
from heapq import heappush, heappop
from collections import defaultdict

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
EAST = 1
STEP_COST = 1
ROTATE_COST = 1000


def load_scenario():
    maze = [list(line.strip()) for line in sys.stdin]

    def find(item):
        return next(
            (x, y)
            for y, row in enumerate(maze) 
            for x, cell in enumerate(row)
            if maze[y][x] == item
        )

    start = find("S")
    end = find("E")

    return maze, start, end


def find_best_route_through_maze(maze, start, end):
    # A priority queue, used for queueing routes to poll, and
    # processing them from lowest to highest cost so far.
    queue = []

    # Cost mapping storage, that is used to keep track of the lowest
    # cost routes that were found to reach certain positions on the
    # maze when moving in a certain direction. This is used to decide
    # whether or not it is feasible to continue tracing a route: it is
    # not when the cost of the trace at hand exceeds an already known
    # cheaper route.
    costs = defaultdict(lambda: defaultdict(lambda: [None]*4))

    def is_wall(x, y):
        return maze[y][x] == "#"

    def enqueue_when_feasible(x, y, direction, cost):
        existing_cost = costs[y][x][direction]
        if existing_cost is None or cost < existing_cost:
            costs[y][x][direction] = cost
            heappush(queue, (cost, x, y, direction))

    # Initialize state, using start direction = east.
    enqueue_when_feasible(*start, EAST, 0)

    while queue:
        cost, x, y, direction = heappop(queue)

        # When the end is reached, we are done.
        if (x, y) == end:
            return cost

        # Try to move one position forward.
        dx, dy = DIRECTIONS[direction]
        x2, y2 = x + dx, y + dy
        if not is_wall(x2, y2):
            new_cost = cost + STEP_COST
            enqueue_when_feasible(x2, y2, direction, new_cost)

        # Try to rotate into the other directions.
        for rotation in (-1, +1):
            new_direction = (direction + rotation) % 4
            new_cost = cost + ROTATE_COST
            enqueue_when_feasible(x, y, new_direction, new_cost)


scenario = load_scenario()
cost = find_best_route_through_maze(*scenario)
print(cost)

