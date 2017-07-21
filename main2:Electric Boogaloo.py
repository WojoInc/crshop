import configparser
import os
import threading
import tkinter as tk
import tkinter.ttk
import backup


class backupApp(tk.Tk):
    def __init__(self):  # Create the window
        tk.Tk.__init__(self)
        # Variables
        self.selected_qnap = tk.IntVar()
        self.title("ITS Backup Superscript")
        # load config file
        self.load_config()
        # setup menus
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="About", command=self.show_about)
        self.qnap_menu = QnapMenu(self.cfg, self.configdir + self.configfile, self.filemenu)
        self.filemenu.add_cascade(label="Change QNAP", menu=self.qnap_menu)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.config(menu=self.menubar)

        # setup tab pages
        self.tabs = tk.ttk.Notebook(self)
        self.tab_bak = BackupTab(self, height=400, width=800, config=self.cfg)
        self.tabs.add(self.tab_bak, text="Backup")
        self.tabs.pack(expand=1, fill="both")

    def show_about(self):
        about_win = PopUpWindow(self)
        about_win.show("All config files stored in ~/.backup_superscript\n"
                       "If something is broken, please don't try to contact TJ or Mitch.\n"
                       "Thanks.\n\n"
                       "Github: https://github.com/WojoInc/crshop\n")

    def show_error(self, err_msg):
        err_win = PopUpWindow(self)
        err_win.show("              ,---------------------------,\n"
                     "              |  /---------------------\  |\n"
                     "              | |                       | |\n"
                     "              | |     REEEEEEE          | |\n"
                     "              | |      EEEEEEEE         | |\n"
                     "              | |       EEEEEEEE        | |\n"
                     "              | |                       | |\n"
                     "              |  \_____________________/  |\n"
                     "              |___________________________|\n"
                     "            ,---\_____     []     _______/------,\n"
                     "          /         /______________\           /|\n"
                     "        /___________________________________ /  | ___\n"
                     "        |                                   |   |    )\n"
                     "        |  o o o                 [-------]  |  /    _)_\n"
                     "        |__________________________________ |/     /  /\n"
                     "    /-------------------------------------/|      ( )/\n"
                     "  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /\n"
                     "/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /\n"
                     "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                     + err_msg)

    def load_config(self):
        self.cfg = configparser.ConfigParser()
        self.configdir = os.path.expanduser("~")
        self.configdir += "/.backup_superscript/"
        self.configfile = "config.ini"

        # Check for config.ini and create one if there is none
        try:
            self.cfg.read_file(open(self.configdir + self.configfile))
        except FileNotFoundError:
            self.cfg["QNAP"] = {"Current QNAP": "1",
                                "QNAP 1": "\"/media/crshop/QNAP-1/\"",
                                "QNAP 2": "\"/media/crshop/QNAP-2/\""}
            os.makedirs(self.configdir)
            with open(self.configdir + self.configfile, "w+") as filetowrite:
                self.cfg.write(filetowrite)

    def mainloop(self):
        tk.Tk.mainloop(self)
        return


class BackupTab(tk.ttk.Frame):
    def __init__(self, master=None, height=100, width=100, config=None):
        tk.ttk.Frame.__init__(self, height=height, width=width, master=master)
        self.lbl_ticket = tk.Label(self, text="Ticket #:")
        self.lbl_ticket.grid(row=0, column=0)
        self.entry_ticket = tk.Entry(self, bd=4)
        self.entry_ticket.grid(row=0, column=1)
        self.cfg = config

        # Create drop-down for drive list
        self.selected_drive = tk.StringVar(self)
        self.devices = backup.get_devices()
        self.dict_device = {}
        self.radio_sel = tk.IntVar()
        devices = backup.get_devices()
        for device in devices:  # Retrives the first part of devices from backup.py
            self.dict_device[device[0] + "    " + device[1] + "   " + str(device[2]) + " MB " + str(device[3])] = device

        self.drpdwn_drive = tk.OptionMenu(self, self.selected_drive, *self.dict_device)
        self.drpdwn_lbl = tk.Label(self, text="Select Drive:")
        self.drpdwn_lbl.grid(row=1, column=0)
        self.drpdwn_drive.grid(row=1, column=1)

        # set up radiobuttons
        self.setup_rbuttons()

        # set up start button
        self.btn_start = tk.Button(self, text="Start Backup", command=self.run_backup)
        self.btn_start.grid(row=3, column=3, padx=5, pady=15)

    def setup_rbuttons(self):
        # Radio buttons for selecting folder to backup
        self.R1 = tk.Radiobutton(self, text="Whole drive", variable=self.radio_sel, value="/")
        self.R1.grid(row=0, column=2)

        self.R2 = tk.Radiobutton(self, text="Users Folder", variable=self.radio_sel, value="/Users/")
        self.R2.grid(row=1, column=2)

        self.R3 = tk.Radiobutton(self, text="Other:", variable=self.radio_sel, value="")
        self.R3.grid(row=2, column=2)

        self.entry_other = tk.Text(self, height=1, width=35)
        self.entry_other.grid(row=2, column=3)

    def run_backup(self):
        txt_errors = tk.StringVar(self)
        threading._start_new_thread(backup.backup, ("", "", txt_errors))
        win_stats = StatusWindow(self, self.config, txt_errors)


class StatusWindow(tk.Toplevel):
    def __init__(self, cfg, txt_errors, master=None):
        tk.Toplevel.__init__(self, master)
        self.title("Running backup...")
        self.txt_errors = tk.StringVar()
        self.txt_main = tk.Text(self, textvariable=txt_errors)
        self.txt_main.pack()


class QnapMenu(tk.Menu):
    def __init__(self, config, cfg_path, master=None):
        tk.Menu.__init__(self, master)
        self.sel_qnap = tk.IntVar()
        self.config = config
        self.cfg_path = cfg_path
        self.add_radiobutton(label="QNAP_1", variable=self.sel_qnap, value=1, command=self.ch_qnap)
        self.add_radiobutton(label="QNAP_2", variable=self.sel_qnap, value=2, command=self.ch_qnap)

    def ch_qnap(self):
        self.config.set("QNAP", "current qnap", str(self.sel_qnap.get()))
        # TODO move this to a different location
        # startbackuptext.set("Start backup on QNAP-" + str(value.get()))
        with open(self.cfg_path, "w+") as filetochange:
            self.config.write(filetochange)


class PopUpWindow(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        self.lbltext = tk.StringVar()
        self.lbl_main = tk.Label(self, bg='firebrick2', textvariable=self.lbltext)
        self.lbl_main.pack()

    def show(self, err_msg=""):
        self.lbltext.set(err_msg)


myapp = backupApp()
myapp.mainloop()
