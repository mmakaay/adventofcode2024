#!/usr/bin/env python3

import sys
from heapq import heappush, heappop
from pathlib import Path

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
EAST = 1
STEP_COST = 1
ROTATE_COST = 1000


def load_scenario():
    p = Path(__file__).parent / "test2.txt"
    with p.open() as f:
        maze = [list(line.strip()) for line in f]

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
    # cost that was found to reach the states in the maze.
    costs = {}

    # Used for backtracking lowest cost routes from end to start.
    backtrace = {}

    def is_wall(x, y):
        return maze[y][x] == "#"

    # 0################
    # 1.#.#.....#█████#
    # 2.#.#######█#.#.#
    # 3.#........█#...#
    # 4.#########█#####  10,5,1 -> 2011
    # 5.#....████x████#  10,5,0 -> 3011
    # 6.#####█#######█#  11,5,3 -> 2020
    # 7███████████████#  10,5,3 -> 2021
    # #1234567890123456  10,5,0 -> 3021

    def enqueue_move(old_state, new_state, new_cost):
        (new_x, new_y, new_direction) = new_state
        new_pos = (new_x, new_y)
        if new_state not in costs or new_cost < costs[new_pos]:
            print("QUEUE CHEAPER")
            costs[new_pos] = new_cost
            heappush(queue, (new_cost, new_state))
            if old_state:
                (old_x, old_y, _) = old_state
                backtrace.setdefault(new_pos, {})[new_direction] = [(old_x, old_y)]

        elif old_state and (new_state not in costs or new_cost == costs[new_pos]):
            print("QUEUE EQUAL")
            (old_x, old_y, _) = old_state
            backtrace[new_pos][new_direction].append((x, y))
        else:
            print("NOQUEUE")


    # Initialize state, using start direction = east.
    enqueue_move(None, (*start, EAST), 0)

    while queue:
        cost, state = heappop(queue)
        (x, y, direction) = state

        # When the end is reached, we are done.
        if (x, y) == end:
            return cost, costs, backtrace

        print("POP", state, "COST", cost, "existing cost", costs[state])

        # Try to rotate into the other directions.
        for rotation in (-1, +1):
            new_direction = (direction + rotation) % 4
            new_cost = cost + ROTATE_COST
            new_state = (x, y, new_direction)
            print("ENQUEUE rotate", rotation, "=", new_state, new_cost)
            enqueue_move(state, new_state, new_cost)

        # Try to move one position forward.
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        if not is_wall(new_x, new_y):
            new_cost = cost + STEP_COST
            new_state = (new_x, new_y, direction)
            print("ENQUEUE step", state, "->", new_state, new_cost)
            enqueue_move(state, new_state, new_cost)

def find_visited_tiles(scenario, routes):
    maze_, start, end = scenario
    cost, costs, backtrace = routes
    tiles = set()

    def trace(position):
        if position in tiles:
            return
        tiles.add(position)
        for predecessors in backtrace[position].values():
            for predecessor in predecessors:
                trace(predecessor)

    trace(end)
    return tiles


def visualize(maze, start, end, tiles):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            p = "█" if (x, y) in tiles else maze[y][x]
            print(p, end="")
        print()


scenario = load_scenario()
routes = find_cheapest_routes(*scenario)
visited_tiles = find_visited_tiles(scenario, routes)

visualize(*scenario, visited_tiles)
print("Number of visited tiles:", len(visited_tiles))
