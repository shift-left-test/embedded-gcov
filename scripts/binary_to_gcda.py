#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Copyright (c) 2023 LG Electronics Inc.
SPDX-License-Identifier: MIT
"""

import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        prog='binary_to_gcda',
        description='convert binary file to gcda files')
    parser.add_argument('binaryfile', help='Path to binary file')

    args = parser.parse_args()

    end_mark = b"Gcov End\0"
    buf_size = 1000

    file_size = os.path.getsize(args.binaryfile)

    with open(args.binaryfile, "rb") as binary_file:
        gcda_list = []
        while True:
            filename = b""
            while not filename.endswith(b"\0"):
                byte = binary_file.read(1)
                if byte == b"":
                    raise ValueError("Cannot find \\0.")
                filename += byte

            if binary_file.tell() == file_size:
                if filename != end_mark:
                    raise ValueError("Cannot find end_mark.")
                break

            try:
                filename = filename[:-1].decode("utf-8")
            except UnicodeDecodeError as ude:
                raise ValueError("Cannot decode filename.") from ude

            gcda_size_byte = binary_file.read(4)
            if len(gcda_size_byte) != 4:
                raise ValueError("Cannot read size of gcda.")
            gcda_size = int.from_bytes(gcda_size_byte,
                                       byteorder="big", signed=False)

            cur_idx = binary_file.tell()
            new_idx = binary_file.seek(cur_idx + gcda_size, os.SEEK_SET)
            if cur_idx + gcda_size != new_idx:
                raise ValueError("Cannot read gcda({}bytes)."
                                 .format(gcda_size_byte))

            gcda_list.append((filename, cur_idx, gcda_size))

        for gcda_info in gcda_list:
            binary_file.seek(gcda_info[1], os.SEEK_SET)
            remain_byte = gcda_info[2]

            gcda_path = gcda_info[0]

            gcda_dir = os.path.dirname(gcda_path)
            if not os.path.isdir(gcda_dir):
                print("Skip writing {}. Directory doesn't exist".
                      format(gcda_path))
                continue

            with open(gcda_path, "wb") as gcda_file:
                while remain_byte > 0:
                    gcda = binary_file.read(min(remain_byte, buf_size))
                    gcda_file.write(gcda)
                    remain_byte -= len(gcda)
                print("Write gcda to {}".format(gcda_path))


if __name__ == "__main__":
    main()
