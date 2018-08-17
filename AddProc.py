# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\User01\Documents\dev\mousens\qt\mousesens\AddProc.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialogAddProc(object):
    def setupUi(self, dialogAddProc):
        dialogAddProc.setObjectName("dialogAddProc")
        dialogAddProc.resize(871, 547)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialogAddProc.sizePolicy().hasHeightForWidth())
        dialogAddProc.setSizePolicy(sizePolicy)
        dialogAddProc.setMinimumSize(QtCore.QSize(871, 547))
        dialogAddProc.setMaximumSize(QtCore.QSize(871, 547))
        dialogAddProc.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        dialogAddProc.setWindowTitle("Add Processes")
        self.buttonBox = QtWidgets.QDialogButtonBox(dialogAddProc)
        self.buttonBox.setGeometry(QtCore.QRect(480, 510, 381, 31))
        self.buttonBox.setMaximumSize(QtCore.QSize(381, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tableProc = QtWidgets.QTableWidget(dialogAddProc)
        self.tableProc.setGeometry(QtCore.QRect(10, 10, 851, 491))
        self.tableProc.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableProc.setTabKeyNavigation(False)
        self.tableProc.setProperty("showDropIndicator", False)
        self.tableProc.setDragDropOverwriteMode(False)
        self.tableProc.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableProc.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableProc.setWordWrap(False)
        self.tableProc.setCornerButtonEnabled(False)
        self.tableProc.setObjectName("tableProc")
        self.tableProc.setColumnCount(0)
        self.tableProc.setRowCount(0)
        self.tableProc.horizontalHeader().setHighlightSections(False)
        self.tableProc.horizontalHeader().setStretchLastSection(True)
        self.tableProc.verticalHeader().setVisible(False)
        self.tableProc.verticalHeader().setHighlightSections(False)

        self.retranslateUi(dialogAddProc)
        self.buttonBox.accepted.connect(dialogAddProc.accept)
        self.buttonBox.rejected.connect(dialogAddProc.reject)
        QtCore.QMetaObject.connectSlotsByName(dialogAddProc)

    def retranslateUi(self, dialogAddProc):
        _translate = QtCore.QCoreApplication.translate
        self.tableProc.setSortingEnabled(True)

