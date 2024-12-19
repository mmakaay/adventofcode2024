#!/usr/bin/env python3

import sys
from heapq import heappush, heappop
from pathlib import Path
from collections import defaultdict, deque

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


def find_lowest_cost(maze, start, end):
    # A priority queue, used for queueing routes to poll, and
    # processing them from lowest to highest cost so far.
    queue = []

    # Cost mapping storage, used to keep track of the lowest possible
    # costs that were found to reach the states in the maze.
    costs = defaultdict(lambda: float("inf"))

    # Initialize state, using start direction = east.
    costs[(0, 0, 1, 0)] = 0
    heappush(queue, (0, (*start, 1, 0)))

    while queue:
        cost, state = heappop(queue)
        x, y, dx, dy = state

        # Walking through walls is a bad idea.
        if maze[y][x] == "#":
            continue

        # Found the end of the maze. The first time we find this,
        # we have found the cheapest route. Keep track of the cost
        # of this cheapest route, so we can reject other routes
        # coming in that have a worse overall cost.
        if (x, y) == end:
            return cost

        # Start moving.
        for new_state, new_cost in (
            ((x + dx, y + dy, dx, dy), cost + STEP_COST), # forward
            ((x, y, -dy, dx), cost + ROTATE_COST), # clockwise
            ((x, y, dy, -dx), cost + ROTATE_COST),# counter-clockwise
        ):
            # If we already have a better route to the new state,
            # then stop following this one.
            if new_cost > costs[new_state]:
                continue

            # If we found a better route to the new state, then
            # enqueue the move to explore the route further.
            if new_cost < costs[new_state]:
                heappush(queue, (new_cost, new_state))
                costs[new_state] = new_cost


maze, start, end = load_scenario()
lowest_cost = find_lowest_cost(maze, start, end)

print(lowest_cost == 78428)

