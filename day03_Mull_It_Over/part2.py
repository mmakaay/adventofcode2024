#!/usr/bin/env python3

import sys


def get_multiplications(bytestream):
    state = 0
    for c in bytestream:
        match state:
            case 0:
                if c == "m":
                    state = 1
                if c == "d":
                    state = 6
            case 1:
                state = 2 if c == "u" else 0
            case 2:
                state = 3 if c == "l" else 0
            case 3:
                if c == "(":
                    state = 4
                    nr_of_digits = 0
                    x = ""
                else:
                    state = 0
            case 4:
                if c.isdigit() and nr_of_digits < 3:
                    x += c
                    nr_of_digits += 1
                elif c == "," and x != "":
                    state = 5
                    nr_of_digits = 0
                    y = ""
                else:
                    state = 0
            case 5:
                if c.isdigit() and nr_of_digits < 3:
                    y += c
                    nr_of_digits += 1
                elif c == ")" and y != "":
                    yield (int(x), int(y))
                    state = 0
                else:
                    state = 0
            case 6:
                state = 7 if c == "o" else 0
            case 7:
                state = 8 if c == "n" else 0
            case 8:
                state = 9 if c == "'" else 0
            case 9:
                state = 10 if c == "t" else 0
            case 10:
                state = 11 if c == "(" else 0
            case 11:
                state = 12 if c == ")" else 0
            case 12:
                state = 13 if c == "d" else 12
            case 13:
                state = 14 if c == "o" else 12
            case 14:
                state = 15 if c == "(" else 12
            case 15:
                state = 0 if c == ")" else 12


def bytestream_from_stdin():
    for line in sys.stdin:
        yield from line


total = 0
for x, y in get_multiplications(bytestream_from_stdin()):
    total += x * y

print("Total:", total)
