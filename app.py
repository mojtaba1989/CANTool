from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import os

rep = []
def reportUpdate(str, obj, new=False):
    if new or not rep:
        rep.append(str)
    else:
        rep[-1] = str
    if len(rep)>6:
        rep.pop(0)
    rep_str = ''
    for l in rep:
        rep_str += l+'\n'
    obj.setText(rep_str)
    obj.repaint()

def readHeader(lines: list):
    header = []
    for idx, l in enumerate(lines):
        if '***' in l:
            header.append(l)
        else:
            break
    return idx, header

def readFooter(lines: list):
    footer = []
    for idx, l in reversed(list(enumerate(lines))):
        if '***' in l:
            footer.append(l)
        elif l == '\n':
            pass
        else:
            break
    return idx+1, footer

def readColumn(line: str):
    if '<' not in line:
        return None, None
    cols = line.replace('*','').replace('<', '').replace('>', ',')
    while cols[-1] in [' ', '\n', ',']:
        cols = cols[:-1]
    return  len(cols.split(',')), cols.split(',')

def insertSeperator(line: str, count: int):
    if line[0]=='*' or line=='\n' or line.count(' ') < count-1:
        return None
    newLine = line.replace(' ', ',', count - 1)
    while newLine[-1] in [' ', '\n', ',']:
        newLine = newLine[:-1]
    newLine = newLine.split(',')
    if len(newLine) == count:
        return newLine
    else:
        return None 
class ScrollLabel(QScrollArea):

	# constructor
	def __init__(self, *args, **kwargs):
		QScrollArea.__init__(self, *args, **kwargs)

		# making widget resizable
		self.setWidgetResizable(True)

		# making qwidget object
		content = QWidget(self)
		self.setWidget(content)

		# vertical box layout
		lay = QVBoxLayout(content)

		# creating label
		self.label = QLabel(content)

		# setting alignment to the text
		self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

		# making label multi-line
		self.label.setWordWrap(True)

		# adding label to the layout
		lay.addWidget(self.label)

	# the setText method
	def setText(self, text):
		# setting text to the label
		self.label.setText(text)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(381, 223)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.log2csv_but = QtWidgets.QPushButton(self.centralwidget)
        self.log2csv_but.setGeometry(QtCore.QRect(290, 160, 75, 23))
        self.log2csv_but.setObjectName("log2csv_but")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 271, 171))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.report = QtWidgets.QLabel(self.groupBox)
        self.report.setGeometry(QtCore.QRect(16, 33, 241, 121))
        self.report.setObjectName("report")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.log2csv_but.clicked.connect(self.convAction)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Log Tool"))
        self.log2csv_but.setText(_translate("MainWindow", "log to CSV"))
        self.groupBox.setTitle(_translate("MainWindow", "Report"))


    def convAction(self):
        temp = QtWidgets.QFileDialog.getOpenFileNames(caption='Select *.log files', filter='log(*.log)')
        if not temp:
            return
        failed = []
        for LOG_FILE in temp[0]:
            LOG_FILE_BASE = os.path.basename(LOG_FILE)
            with open(LOG_FILE, 'r') as f:
                lines = f.readlines()
            reportUpdate(f'Initializing {LOG_FILE_BASE} processing', obj=self.report, new=True)
            idx_start, header = readHeader(lines)
            idx_end, footer = readFooter(lines)
            colNum, cols = readColumn(header[-1])
            data = []
            erfound = False
            total = len(lines[idx_start:idx_end])
            reportUpdate(f'{total} line of data and {colNum} columns detected', obj=self.report, new=True)
            reportUpdate(f'Starting the process on {LOG_FILE_BASE}', obj=self.report, new=True)
            reportUpdate(f'progress: 0%', obj=self.report, new=True)
            idx = 0
            for l in lines[idx_start:idx_end]:
                if idx%10==0:
                    reportUpdate(f'progress: {int(idx/total*100)+1}%', obj=self.report, new=False)
                line_list = insertSeperator(l, colNum)
                if line_list:
                    data.append(line_list)
                    erfound = False
                elif not erfound:
                    reportUpdate(f'[ERROR] bad line at {idx+idx_start}', obj=self.report, new=True)
                    msg = QMessageBox()
                    msg.setWindowTitle("Corrupted Log")
                    msg.setText(f"A none data row is detected within data\n Wish to continue?")
                    msg.setIcon(QMessageBox.Question)
                    msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                    msg.setDefaultButton(QMessageBox.Yes)
                    result = msg.exec_()
                    if result==QMessageBox.Yes:
                        erfound = True
                        reportUpdate(f'[INFO] Ignored', obj=self.report, new=True)
                        reportUpdate(f'', obj=self.report, new=False)
                    else:
                        failed.append(LOG_FILE)
                        reportUpdate(f'[INFO] Abort processing {LOG_FILE_BASE}', obj=self.report, new=True)
                        break
                idx += 1

            df = pd.DataFrame(data, columns=cols, index=None)
            CSV_FILE = LOG_FILE[:-3]+'csv'
            df.to_csv(CSV_FILE, index=None)
        msg = QMessageBox()
        msg.setWindowTitle("Accomplished")
        msg.setText(f'{len(temp[0])-len(failed)} logs have been converted')
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())