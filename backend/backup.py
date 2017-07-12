import psutil as put
import ctypes
import os
from enum import Enum


def mount(device, mntpnt, fs, options=''):
    res = ctypes.CDLL('libc.so.6', use_errno=True).mount(device, mntpnt, fs, 0, options)
    if res < 0:
        errno = ctypes.get_errno()
        raise RuntimeError("Error mounting {} ({}) on {} with options '{}': {}".
                           format(device, fs, mntpnt, options, os.strerror(errno)))


def get_fs_type_desc(type):
    for desc in Filesystem:
        if desc.name == str(type).upper():
            return desc.value
    return type


class Filesystem(Enum):
    EXT4 = "Linux EXT4"

dps = put.disk_partitions()

parts = []

fmt_str = "{:<8} {:<7}"
print(fmt_str.format("Drive", "Types"))

for part in dps:
    parts.append((part.device, get_fs_type_desc(part.fstype)))
for part in parts:
    print(fmt_str.format(part[0], part[1]))