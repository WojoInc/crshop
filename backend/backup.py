import psutil as put
import shutil as sh
import ctypes
import os
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
    # sh.copytree(mntpnt, backup_loc)
    dirs = os.listdir(mntpnt)
    if os.path.exists(backup_loc) is False:
        os.makedirs(backup_loc)
    for dir in dirs:
        srcname = os.path.join(mntpnt, dir)
        dstname = os.path.join(backup_loc, dir)

        try:
            if os.path.isdir(srcname):
                backup(srcname, dstname)
            elif os.path.isfile(srcname):
                if os.path.exists(dstname):
                    print("Error. File { " + dstname + " } already exists")
                else:
                    sh.copy2(srcname, dstname)
        except (IOError, os.error) as ex:
            # TODO add function to update error window
            print(ex)
        except sh.Error as ex:
            # TODO add function to update error window
            print(ex)
        try:
            sh.copystat(mntpnt, backup_loc)
        except WindowsError:
            pass
        except OSError as ex:
            # TODO add function to update error window
            print(ex)
    else:
        print("Error. Directory { " + backup_loc + " } already exists")



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


print(backup("/root/Test1/", "/root/Test2/"))

