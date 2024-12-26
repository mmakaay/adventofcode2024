#!/usr/bin/env python3
#
# I used this script to verify the wiring. The script stops at
# points where the wiring is off. At points where that happened,
# I inspected the wiring to find what was wrong. This way I was
# able to do the swaps by hand on the input, eventually finding
# the wires to swap.
#
# - input.txt contains the broken wiring.
# - input-fixed.txt contains the fixed wiring. 

import re
import sys


def load_scenario():
    registers = {}
    rules = []

    re_register = re.compile(r"^(\w\w\w): ([01])$")
    re_rule = re.compile(r"^(\w{3}) (AND|OR|XOR) (\w{3}) -> (\w{3})$")

    for line in sys.stdin:
        line = line.strip()
        if match := re_register.match(line):
            registers[match.group(1)] = int(match.group(2))
        elif line == "":
            continue
        elif match := re_rule.match(line):
            rules.append(tuple(match.groups()))
            registers[match.group(4)] = None
        else:
            raise ValueError(f"Cannot parse input: {line!r}")

    return registers, rules


def verify(rules):
    def r(i):
        return [f"{register}{i:02}" for register in "xyz"]

    def find(a, b, o):
        for in1, op, in2, out in rules:
            if in1 == a and in2 == b and op == o:
                return out
            if in1 == b and in2 == a and op == o:
                return out
        return None

    def expect_half_adder():
        i = 0
        x, y, z = r(i)
        z_out = find(x, y, "XOR")
        carry_out = find(x, y, "AND")

        if z_out != z:
            print(f"Wrong wiring detected for output {z}")
            return

        expect_full_adder(i + 1, carry_out)

    def expect_full_adder(i, carry_in):
        x, y, z = r(i)
        a = find(x, y, "XOR")
        b = find(x, y, "AND")
        z_out = find(carry_in, a, "XOR") 
        c = find(carry_in, a, "AND") 
        carry_out = find(b, c, "OR")

        if z_out != z:
            print(f"Wrong wiring detected for output {z}")
            return
        print(z_out, carry_out)

        while i < 44:
            return expect_full_adder(i + 1, carry_out)
    

    expect_half_adder()

registers, rules = load_scenario()
verify(rules)
