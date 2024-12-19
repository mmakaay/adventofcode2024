#!/usr/bin/env python3
#
# +------------------------------------------+
# | Register A: 65804993                     |
# | Register B: 0                            |
# | Register C: 0                            |
# |                                          |
# | Program: 2,4,1,1,7,5,1,4,0,3,4,5,5,5,3,0 |
# +------------------------------------------+
#
# Find minimal A, so the output equals the program itself.
#
# Translated:
#
#   BST 4   B = A % 8
#   BXL 1   B' = B ^ 1
#   CDV 5   C = A // (2 ** B')
#   BXL 4   B'' = B' ^ 4
#   ADV 3   A' = A // 8
#   BXC 5   B''' = B'' ^ C
#   OUT 5   >>> B''' % 8
#   JNZ 0   A = A' and loop
#
# Simplified into Python code:
#
#   b = 1 ^ (a % 8)
#   c = a // (2 ** b)
#   out = (b ^ 4 ^ c) % 8
#   a = a // 8
#
# Observations:
#
#   b is always in range 0 - 7, because of the first line
#   This can be used in the reversal process, since this limits
#   the number of options we have to check.
#


def forward(a):
    n = []
    while a:
        b = 1 ^ (a % 8)
        c = a // (2**b)
        out = (b ^ 4 ^ c) % 8
        a = a // 8
        n.append(out)
    return n


def reverse(full_program, a=0, size=1):
    program_length = len(full_program)
    end_of_program = full_program[program_length - size : program_length]
    for i in range(8):
        a_candidate = a * 8 + i
        generated_program = forward(a_candidate)
        if generated_program == full_program:
            yield a_candidate
        elif generated_program == end_of_program:
            yield from reverse(full_program, a_candidate, size + 1)


program = [2, 4, 1, 1, 7, 5, 1, 4, 0, 3, 4, 5, 5, 5, 3, 0]
a_min = min(reverse(program))
print("Minimal A:", a_min)
