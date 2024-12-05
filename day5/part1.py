#!/usr/bin/env python3

import sys
from collections import defaultdict


def read_page_rules():
    sort_map = defaultdict(list)
    for line in sys.stdin:
        if line.strip() == "":
            return sort_map
        a, b = list(map(int, line.strip().split("|")))
        sort_map[a].append(b)


def process_manuals(page_rules):
    for manual in all_manuals():
        yield is_valid_manual(manual, page_rules), manual


def all_manuals():
    for line in sys.stdin:
        yield list(map(int, line.strip().split(",")))


def is_valid_manual(manual, page_rules):
    seen_pages = set()
    for page in manual:
        prepending_pages = page_rules[page]
        if any(p in seen_pages for p in prepending_pages):
            return False
        seen_pages.add(page)
    return True


def get_mid_page(manual):
    mid_page_index = int(len(manual) / 2)
    return manual[mid_page_index]


page_rules = read_page_rules()
total = sum(
    get_mid_page(manual)
    for is_valid_manual, manual in process_manuals(page_rules)
    if is_valid_manual
)

print(total)
