#!/usr/bin/env python3

import sys


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


def find_cheat_time_gains(scenario, time_from_start):
    maze, _, _ = scenario
    w = len(maze[0])
    h = len(maze)

    for (x, y), t_start in time_from_start.items():
        dx, dy = 0, -1
        for _ in range(4):
            dx, dy = -dy, dx
            x2, y2 = x + dx, y + dy
            if maze[y2][x2] == "#":
                x3, y3 = x2 + dx, y2 + dy
                if 0<x3<w and 0<y3<h and maze[y3][x3] != "#":
                    t_fair = time_from_start[(x3, y3)]
                    t_cheat = t_start + 2
                    t_gain = t_fair - t_cheat
                    if t_gain > 0:
                        yield t_gain

scenario = load_scenario()
time_from_start = race(*scenario)
cheat_time_gains = find_cheat_time_gains(scenario, time_from_start)
good_cheats = [t for t in cheat_time_gains if t >= 100]

print("Number of good cheats:", len(good_cheats))
