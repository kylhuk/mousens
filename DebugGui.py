# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\qt\mousesens\DebugGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.createDB = QtWidgets.QPushButton(Dialog)
        self.createDB.setGeometry(QtCore.QRect(10, 10, 161, 41))
        self.createDB.setObjectName("createDB")
        self.dropDB = QtWidgets.QPushButton(Dialog)
        self.dropDB.setGeometry(QtCore.QRect(10, 60, 161, 51))
        self.dropDB.setObjectName("dropDB")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.createDB.setText(_translate("Dialog", "Create DB"))
        self.dropDB.setText(_translate("Dialog", "Drop DB"))

