#!/usr/bin/env python3

import re
import sys

TOKENS_FOR_A = 3
TOKENS_FOR_B = 1
UNIT_CONVERSION_OFFSET = 10_000_000_000_000


def load_machines():
    m = {"A": None, "B": None, "P": None}
    for line in sys.stdin:
        matches = re.match(r"Button ([AB]):.*\+(\d+).*\+(\d+)", line)
        if matches:
            b = matches.group(1)
            x = int(matches.group(2))
            y = int(matches.group(3))
            m[b] = (x, y)
            continue

        matches = re.match(r"Prize.*=(\d+).*=(\d+)", line)
        if matches:
            x = int(matches.group(1))
            y = int(matches.group(2))
            m["P"] = (x + UNIT_CONVERSION_OFFSET, y + UNIT_CONVERSION_OFFSET)
            yield dict(m)


def find_minimum_tokens_for_price(machine):
    Pa, Pb = find_button_presses_to_get_close_to_price(machine)
    return (
        abiding_laws_of_nature(Pa, Pb)
        and claw_is_right_on_price(machine, Pa, Pb)
        and compute_number_of_tokens(Pa, Pb)
    )


def find_button_presses_to_get_close_to_price(machine):
    """See accompanying README.md for information on how I got here."""
    Dxa, Dya = machine["A"]
    Dxb, Dyb = machine["B"]
    Xp, Yp = machine["P"]

    Da = Dya * Dxb - Dxa * Dyb
    assert Da != 0  # Edge case check, not hit by these machines.
    Pa = (Yp * Dxb - Xp * Dyb) // Da
    Pb = (Xp - Pa * Dxa) // Dxb

    return Pa, Pb


def abiding_laws_of_nature(Pa, Pb):
    """We can't do negative button presses, this isn't Bizarro world."""
    return Pa >= 0 and Pb >= 0


def claw_is_right_on_price(machine, Pa, Pb):
    """The claw only works when exactly over the price."""
    Dxa, Dya = machine["A"]
    Dxb, Dyb = machine["B"]
    Xp, Yp = machine["P"]
    Xc = Pa * Dxa + Pb * Dxb
    Yc = Pa * Dya + Pb * Dyb
    return (Xc, Yc) == (Xp, Yp)


def compute_number_of_tokens(Pa, Pb):
    return Pa * TOKENS_FOR_A + Pb * TOKENS_FOR_B


machines = load_machines()
total = 0
for machine in machines:
    total += find_minimum_tokens_for_price(machine)

print("Token:", total)

