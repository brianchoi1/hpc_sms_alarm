import sys, os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QPushButton, QDialog, QLabel, QLineEdit, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread
import singleton 
me = singleton.SingleInstance()
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import SW_sms_alarm_v4 as SMS_main
import time
 
class setupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.interval = SMS_main.MyThread.interval
        self.setupUI_d()

    def setupUI_d(self):
        self.setGeometry(1500, 800, 250, 100)
        self.setWindowTitle("Setup")

        label1 = QLabel("Check interval(s): ")
        self.lineEdit1 = QLineEdit(self.interval, self)
        self.pushButton1= QPushButton("OK")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(self.pushButton1, 0, 2)
        self.setLayout(layout)
       
    def pushButtonClicked(self):
        self.interval = self.lineEdit1.text()
        SMS_main.MyThread.interval = self.interval
        f = open('sms_interval.setup', 'w', encoding='utf-8')
        f.write(self.interval)
        f.close()
        self.close()

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

class App(QDialog):
    def __init__(self):
        super().__init__()
        mail_sending()

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
        self.tray.setToolTip("Monitoring...")
        self.tray.showMessage("HPC SMS Alarm on the tray", "Alarm ON")         
        self.menu.clear()
        self.exitAction1 = self.menu.addAction('Stop')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        self.exitAction1.triggered.connect(self.manual_stop)
        # self.exitAction2.triggered.connect(self.setting)
        self.exitAction3.triggered.connect(self.exit)
        
        self.thread = QThread(self)
        self.worker = SMS_main.MyThread()
        self.worker.moveToThread(self.thread)
        
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(self.auto_stop)
        self.thread.start()
        time.sleep(4)

    def auto_stop(self):
        self.tray.setToolTip("Alarm OFF")
        self.tray.showMessage("HPC SMS Alarm on the tray", "Alarm OFF, No HPC Jobs")
        self.menu.clear()
        self.exitAction1 = self.menu.addAction('Start')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        self.exitAction1.triggered.connect(self.start)
        self.exitAction2.triggered.connect(self.setting)
        self.exitAction3.triggered.connect(self.exit)

    def manual_stop(self):
        self.worker.stop()
        self.tray.setToolTip("Alarm OFF")
        self.tray.showMessage("HPC SMS Alarm on the tray", "Alarm OFF")
        self.menu.clear()
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
