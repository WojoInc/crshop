from sh import mount, umount, ErrorReturnCode, mkdir
import shutil as sh
import ctypes
import os
from enum import Enum
from tkinter import *
import parted as ptd

class Filesystem(Enum):
    ext4 = "-t ext4"
    ntfs = "-t ntfs-3g"


def mount_disk(device, mntpnt, fs):
    mkdir_err = False

    try:
        umount("-f", device)
    except ErrorReturnCode as ex:
        if "not mounted" in ex.stderr.decode():
            pass

    if fs == "ntfs":
        fs = "-t ntfs-3g"

    try:
        mount(device, mntpnt, fs)
    except ErrorReturnCode as  ex:
        if "does not exist" in ex.stderr.decode():
            mkdir(mntpnt)
    if mkdir_err is False:
        try:
            mount(device, mntpnt, fs)
        except ErrorReturnCode as  ex:
            if "does not exist" in ex.stderr.decode():
                mkdir(mntpnt)

                # print(res)


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
    """
    Returns the available partitions known to the kernel
    :return: a tuple, (/dev/sdX#, fs, size, name/ if applicable) or
    returns a tuple " ", " ", " ", " " if not run as root
    """
    devices = ptd.getAllDevices()
    disks = []
    drv_info = []
    if len(devices) == 0:
        return [(" ", " ", " ", " ")]
    for device in devices:
        disks.append(ptd.Disk(device))
    for disk in disks:
        parts = disk.partitions
        for part in parts:
            drv_info.append((part.path, part.fileSystem.type, part.getSize(), part.name))
    return drv_info
    # print(mount("/dev/sda2", "/media/crshop/Test", "ntfs"))
