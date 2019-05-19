from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
# from PyQt5.QtGui import QTextCursor,QTextCharFormat,QColor
from mainWindow import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication
from SDT import SDTAnalysis
from Mips import Assembler
from Production import getCPro


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.loadSourceFile = False
        self.sdtDone = False
        self.error = False
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openFile)
        self.pushButton_2.clicked.connect(self.SDTAnalysis)
        self.pushButton_3.clicked.connect(self.getMips)
        self.textEdit_1.textChanged.connect(self.scrollToBottom)

    def scrollToBottom(self):
        self.textEdit_1.moveCursor(QTextCursor.End)


    def openFile(self):
        fname, _ = QFileDialog.getOpenFileName(self.centralwidget, "Select source file", "./", "Text Files (*.txt)")
        if fname == '': return
        self.textEdit_1.setText('')
        inputPro = getCPro()                 # 获取产生式
        sdt = SDTAnalysis(inputPro)          # 构造语法分析器
        sdt.buildProList()                   # 构造产生式表
        sdt.setStart('Program')              # 设置起始符号
        sdt.delLeftRecur()                   # 消除左递归
        sdt.getFirst()                       # 求FIRST集合
        sdt.getFollow()                      # 求FOLLOW集合
        sdt.buildLL1Table()                  # 构造LL1分析表
        sdt.readFile(fname)                  # 读取待分析文件
        self.sdt = sdt
        self.loadSourceFile = True
        self.sdtDone = False
        self.error = False
        with open(fname, 'r') as f:
            text = ''
            for i, line in enumerate(f.readlines()):
                text += (str(i+1).ljust(6) + line)
            self.textEdit.setText(text)
            f.close()

    def SDTAnalysis(self):
        text = self.textEdit_1.toPlainText()
        if self.loadSourceFile == False:
            text += 'Please select a source file first.\n'
        elif self.sdtDone == True:
            text += 'SDT has already been finished.\n'
        elif self.error == True:
            text += 'Please correct the error first.\n'
        else:
            ERRORresult, codeList, symbolList = self.sdt.analyze()  # 语法分析,返回要错误信息和栈信息
            if ERRORresult == '':
                text += 'Finish SDT successfully, 0 error. \nIntermediate Code saved to InterCode.txt\n'
                self.sdtDone = True
                self.codeList = codeList
                with open('InterCode.txt', 'w') as f:
                    for c in codeList:
                        f.write(str(c['addr']) + ' ' + c['op'] + ' ')
                        def getArg(arg):
                            if arg in c.keys():
                                try:
                                    if 'Imme' in c[arg].keys():
                                        f.write(c[arg]['Imme'] + ' ')
                                    elif 'reg' in c[arg].keys():
                                        f.write('T' + str(c[arg]['reg']) + ' ')
                                    elif 'symbolIndex' in c[arg].keys():
                                        f.write(
                                            symbolList[c[arg]['symbolIndex']]['idName'] + '_' + symbolList[c[arg]['symbolIndex']]['domain'] + ' ')
                                except:
                                    f.write(str(c[arg])+' ')
                            else:
                                f.write('- ')
                        getArg('arg1'), getArg('arg2'), getArg('result')
                        f.write('\n')

                f.close()
                self.symbolList = symbolList
            else:
                self.error = True
                text += ERRORresult
                self.textEdit_1.setText(text)
        self.textEdit_1.setText(text)

    def getMips(self):
        text = self.textEdit_1.toPlainText()
        if self.loadSourceFile == False:
            text += 'Please select a source file first.\n'
        elif self.sdtDone == False:
            text += 'Please finish SDT first.\n'
        else:
            mips = Assembler(self.symbolList, self.codeList)
            code = mips.generate()
            with open('MIPS.asm', 'w') as f:
                f.write(code)
                f.close()
            text += 'Generate MIPS successfully.\nMIPS code saved to MIPS.asm\n'
        self.textEdit_1.setText(text)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())