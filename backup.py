import psutil as put
import shutil as sh
import ctypes
import os
from enum import Enum
from tkinter import *
import parted as ptd

class Filesystem(Enum):
    EXT4 = "Linux EXT4"


def mount(device, mntpnt, fs, options=''):
    res = ctypes.CDLL('libc.so.6', use_errno=True).mount(device, mntpnt, fs, 0, options)
    if res < 0:
        errno = ctypes.get_errno()
        raise RuntimeError("Error mounting {} ({}) on {} with options '{}': {}".
                           format(device, fs, mntpnt, options, os.strerror(errno)))


def backup(mntpnt, backup_loc, errors):
    # TODO prevent overwriting over existing root folder
    errorlog = ""

    def adderror(error, errors):
        errors.insert(INSERT, error + "\n")
        errors.pack()

    try:
        dirs = os.listdir(mntpnt)
        if os.path.exists(backup_loc) is False:
            os.makedirs(backup_loc)
        else:
            adderror("Error. Directory { " + backup_loc + " } already exists", errors)
        for dir in dirs:
            srcname = os.path.join(mntpnt, dir)
            dstname = os.path.join(backup_loc, dir)

            try:
                if os.path.isdir(srcname):
                    backup(srcname, dstname, errors)
                elif os.path.isfile(srcname):
                    if os.path.exists(dstname):
                        adderror("Error. File { " + dstname + " } already exists", errors)
                    else:
                        sh.copy2(srcname, dstname)
            except (IOError, os.error) as ex:
                adderror("Insufficient permission to access { " + dstname + " }", errors)
            except sh.Error as ex:
                adderror(ex.strerror + "When will you learn?", errors)
            try:
                sh.copystat(mntpnt, backup_loc)
            except WindowsError:
                pass
            except OSError as ex:
                adderror(ex.strerror, errors)

    except PermissionError as ex:

        adderror("Insufficient permission to access { " + backup_loc + " }", errors)

def get_fs_type_desc(type):
    for desc in Filesystem:
        if desc.name == str(type).upper():
            return desc.value
    return type


def get_devices():
    devices = ptd.getAllDevices()
    disks = []
    parts = []
    drv_info = []
    if len(devices) == 0:
        return " ", " ", " "
    for device in devices:
        disks.append(ptd.Disk(device))
    for disk in disks:
        parts = disk.partitions
    for part in parts:
        drv_info.append((part.path, part.type, part.name))
    return drv_info
