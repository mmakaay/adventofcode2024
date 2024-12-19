#!/usr/bin/env python3

import sys
import re

A = 0
B = 1
C = 2


def load_input():
    reg = []
    for line in sys.stdin:
        if match := re.match(r"^Register [ABC]: (\d+)", line):
            reg.append(int(match.group(1)))
        elif match := re.match(r"^Program: ([\d,]+)", line):
            program = list(map(int, match.group(1).split(",")))
    return tuple(reg), program


def execute(reg, program):
    state = (reg, program, ptr := 0)
    while ptr < len(program):
        opcode = program[ptr]
        match opcode:
            case 0:
                state = adv(state)
            case 1:
                state = bxl(state)
            case 2:
                state = bst(state)
            case 3:
                state = jnz(state)
            case 4:
                state = bxc(state)
            case 5:
                state = yield from out(state)
            case 6:
                state = bdv(state)
            case 7:
                state = cdv(state)
            case _:
                raise NotImplementedError
        reg, program, ptr = state


def div(state, to_register):
    reg, program, ptr = state
    numerator = reg[A]
    operand = get_combo_operand(state)
    denominator = 2**operand
    result = numerator // denominator
    r = list(reg)
    r[to_register] = result
    return tuple(r), program, ptr + 2


def adv(state):
    return div(state, A)


def bdv(state):
    return div(state, B)


def cdv(state):
    return div(state, C)


def bxl(state):
    reg, program, ptr = state
    result = reg[B] ^ get_literal_operand(state)
    return (reg[A], result, reg[C]), program, ptr + 2


def bst(state):
    reg, program, ptr = state
    result = get_combo_operand(state) % 8
    return (reg[A], result, reg[C]), program, ptr + 2


def jnz(state):
    reg, program, ptr = state
    if reg[A] == 0:
        return reg, program, ptr + 2
    return reg, program, get_literal_operand(state)


def bxc(state):
    reg, program, ptr = state
    result = reg[B] ^ reg[C]
    return (reg[A], result, reg[C]), program, ptr + 2


def out(state):
    reg, program, ptr = state
    result = get_combo_operand(state) % 8
    yield result
    return reg, program, ptr + 2


def get_literal_operand(state):
    reg, program, ptr = state
    return program[ptr + 1]


def get_combo_operand(state):
    reg, program, ptr = state
    value = program[ptr + 1]
    if value <= 3:
        return value
    return reg[value - 4]


if __name__ == "__main__":
    reg, program = load_input()
    results = execute(reg, program)
    print(",".join(map(str, results)))
