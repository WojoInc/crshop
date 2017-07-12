import psutil as put
import shutil as sh
import ctypes
import os
from os.path import getsize, join
from enum import Enum


class Filesystem(Enum):
    EXT4 = "Linux EXT4"


def mount(device, mntpnt, fs, options=''):
    res = ctypes.CDLL('libc.so.6', use_errno=True).mount(device, mntpnt, fs, 0, options)
    if res < 0:
        errno = ctypes.get_errno()
        raise RuntimeError("Error mounting {} ({}) on {} with options '{}': {}".
                           format(device, fs, mntpnt, options, os.strerror(errno)))


def backup(mntpnt, backup_loc):
    sh.copytree(mntpnt, backup_loc)


def get_fs_type_desc(type):
    for desc in Filesystem:
        if desc.name == str(type).upper():
            return desc.value
    return type


def get_devices():
    dps = put.disk_partitions()

    parts = []
    for part in dps:
        parts.append(('' + part.device + ": " + get_fs_type_desc(part.fstype), (part.device, part.fstype)))
    return parts