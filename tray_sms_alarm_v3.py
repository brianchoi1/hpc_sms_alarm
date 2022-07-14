from pystray import MenuItem, Menu
import pystray
from PIL import Image
from tendo import singleton 
me = singleton.SingleInstance()
import sys
from threading import Thread, Event
import SW_sms_alarm_v2
import os
import time

global time_option_key, time_reserve_key, interval, start_time, end_time
time_option_key = 1
time_reserve_key = 0
interval = '600'
start_time = '0'
end_time = '0'
menu_1st = 'Start sms alarm'

def action():
    global menu_1st
    if menu_1st == 'Start sms alarm':
        menu_1st = 'Stop sms alarm'
        pidd = os.getpid()
        ppidd = os.getppid()
        print(pidd)
        print(ppidd)
        # evt.set()
        icon.update_menu
        SW_sms_alarm_v2.excute_program(time_option_key, time_reserve_key)

        
    else:
        menu_1st = 'Start sms alarm'
        icon.update_menu
        time.sleep(6000)
    
def setupp():
    app = QApplication(sys.argv)
    window = setupDialog()
    window.show()
    app.exec_()
    return

def exit_program():
    icon.stop()
    return

from PyQt5.QtWidgets import QPushButton, QApplication, QDialog, QLabel, QLineEdit, QGridLayout, QComboBox, QCheckBox
from PyQt5.QtCore import Qt
import sys

class setupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI_d()

    def setupUI_d(self):
        global time_option_key, time_reserve_key, interval, start_time, end_time
        time_option_key = 1
        time_reserve_key = 0
        interval = '600'
        start_time = '0'
        end_time = '0'

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
            start_time = '20:00'
            end_time = '08:00'
        else:
            start_time = '08:00'
            end_time = '20:00'
        self.close()
        return start_time, end_time, interval

if __name__ == "__main__":
    def setup_pre():
        p = Thread(name="SubProcess2", target=setupp, daemon=True)
        p.start()
    
    def action_pre():
        global pid
        Thread(target=action, daemon=True).start()
        pid = os.getpid()
        return pid

    def iconnary():
        global icon
        image = Image.open("message.ico")
        icon = pystray.Icon("name", image, "HPC sms alarm", menu=Menu(MenuItem(lambda text: menu_1st, action_pre), MenuItem('Setup', setup_pre), MenuItem('Exit', exit_program)))
        icon.run()
        return icon
    icon = iconnary()

