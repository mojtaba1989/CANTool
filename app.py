from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pandas as pd
import os
import numpy as np

def str2msec(timestamp: str, ms=False):
    hours, minutes, seconds, milliseconds = map(int, timestamp.split(":"))
    total = (hours * 60 * 60) + (minutes * 60) + (seconds) + milliseconds/10000
    if ms:
        return total*1000
    else:
        return int(total*10)/10

def find_first_match(lst, condition):
    for index, item in enumerate(lst):
        if condition(item):
            return index, item
    return None, None # Return None if no match is found


rep = []
max_rep = 20
def reportUpdate(str, obj, new=False):
    if max_rep > -1:
        while len(rep)>max_rep:
            rep.pop(0)
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
    

script_path = os.path.abspath(__file__)
script_directory = os.path.dirname(script_path)


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
        self.LOG_FILE_NAME = ""
        self.VBO_FILE_NAME = ""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 375)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.log2csv_but = QtWidgets.QPushButton(self.centralwidget)
        self.log2csv_but.setGeometry(QtCore.QRect(290, 300, 75, 23))
        self.log2csv_but.setToolTip("Convers LOG file(s) to CSV")
        self.log2csv_but.setObjectName("log2csv_but")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 160, 271, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.report = QtWidgets.QLabel(self.groupBox)
        self.report.setGeometry(QtCore.QRect(16, 33, 241, 121))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.report.setFont(font)
        self.report.setObjectName("report")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 381, 41))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(os.path.join(script_directory,"logo.jpg")))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.vbo = QtWidgets.QGroupBox(self.centralwidget)
        self.vbo.setGeometry(QtCore.QRect(10, 50, 361, 51))
        self.vbo.setObjectName("vbo")
        self.dir_vob = QtWidgets.QLabel(self.vbo)
        self.dir_vob.setGeometry(QtCore.QRect(10, 20, 281, 16))
        self.dir_vob.setText("")
        self.dir_vob.setObjectName("dir_vob")
        self.bowse_vbo_but = QtWidgets.QPushButton(self.vbo)
        self.bowse_vbo_but.setGeometry(QtCore.QRect(300, 20, 51, 23))
        self.bowse_vbo_but.setObjectName("bowse_vbo_but")
        self.CAN = QtWidgets.QGroupBox(self.centralwidget)
        self.CAN.setGeometry(QtCore.QRect(10, 110, 361, 51))
        self.CAN.setObjectName("CAN")
        self.dir_can = QtWidgets.QLabel(self.CAN)
        self.dir_can.setGeometry(QtCore.QRect(10, 20, 281, 16))
        self.dir_can.setText("")
        self.dir_can.setObjectName("dir_can")
        self.bowse_can_but = QtWidgets.QPushButton(self.CAN)
        self.bowse_can_but.setGeometry(QtCore.QRect(300, 20, 51, 23))
        self.bowse_can_but.setObjectName("bowse_can_but")
        self.append_but = QtWidgets.QPushButton(self.centralwidget)
        self.append_but.setGeometry(QtCore.QRect(290, 270, 75, 23))
        self.append_but.setToolTip("Append CAN LOG to VBO file")
        self.append_but.setObjectName("append_but")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 380, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.log2csv_but.clicked.connect(self.convAction)
        self.bowse_vbo_but.clicked.connect(self.actionOpen_File_VBO)
        self.bowse_can_but.clicked.connect(self.actionOpen_File_LOG)
        self.append_but.clicked.connect(self.appendAction)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CAN Tool"))
        self.log2csv_but.setText(_translate("MainWindow", "LOG -> CSV"))
        self.groupBox.setTitle(_translate("MainWindow", "Report"))
        self.report.setText(_translate("MainWindow", ""))
        self.vbo.setTitle(_translate("MainWindow", "VBO File"))
        self.bowse_vbo_but.setText(_translate("MainWindow", "Browse"))
        self.CAN.setTitle(_translate("MainWindow", "LOG(*.csv) file"))
        self.bowse_can_but.setText(_translate("MainWindow", "Browse"))
        self.append_but.setText(_translate("MainWindow", "Append"))



    def actionOpen_File_VBO(self):
        temp = QtWidgets.QFileDialog.getOpenFileName(caption='Select *.vbo file', filter='vbo(*.vbo)')
        if temp and temp[0][-4:]=='.vbo':
            self.VBO_FILE_NAME = temp[0]
            self.dir_vob.setText(QtCore.QCoreApplication.translate("Dialog", self.VBO_FILE_NAME))
        else:
            self.VBO_FILE_NAME = ""


    def actionOpen_File_LOG(self):
        temp = QtWidgets.QFileDialog.getOpenFileName(caption='Select *.csv file', filter='log(*.csv)')
        if temp and temp[0][-4:]=='.csv':
            self.LOG_FILE_NAME = temp[0]
            self.dir_can.setText(QtCore.QCoreApplication.translate("Dialog", self.LOG_FILE_NAME))
        else:
            self.LOG_FILE_NAME = ""


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
    
    def appendAction(self):
        if self.VBO_FILE_NAME=="":
            reportUpdate(f'[ERROR] No VBO file selected', obj=self.report, new=True)
            return
        else:
            reportUpdate(f'[INFO] VBO file selected', obj=self.report, new=True)
        
        if self.LOG_FILE_NAME=="":
            reportUpdate(f'[ERROR] No LOG file selected', obj=self.report, new=True)
            return
        else:
            reportUpdate(f'[INFO] Log file selected', obj=self.report, new=True)
        
        secs=[]
        with open(self.VBO_FILE_NAME, 'r') as f:
            for i, l in enumerate(f):    
                if '[' in l:
                    header = secs.append((l, i))


        with open(self.VBO_FILE_NAME, 'r') as f:
            for sec in secs:
                if 'column names' in sec[0]:
                    cols = f.readlines()[sec[1]+1]
            while cols[-1] in ['\n', ' ']:
                cols = cols[:-1]
            cols = cols.split(' ')
                    
        with open(self.VBO_FILE_NAME, 'r') as f:
            for sec in secs:
                if 'data' in sec[0]:
                    lines = f.readlines()[sec[1]+1:]

        df = []
        for l in lines:
            df.append(list(l[:-1].split(' ')))
        vbo = pd.DataFrame(df, columns=cols)
        log = pd.read_csv(self.LOG_FILE_NAME, index_col=None)

        req_cols = ['time', 'IVT_Result_U1', 'IVT_Result_I']
        reportUpdate(f'[INFO] VBO->CSV [DONE]', obj=self.report, new=True)
        for req in req_cols:
            if req not in vbo.columns:
                reportUpdate(f'[ERROR] VBO: missing {req}', obj=self.report, new=True)
                return
        reportUpdate(f'[INFO] VBO is OK', obj=self.report, new=True)
            
        req_cols = ['CAN ID', 'Time', 'DLC']
        for req in req_cols:
            if req not in log.columns:
                reportUpdate(f'[ERROR] LOG: missing {req} ', obj=self.report, new=True)
                return
        reportUpdate(f'[INFO] LOG is OK', obj=self.report, new=True)
        reportUpdate(f'[INFO] Processing', obj=self.report, new=True)

        CAN_ID_LIST = np.unique(log['CAN ID'])
        log['Time_ms'] = [str2msec(i) for i in log['Time']]
        TIME_LIST = np.unique(log['Time_ms'])

        vbo['Traffic_kB/s'] = [0] * len(vbo['time'])
        vbo['Traffic_msgs/s'] = [0] * len(vbo['time'])
        for id in CAN_ID_LIST:
            vbo[id] = [0] * len(vbo['time'])

        Traffic_byte = []
        Traffic_msgs = []
        reportUpdate(f'[INFO] Initializing...', obj=self.report, new=True)
        reportUpdate(f'[INFO] calc traffic:0%', obj=self.report, new=True)
        for i, t in enumerate(TIME_LIST):
            tmp = log[log['Time_ms']==t]
            Traffic_byte.append(np.sum(tmp['DLC'])/100)
            Traffic_msgs.append(len(tmp['Time_ms'])/10)
            reportUpdate(f'[INFO] calc traffic:{np.ceil(i/len(TIME_LIST)*100)}%', obj=self.report, new=False)

        vbo_t = np.array([float(t) for t in vbo['time']])
        for i,_ in enumerate(vbo_t):
            vbo_t[i] = np.round(vbo_t[0] + i * 0.1,1)
        vbo_i = np.array([float(t) for t in vbo['IVT_Result_I']])

        idx,_ = find_first_match(Traffic_byte, lambda x: x>0)
        t_max_can = TIME_LIST[idx]
        idx,_ = find_first_match(np.abs(np.diff(vbo_i)), lambda x: x>500)
        t_max_vbo = vbo_t[idx]
        log['Time_ms'] += t_max_vbo - t_max_can
        log['Time_ms'] = np.round(log['Time_ms'], 1)
        TIME_LIST += t_max_vbo - t_max_can
        TIME_LIST = np.round(TIME_LIST, 1)

        reportUpdate(f'[INFO] CAN ID traffic:0%', obj=self.report, new=True)
        for i, id in enumerate(CAN_ID_LIST):
            tmp = log[log['CAN ID'] == id]
            lookup = dict(zip(tmp['Time_ms'], tmp['DLC']))
            vbo[id] = [lookup.get(val, 0) for val in vbo_t]
            reportUpdate(f'[INFO] CAN ID traffic:{np.ceil((i+1)/len(CAN_ID_LIST)*100)}%', obj=self.report, new=False)

        lookup = dict(zip(list(TIME_LIST), Traffic_byte))
        vbo['Traffic_kB/s'] = [lookup.get(val, 0) for val in vbo_t]
        lookup = dict(zip(TIME_LIST, Traffic_msgs))
        vbo['Traffic_msgs/s'] = [lookup.get(val, 0) for val in vbo_t]

        vbo.to_csv('vbo.csv', sep=' ', header=None, index=None)
        reportUpdate(f'[INFO] Gnerating new VBO...', obj=self.report, new=True)
        TARGET_FILE_NAME = self.VBO_FILE_NAME[:-4]+'_E.vbo'
        with open(self.VBO_FILE_NAME, 'r') as f:
            T_header = f.readlines()[:secs[1][1]-1]
            for c in vbo.columns:
                if c not in cols:
                    T_header.append(c+'\n')
            T_header.append('\n')

        with open(self.VBO_FILE_NAME, 'r') as f:
            T_channel_units = f.readlines()[secs[1][1]:secs[2][1]-1]
            T_channel_units.append('\n')

        with open(self.VBO_FILE_NAME, 'r') as f:
            T_fill = f.readlines()[secs[2][1]:secs[4][1]-1]
            T_fill.append('\n')

        with open(self.VBO_FILE_NAME, 'r') as f:
            T_columns = f.readlines()[secs[4][1]:secs[5][1]+1]
            while T_columns[1][-1] in ['\n', ' ']:
                T_columns[1] = T_columns[1][:-1]
            for c in vbo.columns:
                if c not in cols:
                    T_columns[1] += ' '+c
            T_columns[1] += '\n'

        with open('vbo.csv', 'r') as f:
            data = f.readlines()

        with open(TARGET_FILE_NAME, 'w') as f:
            for l in T_header:
                f.write(l)
            for l in T_channel_units:
                f.write(l)
            for l in T_fill:
                f.write(l)
            for l in T_columns:
                f.write(l)
            for l in data:
                f.write(l)
        
        reportUpdate(f'[INFO] DONE', obj=self.report, new=True)
        
        msg = QMessageBox()
        msg.setWindowTitle("Accomplished")
        msg.setText('New file:' + TARGET_FILE_NAME)
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
