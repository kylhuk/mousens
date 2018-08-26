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

import atexit
import ctypes
import linecache
import sys

import wmi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

import constants as C
import dbhandler
import messagebox
from AddProc import Ui_dialogAddProc
from DebugGui import Ui_Dialog
from MainWindow import Ui_MainWindow

c = wmi.WMI()


class MainAppWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            load_data_into_table(self)

            self.ui.pbAdd.clicked.connect(lambda: show_add_processes_gui(self))
            self.ui.pbDebug.clicked.connect(lambda: show_debug_gui(self))
            self.ui.tableWidget.cellChanged.connect(lambda: update_db(self))
            self.ui.tableWidget.itemSelectionChanged.connect(lambda: selection_changed(self))
            self.ui.pbRemove.clicked.connect(lambda: remove_data(self))

            if C.DEBUG:
                self.ui.pbDebug.setVisible(True)
            else:
                self.ui.pbDebug.setVisible(False)

            self.show()
        except Exception as ex:
            print_exception(ex)


def remove_data(maingui):
    try:
        qtable = maingui.ui.tableWidget

        # print("length: " + str(len(qtable.selectedItems())))

        if len(qtable.selectedItems()) > 0:
            selecteditem = qtable.selectedItems()[0]
            indexes = qtable.selectedIndexes()
            currentrows = qtable.currentRow()

            print("selecteditem: " + str(selecteditem))
            print("indexes: " + str(indexes))
            print("len of indexes: " + str(len(indexes)))

            for i in range(0, len(indexes)):
                print("Remove row id: " + str(indexes[i].row()))

                qtable.removeRow(indexes[i].row())

    except Exception as ex:
        print_exception(ex)


def selection_changed(maingui):
    try:
        qtable = maingui.ui.tableWidget

        # print("length: " + str(len(qtable.selectedItems())))

        if len(qtable.selectedItems()) > 0:
            selecteditem = qtable.selectedItems()[0]
            indexes = qtable.selectedIndexes()
            currentrows = qtable.currentRow()

            # for i in range(0, len(indexes)):
                # print(indexes[i].row())

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


def update_db(maingui):
    try:
        qtable = maingui.ui.tableWidget

        processname = qtable.item(qtable.currentRow(), 0).text()
        sensitivity = int(qtable.item(qtable.currentRow(), 2).text())

        if sensitivity > 20:
            qtable.item(qtable.currentRow(), 2).setText("20")
            sensitivity = 20

        dbhandler.update_data(processname, "sens", sensitivity)

    except Exception as ex:
        print_exception(ex)


def load_data_into_table(maingui):
    try:
        qtable = maingui.ui.tableWidget

        qtable.setColumnCount(3)
        qtable.setRowCount(1)

        qtable.setHorizontalHeaderLabels(["Process Name", "Path", "Sensitivity"])

        qtable.setColumnWidth(0, 100)
        qtable.setColumnWidth(1, 300)
        qtable.setColumnWidth(2, 100)

        sqlresult = dbhandler.get_data()

        qtable.setRowCount(len(sqlresult))

        for i in range(0, len(sqlresult)):
            processname = QTableWidgetItem()
            processpath = QTableWidgetItem()
            sensitivity = QTableWidgetItem()

            processname.setText(str(sqlresult[i][0]))
            processpath.setText(str(sqlresult[i][1]))
            sensitivity.setText(str(sqlresult[i][2]))

            processname.setFlags(Qt.ItemIsEnabled)
            processpath.setFlags(Qt.ItemIsEnabled)

            qtable.setItem(i, 0, processname)
            qtable.setItem(i, 1, processpath)
            qtable.setItem(i, 2, sensitivity)

            # active.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            #
            # if sqlresult[i][3] == 1:
            #     active.setCheckState(Qt.Checked)
            # else:
            #     active.setCheckState(Qt.Unchecked)
            #
            # qtable.setItem(i, 0, active)

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

        load_data_into_table(maingui)

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
        # acceleration = ctypes.c_int()
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

        for row in range(0, 5):
            for col in range(0, 2):
                stringitem = QTableWidgetItem()

                stringitem.setText("Test r: " + str(row) + " c: " + str(col))

                qtable.setItem(row, col, stringitem)

            chkboxitem = QTableWidgetItem()
            chkboxitem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkboxitem.setCheckState(Qt.Checked)

            qtable.setItem(row, 2, chkboxitem)

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
