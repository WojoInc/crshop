__author__ = "Meme_master_69"

import psutil
from tkinter import *
from tkinter import ttk

dps = psutil.disk_partitions()


def placeholder():  # TODO
    pass


def close(val=False):
    if val is True:
        exit(0)


mainwindow = Tk()   # The main window for the program options to run in
mainwindow.title("ITS Backup superscript")
menubar = Menu(mainwindow)  # Space for the drop-down file menu from the top

# "File" cascade menu
filemenu = Menu(menubar, tearoff=0)  # Actual drop-down file menu
filemenu.add_command(label="Placeholder", command=placeholder())  # TODO actually add commands
filemenu.add_separator()    # adds a separator, you dingus
filemenu.add_command(label="other placeholder", command=placeholder())
menubar.add_cascade(label="File", menu=filemenu)

# "Advanced" cascade menu
advmenu = Menu(menubar, tearoff=0)
advmenu.add_command(label="Placeholder", command=placeholder())
menubar.add_cascade(label="Advanced", menu=advmenu)

mainwindow.config(menu=menubar)  # Packs the menubar

tabs = ttk.Notebook(mainwindow)  # Create tabs for different options
backuptab = ttk.Frame(tabs, height=400, width=800)
# TODO add widgets for backup
ticketlabel = Label(backuptab, text="Ticket #:")
ticketlabel.pack(side=LEFT)
ticketentry = Entry(backuptab, bd=4)
ticketentry.pack(side=LEFT, fill="x")

restoretab = ttk.Frame(tabs, height=400, width=800)
# TODO add widgets for restore


tabs.add(backuptab, text="Backup")
tabs.add(restoretab, text="Restore")

tabs.pack(expand=1, fill="both")

mainwindow.mainloop()
