#!/usr/bin/env python3

import sys
from heapq import heappush, heappop

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

    # Cost mapping storage, used to keep track of the lowest possible
    # cost that was found to reach the states in the maze.
    costs = {}

    def is_wall(x, y):
        return maze[y][x] == "#"

    def enqueue_when_cheaper(cost, state):
        if state not in costs or cost < costs[state]:
            costs[state] = cost
            heappush(queue, (cost, state))

    # Initialize state, using start direction = east.
    enqueue_when_cheaper(0, (*start, EAST))

    while queue:
        cost, (x, y, direction) = heappop(queue)

        # When the end is reached, we are done.
        if (x, y) == end:
            return cost

        # Try to move one position forward.
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        if not is_wall(new_x, new_y):
            new_cost = cost + STEP_COST
            enqueue_when_cheaper(new_cost, (new_x, new_y, direction))

        # Try to rotate into the other directions.
        for rotation in (-1, +1):
            new_direction = (direction + rotation) % 4
            new_cost = cost + ROTATE_COST
            enqueue_when_cheaper(new_cost, (x, y, new_direction))


scenario = load_scenario()
cost = find_best_route_through_maze(*scenario)
print(cost)

