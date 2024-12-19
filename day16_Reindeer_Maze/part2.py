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


def find_cheapest_routes(maze, start, end):
    # A priority queue, used for queueing routes to poll, and
    # processing them from lowest to highest cost so far.
    queue = []

    # Cost mapping storage, used to keep track of the lowest possible
    # costs that were found to reach the states in the maze.
    costs = defaultdict(lambda: float("inf"))
    cheapest = float("inf")

    # Used for backtracking lowest cost routes from end to start.
    backtrack = {}

    # Initialize state, using start direction = east.
    costs[(0, 0, 1, 0)] = 0
    heappush(queue, (0, (*start, 1, 0)))

    while queue:
        cost, state = heappop(queue)
        x, y, dx, dy = state

        # Walking through walls is a bad idea.
        if maze[y][x] == "#":
            continue

        # Don't follow a route when it's worse than the cheapest.
        if cost > cheapest:
            continue

        # Found the end of the maze. The first time we find this,
        # we have found the cheapest route. Keep track of the cost
        # of this cheapest route, so we can reject other routes
        # coming in that have a worse overall cost.
        if (x, y) == end:
            cheapest = cost
            continue

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

            # If we found a better route to the new state, then reset
            # the backtrack to ditch existing, more expensive routes,
            # and enqueue the move to explore the route further.
            if new_cost < costs[new_state]:
                backtrack[new_state] = set()
                heappush(queue, (new_cost, new_state))

            # Update cost and backtrack information. This will also
            # add a new backtrack item when we are on a route that
            # is equally expensive as the currently cheapest route.
            costs[new_state] = new_cost
            backtrack[new_state].add(state)

    return backtrack


def find_visited_tiles(end, backtrack):
    end_tiles = (
        (x, y, dx, dy)
        for x, y, dx, dy in backtrack
        if (x, y) == end
    )
    queue = deque(end_tiles)

    seen = set()
    visited_tiles = set()
    while queue:
        state = x, y, _, _ = queue.pop()
        visited_tiles.add((x, y))
        if state not in seen:
            seen.add(state)
            queue.extend(backtrack[state])

    return visited_tiles


def visualize(maze, visited_tiles):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            p = "█" if (x, y) in visited_tiles else maze[y][x]
            print(p, end="")
        print()


maze, start, end = load_scenario()
backtrack = find_cheapest_routes(maze, start, end)
visited_tiles = find_visited_tiles(end, backtrack)
visualize(maze, visited_tiles)

print("Number of visited tiles:", len(visited_tiles))

