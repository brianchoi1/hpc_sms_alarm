import sys, os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QPushButton, QDialog, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
from tendo import singleton 
me = singleton.SingleInstance()
import threading 
import ctypes 
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import SW_sms_alarm_v2 as SMS_main
import time
 
class setupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI_d()

    def setupUI_d(self):
        self.setGeometry(1500, 800, 250, 100)
        self.setWindowTitle("Setup")

        label1 = QLabel("Check interval(s): ")
        self.lineEdit1 = QLineEdit(interval, self)
        self.pushButton1= QPushButton("OK")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        self.setLayout(layout)
       
    def pushButtonClicked(self):
        global interval
        interval = self.lineEdit1.text()
        self.close()
        return interval
   
class thread_with_exception(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 

    def run(self):
        global interval 
        success_key = SMS_main.excute_program(interval)
           
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
        # print('stop')
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 
        return thread_id

def mail_sending():
    now = datetime.now()
    now_time = now.time()

    data = open('sms_alarm.setup').readlines() 
    data = [line.rstrip('\n') for line in data] 
    ip = str(data[0])
    id = str(data[1])      
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()  # TLS 사용시 필요
    smtp.login('skyiling4', '#c01020667742jy')
    
    msg = MIMEText(' ')
    msg['Subject'] = id + ' is playing at ' + str(now_time)
    smtp.sendmail('skyiling4@gmail.com', 'jaeyoung.choi@lge.com', msg.as_string())
    smtp.quit()

class App(object):
    def __init__(self):
        mail_sending()
        global interval
        interval = '600'

        self.app = QApplication(sys.argv)
        icon = QIcon("message.ico")
        self.menu = QMenu()
        self.exitAction1 = self.menu.addAction('Start')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        self.exitAction1.triggered.connect(self.start)
        self.exitAction2.triggered.connect(self.setting)
        self.exitAction3.triggered.connect(self.exit)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.tray.setToolTip("HPC SMS Alarm")
        self.tray.showMessage("HPC SMS Alarm on the tray", "monitoring...")

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

    def setting(self):
        dlf = setupDialog()
        dlf.exec_()

    def start(self):
        self.tray.showMessage("HPC SMS Alarm on the tray", "Alarm ON")         
        self.menu.removeAction(self.exitAction1)
        self.menu.removeAction(self.exitAction2)
        self.menu.removeAction(self.exitAction3)
        self.exitAction1 = self.menu.addAction('Stop')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        self.exitAction1.triggered.connect(self.manual_stop)
        # self.exitAction2.triggered.connect(self.setting)
        self.exitAction3.triggered.connect(self.exit)
        self.t1 = thread_with_exception()
        self.t1.start()

    def stop(self):
        self.tray.showMessage("HPC SMS Alarm on the tray", "Alarm OFF")
        self.menu.removeAction(self.exitAction1)
        self.menu.removeAction(self.exitAction2)
        self.menu.removeAction(self.exitAction3)
        self.exitAction1 = self.menu.addAction('Start')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        # self.exitAction1.triggered.connect(self.start)
        # self.exitAction2.triggered.connect(self.setting)
        self.exitAction3.triggered.connect(self.exit)

    def manual_stop(self):
        self.t1.raise_exception()
        self.t1.join()
        self.tray.showMessage("HPC SMS Alarm on the tray", "Alarm OFF")
        self.menu.removeAction(self.exitAction1)
        self.menu.removeAction(self.exitAction2)
        self.menu.removeAction(self.exitAction3)
        self.exitAction1 = self.menu.addAction('Start')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        self.exitAction1.triggered.connect(self.start)
        self.exitAction2.triggered.connect(self.setting)
        self.exitAction3.triggered.connect(self.exit)

    def exit(self):
        pid = os.getpid()
        os.kill(pid, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = App()
    window.run()
    app.exec_()
