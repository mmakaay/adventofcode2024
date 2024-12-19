#!/usr/bin/env python3

from part1 import load_input, execute


def forward(a, program):
    return list(execute((a, 0, 0), program))


def reverse(full_program, a=0, size=1):
    program_length = len(full_program)
    end_of_program = full_program[program_length - size : program_length]
    for i in range(8):
        a_candidate = a * 8 + i
        generated_program = forward(a_candidate, full_program)
        if generated_program == full_program:
            yield a_candidate
        elif generated_program == end_of_program:
            yield from reverse(full_program, a_candidate, size + 1)


_, program = load_input()
a_min = min(reverse(program))
print("Minimal A:", a_min)
