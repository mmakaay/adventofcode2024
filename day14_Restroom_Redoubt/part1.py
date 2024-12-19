#!/usr/bin/env python3

import sys
import re
from functools import reduce
from operator import mul
from collections import defaultdict


def load_robots():
    robots = []
    for line in sys.stdin:
        if m := re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line):
            robot = (
                (int(m.group(1)), int(m.group(2))),
                (int(m.group(3)), int(m.group(4))),
            )
            robots.append(robot)
    return robots


def find_bathroom_size(robots):
    # Note: the example and real input both have robots on the
    # far right and bottom, so we can look at the robots to
    # determine the bathroom size.
    w = max(x for (x, _), _ in robots) + 1
    h = max(y for (_, y), _ in robots) + 1
    return (w, h)


def move_once(robots, bathroom):
    w, h = bathroom
    def step(robot):
        (x, y), (dx, dy) = robot
        return ((x + dx, y + dy), (dx, dy))

    def teleport(robot):
        (x, y), direction = robot
        return ((x % w, y % h), direction)

    moved_robots = []
    occupied_spaces = defaultdict(int)
    for robot in robots:
        moved_robot = teleport(step(robot))
        moved_robots.append(moved_robot)
        occupied_spaces[moved_robot[0]] += 1
    return moved_robots, occupied_spaces


def compute_safety_factor(occupied_spaces, bathroom):
    count_per_quadrant = get_robot_count_per_quadrant(occupied_spaces, bathroom)
    safety_factor = reduce(mul, (count_per_quadrant.values()))
    return safety_factor


def get_robot_count_per_quadrant(occupied_spaces, bathroom):
    w, h = bathroom
    mid_w = w // 2
    mid_h = h // 2

    def determine_quadrant(x, y):
        if x < mid_w and y < mid_h: return 1
        if x > mid_w and y < mid_h: return 2
        if x < mid_w and y > mid_h: return 3
        if x > mid_w and y > mid_h: return 4
        return 0

    count_per_quadrant = {1: 0, 2: 0, 3: 0, 4: 0}
    for (x, y), robot_count in occupied_spaces.items():
        quadrant = determine_quadrant(x, y)
        if quadrant:
            count_per_quadrant[quadrant] += robot_count
    return count_per_quadrant 


robots = load_robots()
bathroom = find_bathroom_size(robots)
for _ in range(100):
    robots, occupied_spaces = move_once(robots, bathroom)
safety_factor = compute_safety_factor(occupied_spaces, bathroom)

print("Bathroom safety factor:", safety_factor)
