#!/usr/bin/env python3

import sys
from heapq import heappush, heappop
from collections import defaultdict

MAX_CHEAT_TIME = 20
MINIMAL_GAIN_TO_REPORT = 100


def load_scenario():
    def find(item):
        return next(
            (x, y)
            for y, row in enumerate(maze)
            for x, cell in enumerate(row)
            if maze[y][x] == item
        )

    maze = [list(line.strip()) for line in sys.stdin]
    return maze, find("S"), find("E")


def race(maze, start, finish):
    x, y = start
    w = len(maze[0])
    h = len(maze)
    time = 0
    time_from_start = {start: time}

    while (x, y) != finish:
        dx, dy = 0, -1
        for _ in range(4):
            dx, dy = -dy, dx
            x2, y2 = x + dx, y + dy
            if (x2, y2) in time_from_start:
                continue
            if maze[y2][x2] != "#":
                time += 1
                time_from_start[(x2, y2)] = time
                x, y = x2, y2
                break

    return time_from_start


def find_cheat_routes(scenario, time_from_start):
    maze, _, _ = scenario
    w = len(maze[0])
    h = len(maze)

    def find_cheat_jumps(start):
        queue = []
        heappush(queue, (0, *start))
        seen = set()

        while queue:
            time, x, y = heappop(queue)
            time += 1

            # Move into all four directions.
            dx, dy = 0, -1
            for _ in range(4):
                dx, dy = -dy, dx
                x2, y2 = x + dx, y + dy

                # Make sure we stay within bounds.
                if x2 == 0 or y2 == 0 or x2 == w-1 or y2 == h-1:
                    continue

                # Skip positions that we have already seen.
                if (x2, y2) in seen:
                    continue
                seen.add((x2, y2))

                # Non-wall found. This is the possible end of a cheat route.
                if maze[y2][x2] != "#":
                    yield start, (x2, y2), time

                if time < MAX_CHEAT_TIME:
                    heappush(queue, (time, x2, y2))


    routes = defaultdict(lambda: float("inf"))
    for start, t_start in time_from_start.items():
        for start, end, t_cheat in find_cheat_jumps(start):
            routes[start, end] = min(routes[start, end], t_cheat)
    return routes


scenario = load_scenario()
time_from_start = race(*scenario)
cheat_routes = find_cheat_routes(scenario, time_from_start)

good_cheats = 0
for (start_pos, end_pos), cheat_time in cheat_routes.items():
    t_fair = time_from_start[end_pos]
    t_cheat = time_from_start[start_pos] + cheat_time
    t_gain = t_fair - t_cheat
    if t_gain >= MINIMAL_GAIN_TO_REPORT:
        good_cheats += 1

print("Number of good cheats:", good_cheats)
