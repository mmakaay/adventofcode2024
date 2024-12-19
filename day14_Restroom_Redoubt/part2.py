#!/usr/bin/env python3

import sys
import re

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
    occupied_spaces = set()
    for robot in robots:
        moved_robot = teleport(step(robot))
        moved_robots.append(moved_robot)
        occupied_spaces.add(moved_robot[0])
    return moved_robots, occupied_spaces


def there_could_be_a_tree(occupied_spaces, bathroom):
    w, h = bathroom
    line_length = 0
    for y in range(h):
        for x in range(w):
            if (x, y) in occupied_spaces:
                line_length +=1
            else:
                line_length = 0
            if line_length > 10:
                return True
    return False



def visualize(occupied_spaces, bathroom):
    w, h = bathroom
    for y in range(h):
        for x in range(w):
            if (x, y) in occupied_spaces:
                print("█", end="")
            else:
                print(".", end="")
        print()


t = 0
robots = load_robots()
bathroom = find_bathroom_size(robots)
occupied_spaces = set()
while not there_could_be_a_tree(occupied_spaces, bathroom):
    robots, occupied_spaces = move_once(robots, bathroom)
    t += 1

visualize(occupied_spaces, bathroom)
print("Time:", t)
