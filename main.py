import configparser
import os
import threading
from tkinter import *
from tkinter import ttk
import backup
from subprocess import call
__author__ = "Meme_master_69"

config = configparser.ConfigParser()
configdir = os.path.expanduser("~")
configdir += "/.backup_superscript/"
configfile = "config.ini"


def placeholder():  # Delte this
    pass


def runbackup(device, fs, src_path, backup_loc=None):
    # backup.mount(device, "/mnt/"+"source", fs)
    ticketnumber = ticketentry.get()
    qnappath = config["QNAP"]["qnap " + str(selected_qnap.get())]
    window = Toplevel()
    window.title("Info")
    global errorlog
    errorlog = ""
    errors = Text(window, errorlog, height=36, width=100, state=NORMAL)
    errors.pack()

    threading._start_new_thread(backup.backup, (src_path, qnappath +
                                                ticketnumber, errors))


def runrestore():
    pass


def helpwindow():  # TODO
    pass


def setdevice(value):
    selected_device = value


def changeQNAP(value):
    config.set("QNAP", "current qnap", str(value.get()))
    print(value.get())
    with open(configdir + configfile, "w+") as filetochange:
        config.write(filetochange)


# Check for config.ini and create one if there is none
try:
    config.read_file(open(configdir + configfile))
except FileNotFoundError:
    config["QNAP"] = {"Current QNAP": "1",
                      "QNAP 1": "\"/media/crshop/QNAP-1/\"",
                      "QNAP 2": "\"/media/crshop/QNAP-2/\""}
    os.makedirs(configdir)
    with open(configdir + configfile, "w+") as filetowrite:
        config.write(filetowrite)

# Create the window
mainwindow = Tk()   # The main window for the program options to run in
mainwindow.title("ITS Backup Superscript")
menubar = Menu(mainwindow)  # Space for the drop-down file menu from the top

# "File" cascade menu
filemenu = Menu(menubar, tearoff=0)  # Actual drop-down file menu
filemenu.add_command(label="Placeholder", command=placeholder())  # TODO actually add commands
filemenu.add_separator()    # adds a separator, you dingus
filemenu.add_command(label="other placeholder", command=placeholder())
menubar.add_cascade(label="File", menu=filemenu)

# "Advanced" cascade menu
advmenu = Menu(menubar, tearoff=0)
advmenu.add_command(label="About", command=helpwindow())

# Qnap radio buttons inside the advanced menu
selected_qnap = IntVar()  # stores and pulls last used QNAP
print(config["QNAP"]["current qnap"])
selected_qnap.set(int(config["QNAP"]["current qnap"]))

qnapmenu = Menu(advmenu, tearoff=0)
qnapmenu.add_radiobutton(label="QNAP_1", variable=selected_qnap, value=1, command=lambda: changeQNAP(selected_qnap))
qnapmenu.add_radiobutton(label="QNAP_2", variable=selected_qnap, value=2, command=lambda: changeQNAP(selected_qnap))
advmenu.add_cascade(label="Change QNAP", menu=qnapmenu)
menubar.add_cascade(label="Advanced", menu=advmenu)


mainwindow.config(menu=menubar)  # Packs the menubar


tabs = ttk.Notebook(mainwindow)  # Create tabs for different options
backuptab = ttk.Frame(tabs, height=400, width=800)  # Tab with options for backup

# Create entry for ticket number
ticketlabel = Label(backuptab, text="Ticket #:")
ticketlabel.grid(row=0, column=0)
ticketentry = Entry(backuptab, bd=4)
ticketentry.grid(row=0, column=1)

selected_device = ()
radio_sel = StringVar(backuptab)


# Create drop-down for drive list
driveoptions = StringVar(backuptab)
devices = backup.get_devices()
devicedict = {}

for device in devices:  # Retrives the first part of devices from backup.py
    devicedict[device[0]] = device
    # devicedict[device[0] + " " + str(device[1]) + " " + str(device[2])] = device


def drive_select(value):
    print(devicedict[value])
    global selected_device
    selected_device = devicedict[value]


driveentry = OptionMenu(backuptab, driveoptions, *devicedict, command=drive_select)
drivelabel = Label(backuptab, text="Select Drive:")
drivelabel.grid(row=1, column=0)
driveentry.grid(row=1, column=1)

# Radio buttons for selecting folder to

R1 = Radiobutton(backuptab, text="Whole drive", variable=radio_sel, value="/")
R1.grid(row=0, column=2)

R2 = Radiobutton(backuptab, text="Users Folder", variable=radio_sel, value="/Users/")
R2.grid(row=1, column=2)

R3 = Radiobutton(backuptab, text="Other:", variable=radio_sel, value="")  # TODO add other text box
R3.grid(row=2, column=2)

otherentry = Text(backuptab, height=1, width=35)
otherentry.grid(row=2, column=3)

startbutton = Button(backuptab, text="Start Backup on QNAP-" + str(selected_qnap.get()), command=lambda:
runbackup(selected_device[1], selected_device[2], radio_sel.get()))

startbutton.grid(row=5, column=3, padx=5, pady=15)


restoretab = ttk.Frame(tabs, height=400, width=800)  # Tab with options for restoring
# Create entry for ticket number
ticketlabel = Label(restoretab, text="Ticket #:")
ticketlabel.grid(row=0, column=0)
ticketentry = Entry(restoretab, bd=4)
ticketentry.grid(row=0, column=1)

# Create drop-down for drive list
driveoptions = StringVar(backuptab)
devices = backup.get_devices()
devicelist = []
for device in devices:  # Retrives the first part of devices from backup.py
    devicelist.append(device[0])

driveentry = OptionMenu(restoretab, driveoptions, *devicelist)
drivelabel = Label(restoretab, text="Select Drive:")
drivelabel.grid(row=0, column=2)
driveentry.grid(row=0, column=3)

startbutton = Button(restoretab, text="Start Restore", command=lambda: runrestore())
startbutton.grid(row=1, column=1)

tabs.add(backuptab, text="Backup")
tabs.add(restoretab, text="Restore")

tabs.pack(expand=1, fill="both")

mainwindow.mainloop()
