# /==============================================.=====================================================================\
# |  Filename:  main.py                          |   Created at:  2018-08-01                                           |
# |----------------------------------------------'---------------------------------------------------------------------|
# |  Project:        mousens                                                                                           |
# |  Author:         https://github.com/kylhuk                                                                         |
# |  Last updated:   August 2018                                                                                       |
# |  License:        GNU GPLv3                                                                                         |
# |                                                                                                                    |
# \====================================================================================================================/

# TODO: update database on every interaction

import fnmatch

import wmi
import ctypes
import atexit

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt

from MainWindow import Ui_MainWindow
from AddProc import Ui_dialogAddProc
from DebugGui import Ui_Dialog
import sys
import messagebox
import linecache
import dbhandler
import constants as C

c = wmi.WMI()


class MainAppWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            # self.ui.createDB.clicked.connect(create_default_db_structure)
            # self.ui.dropDB.clicked.connect(drop_db)
            # self.ui.pushButton.pressed.connect(lambda: table_loader(self.ui.tableWidget))
            self.ui.pushButton.clicked.connect(lambda: show_add_processes_gui(self))
            self.ui.pbDebug.clicked.connect(lambda: show_debug_gui(self))

            load_data_into_table(self)

            if C.DEBUG:
                self.ui.pbDebug.setVisible(True)
            else:
                self.ui.pbDebug.setVisible(False)

            self.show()
        except Exception as ex:
            print_exception(ex)


class AddProc(QDialog):
    def __init__(self, parent=None):
        try:
            super(AddProc, self).__init__(parent=parent)
            self.ui = Ui_dialogAddProc()
            self.ui.setupUi(self)

            self.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(lambda: close_add_processes_gui(self))

        except Exception as ex:
            print_exception(ex)


class DebugGui(QDialog):
    def __init__(self, parent=None):
        try:
            super(DebugGui, self).__init__(parent=parent)
            self.ui = Ui_Dialog()
            self.ui.setupUi(self)

        except Exception as ex:
            print_exception(ex)


def load_data_into_table(maingui):
    try:
        qtable = maingui.ui.tableWidget

        qtable.setColumnCount(4)
        qtable.setRowCount(2)   # TODO: SELECT Query to get COUNT of Processes

        qtable.setHorizontalHeaderLabels(["Active", "Process Name", "Path", "Sensitivity"])

        qtable.setColumnWidth(0, 20)
        qtable.setColumnWidth(1, 100)
        qtable.setColumnWidth(2, 500)
        qtable.setColumnWidth(3, 100)

        # TODO: On inactive, set row font to gray


    except Exception as ex:
        print_exception(ex)


def show_debug_gui(maingui):
    maingui.dialogDebugGui = DebugGui()

    maingui.dialogDebugGui.exec_()


def save_process_data(data):
    """

    :param data:
    :return:
    """
    print("add_items_to_settings_table")
    dbhandler.save_data_to_db(data)


def close_add_processes_gui(maingui):
    """

    :param maingui:
    :return:
    """
    try:
        qtable = maingui.ui.tableProc
        processes = []

        for i in range(0, qtable.rowCount()):
            chkboxitem = qtable.item(i, 0)

            if chkboxitem.checkState() == 2:
                print(qtable.item(i, 1).text())
                processes.append((qtable.item(i, 1).text(), qtable.item(i, 2).text(), 10, 1))

                dbhandler.save_data_to_db(processes)

    except Exception as ex:
        print_exception(ex)


def show_add_processes_gui(maingui):
    """

    :param maingui:
    :return:
    """
    try:

        maingui.dialogAddProc = AddProc()

        qtable = maingui.dialogAddProc.ui.tableProc

        process_list = list(filter(None, set(get_process_list().split("\n"))))

        num_processes = len(process_list)

        qtable.setColumnCount(3)
        qtable.setRowCount(num_processes)

        qtable.setHorizontalHeaderLabels(["Add", "Process Name", "Path"])

        qtable.setColumnWidth(0, 20)
        qtable.setColumnWidth(1, 100)
        qtable.setColumnWidth(2, 500)

        for r in range(0, num_processes):
            processname = QTableWidgetItem()
            processpath = QTableWidgetItem()

            processname.setText(str(process_list[r]).split(" | ")[0])
            processpath.setText(str(process_list[r]).split(" | ")[1])

            qtable.setItem(r, 1, processname)
            qtable.setItem(r, 2, processpath)

            chkboxitem = QTableWidgetItem()
            chkboxitem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkboxitem.setTextAlignment(Qt.AlignRight)
            chkboxitem.setCheckState(Qt.Unchecked)

            qtable.setItem(r, 0, chkboxitem)

        maingui.dialogAddProc.exec_()

    except Exception as ex:
        print_exception(ex)


