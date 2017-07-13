import psutil as put
import shutil as sh
import ctypes
import os
from enum import Enum
from tkinter import *


class Filesystem(Enum):
    EXT4 = "Linux EXT4"


def mount(device, mntpnt, fs, options=''):
    res = ctypes.CDLL('libc.so.6', use_errno=True).mount(device, mntpnt, fs, 0, options)
    if res < 0:
        errno = ctypes.get_errno()
        raise RuntimeError("Error mounting {} ({}) on {} with options '{}': {}".
                           format(device, fs, mntpnt, options, os.strerror(errno)))


def backup(mntpnt, backup_loc, errors):
    errorlog = ""

    def adderror(errorlog, errors):
        errors.configure(text=errorlog)
        errors.pack()

    try:
        dirs = os.listdir(mntpnt)
        if os.path.exists(backup_loc) is False:
            os.makedirs(backup_loc)
        for dir in dirs:
            srcname = os.path.join(mntpnt, dir)
            dstname = os.path.join(backup_loc, dir)

            try:
                if os.path.isdir(srcname):
                    backup(srcname, dstname, errors)
                elif os.path.isfile(srcname):
                    if os.path.exists(dstname):
                        errorlog += ("Error. File { " + dstname + " } already exists/n")
                        adderror(errorlog, errors)
                    else:
                        sh.copy2(srcname, dstname)
            except (IOError, os.error) as ex:
                errorlog += ex.strerror + "/n"
                adderror(errorlog, errors)
            except sh.Error as ex:
                errorlog += ex.strerror + "/n"
                adderror(errorlog, errors)
            try:
                sh.copystat(mntpnt, backup_loc)
            except WindowsError:
                pass
            except OSError as ex:
                errorlog += ex.strerror + "/n"
                adderror(errorlog, errors)
        else:
            errorlog += ("Error. Directory { " + backup_loc + " } already exists/n")
            adderror(errorlog, errors)
    except PermissionError as ex:
        errorlog += ("Insufficient permission to access { " + backup_loc + " }/n")
        adderror(errorlog, errors)

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
