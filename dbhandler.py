import linecache
import sqlite3
import os
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import ctypes
from DebugGui import Ui_Dialog
import sys
import messagebox

DB_FILE_NAME = 'settings.db'


class AppWindow(QDialog):
    def __init__(self):
        try:
            super().__init__()
            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
            self.show()
            self.ui.createDB.clicked.connect(create_default_db_structure)
            self.ui.dropDB.clicked.connect(drop_db)
        except Exception as ex:
            print_exception(ex)


def open_connection():
    try:
        connection = sqlite3.connect(DB_FILE_NAME)
        connection.isolation_level = None
        return connection
    except Exception as ex:
        print_exception(ex)


def create_default_db_structure():
    try:
        connection = open_connection()
        c = connection.cursor()

        c.execute('''
        CREATE TABLE settings
                 (processname text, path text, sens int, active int)
        ''')

        connection.commit()

        connection.close()

        messagebox.MsgBox("Database " + DB_FILE_NAME + " was created successfully.", title="Success")

    except sqlite3.OperationalError:
        messagebox.MsgBox("Database " + DB_FILE_NAME + " already exists!", style=(
                messagebox.MB_ICONWARNING | messagebox.MB_OK), title="Warning")
    except Exception as ex:
        print_exception(ex)


def drop_db():
    try:
        os.remove(DB_FILE_NAME)

        messagebox.MsgBox("Database " + DB_FILE_NAME + " was removed successfully.", title="Success")
    except FileNotFoundError:
        messagebox.MsgBox("The file " + DB_FILE_NAME + " was not found. Was it removed already?", style=(
                messagebox.MB_ICONWARNING | messagebox.MB_OK), title="Warning")
    except Exception as ex:
        print_exception(ex)


def save_data_to_db(data):
    try:
        print("save_data_to_db")
        listsize = len(data)

        connection = open_connection()
        c = connection.cursor()

        for i in range(0, listsize):
            #sqlquery = "SELECT * FROM settings WHERE processname = \"" + data[i] + "\""
            sqlquery = '''SELECT COUNT(processname) AS processname FROM settings WHERE processname = "firefox.exe"'''

            print("SQLQUERY: " + sqlquery)

            print("iteration: " + str(i))

            c.execute(sqlquery)
            connection.commit()

            result = c.fetchall()
            processcount = result[0][0]

            if processcount == 0:
                sqlquery = '''INSERT INTO settings VALUES ("firefox.exe","C:\path_to_firefox",10,1)'''

                c.execute(sqlquery)
                connection.commit()

        connection.close()

    except Exception as ex:
        print_exception(ex)

def print_exception(ex):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    messagebox.MsgBox('EXCEPTION \'' + type(ex).__name__ + '\' IN ({}, LINE {} "{}"): {}'.format(filename,
                                                                                                 lineno,
                                                                                                 line.strip(),
                                                                                                 exc_obj),
                      style=(messagebox.MB_ICONERROR | messagebox.MB_TASKMODAL | messagebox.MB_OK), title="Exception")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())

