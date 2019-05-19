# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(642, 609)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 621, 341))
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 400, 611, 201))
        self.groupBox_5.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textEdit_1 = QtWidgets.QTextEdit(self.groupBox_5)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.textEdit_1.setFont(font)
        self.textEdit_1.setStyleSheet("")
        self.textEdit_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.textEdit_1.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEdit_1.setReadOnly(True)
        self.textEdit_1.setObjectName("textEdit_1")
        self.gridLayout_4.addWidget(self.textEdit_1, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 350, 101, 33))
        self.pushButton.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
"background-color:rgba(225,225,225,180);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-color:rgba(0,0,0,30);\n"
"color:rgba(0,0,0,200);\n"
"padding:6px;}\n"
"QPushButton:pressed{\n"
"background-color:rgba(205,230,255,200);\n"
"border-color:rgba(0,120,215,30);\n"
"border-style:inset;\n"
"color:rgba(0,0,0,100);}\n"
"QPushButton:hover{\n"
"background-color:rgba(230,240,250,100);\n"
"border-color:rgba(0,120,215,200);\n"
"color:rgba(0,0,0,200);}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 350, 131, 33))
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"background-color:rgba(225,225,225,180);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-color:rgba(0,0,0,30);\n"
"color:rgba(0,0,0,200);\n"
"padding:6px;}\n"
"QPushButton:pressed{\n"
"background-color:rgba(205,230,255,200);\n"
"border-color:rgba(0,120,215,30);\n"
"border-style:inset;\n"
"color:rgba(0,0,0,100);}\n"
"QPushButton:hover{\n"
"background-color:rgba(230,240,250,100);\n"
"border-color:rgba(0,120,215,200);\n"
"color:rgba(0,0,0,200);}\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 350, 131, 33))
        self.pushButton_3.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"background-color:rgba(225,225,225,180);\n"
"border-style:outset;\n"
"border-width:2px;\n"
"border-color:rgba(0,0,0,30);\n"
"color:rgba(0,0,0,200);\n"
"padding:6px;}\n"
"QPushButton:pressed{\n"
"background-color:rgba(205,230,255,200);\n"
"border-color:rgba(0,120,215,30);\n"
"border-style:inset;\n"
"color:rgba(0,0,0,100);}\n"
"QPushButton:hover{\n"
"background-color:rgba(230,240,250,100);\n"
"border-color:rgba(0,120,215,200);\n"
"color:rgba(0,0,0,200);}\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Compiler"))
        self.groupBox.setTitle(_translate("MainWindow", "Source File"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Output"))
        self.pushButton.setText(_translate("MainWindow", "Open File"))
        self.pushButton_2.setText(_translate("MainWindow", "Execute SDT"))
        self.pushButton_3.setText(_translate("MainWindow", "Generate MIPS"))

