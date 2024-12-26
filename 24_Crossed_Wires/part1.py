#!/usr/bin/env python3

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


def run_simulation(registers, rules):
    def cycle():
        for in1, op, in2, out in rules:
            if registers[in1] is None or registers[in2] is None:
                continue
            if op == "AND":
                registers[out] = registers[in1] & registers[in2]
            elif op == "OR":
                registers[out] = registers[in1] | registers[in2]
            elif op == "XOR":
                registers[out] = registers[in1] ^ registers[in2]

    while any(value is None for value in registers.values()):
        cycle()


def get_z_register_number(registers):
    def z_registers():
        z = 0
        while True:
            name = f"z{z:02}"
            if name not in registers:
                return
            yield (f"z{z:02}")
            z += 1

    number = 0
    bit = 1
    for z_register in z_registers():
        number |= bit * registers[z_register]
        bit <<= 1

    return number


registers, rules = load_scenario()
run_simulation(registers, rules)
number = get_z_register_number(registers)

print("Z-register number:", number)
