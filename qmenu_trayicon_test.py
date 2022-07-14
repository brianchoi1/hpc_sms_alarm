import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QPushButton, QApplication, QDialog, QLabel, QLineEdit, QGridLayout, QComboBox, QCheckBox
from PyQt5.QtCore import Qt
import sys
import setup_ui

# class setupDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setupUI_d()

#     def setupUI_d(self):
#         global time_option_key, time_reserve_key, interval, start_time, end_time
#         time_option_key = 1
#         time_reserve_key = 0
#         interval = '600'
#         start_time = '0'
#         end_time = '0'

#         self.setGeometry(1500, 800, 250, 100)
#         self.setWindowTitle("Setup")

#         label1 = QLabel("Check interval(s): ")
#         label2 = QLabel("Reserved action: ")
#         self.lineEdit1 = QLineEdit('600',self)
#         self.cb = QComboBox(self)
#         self.cb.addItem('20:00 ~ 08:00')
#         self.cb.addItem('08:00 ~ 20:00')
#         self.cb.activated[str].connect(self.cb_switch)
#         self.qcb = QCheckBox('Reserve', self)
#         self.qcb.stateChanged.connect(self.reserve_func)
#         self.pushButton1= QPushButton("OK")
#         self.pushButton1.clicked.connect(self.pushButtonClicked)

#         layout = QGridLayout()
#         layout.addWidget(label1, 0, 0)
#         layout.addWidget(self.lineEdit1, 0, 1)
#         layout.addWidget(self.pushButton1, 0, 2)
#         layout.addWidget(label2, 1, 0)
#         layout.addWidget(self.cb, 1, 1)
#         layout.addWidget(self.qcb, 1, 2)
#         self.setLayout(layout)

#     def cb_switch(self, text):
#         global time_option_key
#         if text == '20:00 ~ 08:00':
#             time_option_key = 1
#         else:
#             time_option_key = 2
#         return time_option_key

#     def reserve_func(self, state):
#         global time_reserve_key
#         if state == Qt.Checked:
#             time_reserve_key = 1
#         else:
#             time_reserve_key = 0
#         return time_reserve_key
       
#     def pushButtonClicked(self):
#         global interval, start_time, end_time
#         interval = self.lineEdit1.text()
#         if time_option_key == 1:
#             start_time = '20:00'
#             end_time = '08:00'
#         else:
#             start_time = '08:00'
#             end_time = '20:00'
#         # self.close()
#         return start_time, end_time, interval

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = setupDialog()
#     window.show()
#     app.exec_()

import threading 
import ctypes 
import time 
   
class thread_with_exception(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 

    def run(self): 
        popSetup = setupDialog()
        popSetup.exec_()
           
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
   
    def raise_exception(self): 
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
              ctypes.py_object(SystemExit)) 
        print('stop')
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 
        return thread_id




app = QApplication(sys.argv)
trayIcon = QSystemTrayIcon(QIcon('message.ico'), parent = app)
trayIcon.setToolTip('HPC SMS Alarm')
trayIcon.show()

def callSetupdialog():
    popSetup = setup_ui.setupDialog()
    popSetup.exec_()

menu = QMenu()
def menu1():
    global exitAction1, exitAction2 ,exitAction3 ,exitAction4
    exitAction1 = menu.addAction('Start')
    exitAction2 = menu.addAction('Setup')
    exitAction3 = menu.addAction('Exit')
    exitAction1.triggered.connect(menu2)
    exitAction2.triggered.connect(callSetupdialog)
    exitAction3.triggered.connect(app.quit)

    trayIcon.setContextMenu(menu)

def menu2():
    global exitAction1, exitAction2 ,exitAction3 ,exitAction4
    menu.removeAction(exitAction1)
    menu.removeAction(exitAction2)
    menu.removeAction(exitAction3)
    menu.removeAction(exitAction4)
    exitAction5 = menu.addAction('Stop')
    exitAction6 = menu.addAction('Stop')
    exitAction7 = menu.addAction('Setup')
    exitAction8 = menu.addAction('Exit')
    # trayIcon.setContextMenu(menu)

menu1()       
sys.exit(app.exec_())

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MyWindow()
#     window.show()
#     app.exec_()
