#!/usr/bin/env python3

import sys
import sys
from heapq import heappush, heappop


def load_warzone():
    impacts = [
        tuple(map(int, line.strip().split(",")))
        for line in sys.stdin
    ]
    width = max(x for x, _ in impacts) + 1
    height = max(y for _, y in impacts) + 1
    return width, height, impacts


def plan_safe_route(warzone, start, end, number_of_impacts):
    width, height, impacts = warzone
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    queue = []
    costs = {}

    def is_impact_zone(x, y, number_of_impacts):
        return (x, y) in impacts[:number_of_impacts]

    def enqueue(cost, state):
        if state not in costs or cost < costs[state]:
            costs[state] = cost
            heappush(queue, (cost, state))

    costs[start] = 0
    heappush(queue, (0, start))

    while queue:
        cost, (x, y) = heappop(queue)

        if (x, y) == end:
            return cost

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0<=new_x<width and 0<=new_y<height:
                if not is_impact_zone(new_x, new_y, number_of_impacts):
                    enqueue(cost + 1, (new_x, new_y))
    return None


warzone = width, height, impacts = load_warzone()
start = (0, 0)
end = (width - 1, height - 1)

lower = 0
upper = len(impacts)
last_attempt = None
while True:
    attempt = lower + (upper - lower) // 2
    if attempt == last_attempt:
        print("First blocking impact:", impacts[upper-1])
        break
    last_attempt = attempt
    if plan_safe_route(warzone, start, end, attempt):
        lower = attempt
    else:
        upper = attempt

