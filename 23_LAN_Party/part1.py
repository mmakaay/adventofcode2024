#!/usr/bin/env python3

import sys
from collections import deque


connections = {}
for a, b in [line.strip().split("-") for line in sys.stdin]:
    connections.setdefault(a, set()).add(b)
    connections.setdefault(b, set()).add(a)

triplets = set()

for node in connections:
    # We only care about groups of computers that have at
    # least one computer that has a name starting with "t".
    # Since we're visiting all nodes as starting points for
    # searching, we can skip any node without a starting "t".
    if not node.startswith("t"):
        continue

    queue = deque()
    queue.append((node, [node]))
    while queue:
        node, path = queue.pop()
        for neighbour in connections[node]:
            # Loop of three nodes found?
            if neighbour == path[0] and len(path) == 3:
                triplets.add(tuple(sorted(path)))
                continue

            if neighbour in path:
                continue

            # Continue searching when we've not yet inspected
            # three nodes in a path.
            if len(path) < 3:
                new_path = list(path) + [neighbour]
                queue.append((neighbour, new_path))


print("Length:", len(triplets))