def change_speed(speed):
    """

    :param speed:
    :return:
    """
    try:
        #   1 - slow
        #   10 - standard
        #   20 - fast
        set_mouse_speed = 113  # 0x0071 for SPI_SETMOUSESPEED
        ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0)
        print("CHANGING SPEED to: " + str(speed))
    except Exception as ex:
        print_exception(ex)


def get_current_speed():
    """
    Queries the Windows operating system for the current mouse speed settings
    :return:
    """
    try:
        get_mouse_speed = 112  # 0x0070 for SPI_GETMOUSESPEED
        speed = ctypes.c_int()
        acceleration = ctypes.c_int()
        ctypes.windll.user32.SystemParametersInfoA(get_mouse_speed, 0, ctypes.byref(speed), 0)
        print("GET CURRENT SPEED: " + str(speed.value))
        return speed.value
    except Exception as ex:
        print_exception(ex)


def proper_close():
    """
    Closes the application gracefully and resetting changed Windows settings
    :return: None
    """
    try:
        change_speed(standard_speed)
        print("PROGRAMM BEENDET")
    except Exception as ex:
        print_exception(ex)


def get_process_list():
    """
    Queries the WMI to get all the running processes w/o those containing "Windows" inside the path
    :return: list
    """
    try:
        sql_query = """SELECT Name, ExecutablePath FROM Win32_Process WHERE ExecutablePath IS NOT NULL 
                        AND NOT ExecutablePath LIKE '%Windows%'"""
        exe = ""
        for p in c.query(sql_query):
            exe += p.Name + " | " + p.ExecutablePath + "\n"

        # print("\n".join(sorted(set(exe.split("\n")))))
        return "\n".join(sorted(set(exe.split("\n"))))
    except Exception as ex:
        print_exception(ex)


def table_loader(qtable):
    """
    Responsible for loading data into the QTableWidget
    :param qtable: QTableWidget
    :return: None
    """
    try:

        qtable.setColumnCount(3)
        qtable.setRowCount(5)

        for r in range(0, 5):
            for c in range(0, 2):
                stringitem = QTableWidgetItem()

                stringitem.setText("Test r: " + str(r) + " c: " + str(c))

                qtable.setItem(r, c, stringitem)

            chkboxitem = QTableWidgetItem()
            chkboxitem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkboxitem.setCheckState(Qt.Checked)

            qtable.setItem(r, 2, chkboxitem)

    except Exception as ex:
        print_exception(ex)


def print_exception(ex):
    """
    Gathers all the necessary debug information and generates a MsgBox
    :param ex: The exception object
    :type ex: Exception
    :return: None
    """
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    messagebox.MsgBox('EXCEPTION \'' + type(ex).__name__ + '\' IN ({}, LINE {} "{}"): {}'.format(filename,
                                                                                                 lineno,
                                                                                                 line.strip(),
                                                                                                 exc_obj),
                      style=(messagebox.MB_ICONERROR | messagebox.MB_TASKMODAL | messagebox.MB_OK), title="Exception")


if __name__ == "__main__":
    """
    Main routine
    """
    standard_speed = get_current_speed()
    print("CURRENT SPEED: " + str(get_current_speed()))

    atexit.register(proper_close)

    # get_process_list()

    app = QApplication(sys.argv)
    w = MainAppWindow()
    w.show()
    sys.exit(app.exec_())

# while True:
#     _, pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
#     for p in c.query('SELECT ExecutablePath FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
#         exe = p.ExecutablePath
#         print(exe)
#     if exe == "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2018.2\\bin\\pycharm64.exe":
#         change_speed(20)
#     else:
#         change_speed(standard_speed)
#
#     time.sleep(1)
