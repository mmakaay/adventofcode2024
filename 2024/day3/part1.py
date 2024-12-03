#!/usr/bin/env python3

import sys


def get_instructions(line):
    state = 0
    for c in line:
        match state:
            case 0:
                if c == "m":
                    state = 1
            case 1:
                state = 2 if c == "u" else 0
            case 2:
                state = 3 if c == "l" else 0
            case 3:
                if c == "(":
                    state = 4
                    number_of_digits = 0
                    x = ""
                else:
                    state = 0
            case 4:
                if c.isdigit() and number_of_digits < 3:
                    x += c
                    number_of_digits += 1
                elif c == "," and x != "":
                    state = 5
                    number_of_digits = 0
                    y = ""
                else:
                    state = 0
            case 5:
                if c.isdigit() and number_of_digits < 3:
                    y += c
                    number_of_digits += 1
                elif c == ")" and y != "":
                    yield ("mul", int(x), int(y))
                    state = 0
                else:
                    state = 0


total = 0
for line in sys.stdin:
    for instruction, x, y in get_instructions(line):
        total += x * y

print("Total:", total)
