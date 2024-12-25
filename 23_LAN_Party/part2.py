#!/usr/bin/env python3

import sys
from collections import deque


def load_connections():
    connections = {}
    for a, b in [line.strip().split("-") for line in sys.stdin]:
        connections.setdefault(a, set()).add(b)
        connections.setdefault(b, set()).add(a)
    return connections


def find_biggest_party(connections):
    biggest_party = tuple()
    seen = set()

    for node in connections:
        queue = deque([(node, {node})])
        while queue:
            node, party = queue.pop()

            if node in seen:
                continue
            seen.add(node)

            for neighbour in connections[node]:
                # The neighbour is only part of the party when it is
                # connected to all the existing nodes in the party.
                if not all(neighbour in connections[node] for node in party):
                    continue

                # Keep track of the biggest party.
                new_party = party | {neighbour}
                if len(new_party) > len(biggest_party):
                    biggest_party = new_party
                queue.append((neighbour, new_party))

    return biggest_party


def create_password(party):
    return ",".join(sorted(party))


connections = load_connections()
biggest_party = find_biggest_party(connections)
password = create_password(biggest_party)

print("LAN party password:", password)
