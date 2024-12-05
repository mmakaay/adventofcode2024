#!/usr/bin/env python3

import sys
from functools import cmp_to_key


def read_page_rules():
    page_rules = {}
    for line in sys.stdin:
        if line.strip() == "":
            return page_rules
        a, b = list(map(int, line.strip().split("|")))
        page_rules[(a, b)] = True


def create_page_sort_key(page_rules):
    def cmp_page(a, b):
        return -1 if (a, b) in page_rules else 0

    return cmp_to_key(cmp_page)


def process_manuals(page_sort_key):
    for manual in all_manuals():
        sorted_manual = sorted(manual, key=page_sort_key)
        yield manual == sorted_manual, sorted_manual


def all_manuals():
    for line in sys.stdin:
        yield list(map(int, line.strip().split(",")))


def get_mid_page(manual):
    mid_page_index = int(len(manual) / 2)
    return manual[mid_page_index]


page_rules = read_page_rules()
page_sort_key = create_page_sort_key(page_rules)
total = sum(
    get_mid_page(manual)
    for is_valid_manual, manual in process_manuals(page_sort_key)
    if not is_valid_manual
)


print(total)
