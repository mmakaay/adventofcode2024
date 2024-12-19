#!/usr/bin/env python3

import sys


def load_disk_map():
    disk_map = []
    line = next(sys.stdin).strip()
    for i, c in enumerate(map(int, line)):
        file_id = i // 2
        data = None if i % 2 else file_id
        if c:
            disk_map.append((c, data))
    return disk_map


def compact_disk_map(disk_map):
    for i_data, sz_data, file_id in all_data_blocks_high_to_low(disk_map):
        try:
            i_free, sz_free = find_free_space_fitting(sz_data)
            if i_free > i_data:
                pass
            elif sz_data == sz_free:
                disk_map[i_free] = (sz_data, file_id)
                disk_map[i_data] = (sz_data, None)
            elif sz_data < sz_free:
                disk_map[i_data] = (sz_data, None)
                disk_map[i_free] = (sz_free - sz_data, None)
                disk_map.insert(i_free, (sz_data, file_id))
        except StopIteration:
            pass


def all_data_blocks_high_to_low(disk_map):
    for size, file_id in list(reversed(disk_map)):
        if file_id is not None:
            yield next((i, s, f) for i, (s, f) in enumerate(disk_map) if f == file_id)


def find_free_space_fitting(requested_size):
    return next(
        (i, size)
        for i, (size, file_id) in enumerate(disk_map)
        if file_id is None and size >= requested_size
    )


def compute_disk_checksum(disk_map):
    def stream_files():
        for size, file_id in disk_map:
            for _ in range(size):
                yield file_id

    return sum(
        i * file_id for i, file_id in enumerate(stream_files()) if file_id is not None
    )


disk_map = load_disk_map()
compact_disk_map(disk_map)
disk_checksum = compute_disk_checksum(disk_map)

print("Disk checksum:", disk_checksum)
