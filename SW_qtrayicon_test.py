import sys, os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QPushButton, QDialog, QLabel, QLineEdit, QGridLayout, QComboBox, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from tendo import singleton 
me = singleton.SingleInstance()
import threading 
import ctypes 
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
import SW_sms_alarm_v2 as SMS_main
 
class setupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI_d()

    def setupUI_d(self):
        self.setGeometry(1500, 800, 250, 100)
        self.setWindowTitle("Setup")

        label1 = QLabel("Check interval(s): ")
        label2 = QLabel("Reserved action: ")
        self.lineEdit1 = QLineEdit('600',self)
        self.cb = QComboBox(self)
        self.cb.addItem('20:00 ~ 08:00')
        self.cb.addItem('08:00 ~ 20:00')
        self.cb.activated[str].connect(self.cb_switch)
        self.qcb = QCheckBox('Reserve', self)
        self.qcb.stateChanged.connect(self.reserve_func)
        self.pushButton1= QPushButton("OK")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.cb, 1, 1)
        layout.addWidget(self.qcb, 1, 2)
        self.setLayout(layout)

    def cb_switch(self, text):
        global time_option_key
        if text == '20:00 ~ 08:00':
            time_option_key = 1
        else:
            time_option_key = 2
        return time_option_key

    def reserve_func(self, state):
        global time_reserve_key
        if state == Qt.Checked:
            time_reserve_key = 1
        else:
            time_reserve_key = 0
        return time_reserve_key
       
    def pushButtonClicked(self):
        global interval, start_time, end_time
        interval = self.lineEdit1.text()
        if time_option_key == 1:
            start_time = '20'
            end_time = '8'
        else:
            start_time = '8'
            end_time = '20'
        self.close()
        return start_time, end_time, interval
   
class thread_with_exception(threading.Thread): 
    def __init__(self): 
        threading.Thread.__init__(self) 

    def run(self):
        global interval 
        SMS_main.excute_program(interval)
           
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

class App():
    def __init__(self):
        mail_sending()
        global time_option_key, time_reserve_key, interval, start_time, end_time
        time_option_key = 1
        time_reserve_key = 0
        interval = '600'
        start_time = '0'
        end_time = '0'

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
        if time_reserve_key == 0:
            self.t1 = thread_with_exception()
            self.t1.start()
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
        else:
            self.tray.showMessage("HPC SMS Alarm on the tray", "Timer ON")
            self.menu.removeAction(self.exitAction1)
            self.menu.removeAction(self.exitAction2)
            self.menu.removeAction(self.exitAction3)
            self.exitAction1 = self.menu.addAction('Stop')
            self.exitAction2 = self.menu.addAction('Setup')
            self.exitAction3 = self.menu.addAction('Exit')
            # self.exitAction1.triggered.connect(self.manual_stop)
            # self.exitAction2.triggered.connect(self.setting)
            self.exitAction3.triggered.connect(self.exit)
            th1 = threading.Thread(target=self.timer())
            th1.start()
            th1.join()

    def timer(self):
        now = datetime.now()
        now_time = now.hour
        i = 1
        while i > 0:
            if now_time >= int(start_time) and now_time <= int(end_time):
                self.t1 = thread_with_exception()
                self.t1.start()
                time.sleep(5)
                self.auto_stop() 
                break
            elif now_time <= int(start_time) and now_time >= int(end_time):
                self.t1 = thread_with_exception()
                self.t1.start()
                time.sleep(5)
                self.auto_stop() 
                break
            else:
                time.sleep(300) 
    
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

    def auto_stop(self):
        while True:
            if not self.t1.is_alive():
                break
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
