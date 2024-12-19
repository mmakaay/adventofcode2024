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
    if disk_map[-1][1] is None:
        del disk_map[-1]
    for i_free, sz_free in get_first_free_space(disk_map):
        i_data, sz_data, file_id = get_last_data_block(disk_map)
        if sz_data < sz_free:
            del disk_map[i_data]
            disk_map[i_free] = (sz_free - sz_data, None)
            disk_map.insert(i_free, (sz_data, file_id))
        elif sz_data == sz_free:
            del disk_map[i_data]
            disk_map[i_free] = (sz_data, file_id)
        else:
            disk_map[i_data] = (sz_data - sz_free, file_id)
            disk_map[i_free] = (sz_free, file_id)


def get_first_free_space(disk_map):
    while True:
        try:
            yield next(
                (i, size)
                for i, (size, file_id) in enumerate(disk_map)
                if file_id is None and size
            )
        except StopIteration:
            return


def get_last_data_block(disk_map):
    return next(
        (len(disk_map) - 1 - i, size, file_id)
        for i, (size, file_id) in enumerate(reversed(disk_map))
        if file_id is not None
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
