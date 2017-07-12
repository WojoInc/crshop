import psutil
from tkinter import *
from tkinter import ttk
from backend import backup

__author__ = "Meme_master_69"

dps = psutil.disk_partitions()


def placeholder():
    pass

def changeqnap():  # TODO
    pass

def helpwindow():  # TODO
    pass


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
advmenu.add_command(label="Change QNAP", command=changeqnap())
advmenu.add_command(label="About", command=helpwindow())
menubar.add_cascade(label="Advanced", menu=advmenu)

mainwindow.config(menu=menubar)  # Packs the menubar


tabs = ttk.Notebook(mainwindow)  # Create tabs for different options
backuptab = ttk.Frame(tabs, height=400, width=800)  # Tab with options for backup
# TODO add widgets for backup
# Create entry for ticket number
ticketlabel = Label(backuptab, text="Ticket #:")
ticketlabel.grid(row=0, column=0)
ticketentry = Entry(backuptab, bd=4)
ticketentry.grid(row=0, column=1)

# Create drop-down for drive list
driveoptions = StringVar(backuptab)
tempoptions = {"This", "are", "some", "options"}
devices = backup.get_devices()
devicelist = []
for device in devices:  # Retrives the first part of devices from backup.py
    devicelist.append(device[0])

driveentry = OptionMenu(backuptab, driveoptions, *devicelist)
drivelabel = Label(backuptab, text="Select Drive:")
drivelabel.grid(row=0, column=2)
driveentry.grid(row=0, column=3)

startbutton = Button(backuptab, text="Start Backup", command=placeholder())
startbutton.grid(row=1, column=1)


restoretab = ttk.Frame(tabs, height=400, width=800)  # Tab with options for restoring
# TODO add widgets for restore
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

tabs.add(backuptab, text="Backup")
tabs.add(restoretab, text="Restore")

tabs.pack(expand=1, fill="both")

mainwindow.mainloop()
