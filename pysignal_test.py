import sys, os
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QPushButton, QDialog, QLabel, QLineEdit, QGridLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import time, sys

class MyThread(QThread):
    updated = pyqtSignal(str)

    def run( self ):
        # do some functionality
        # for i in range(10000):
        #     self.updated.emit(str(i))
        print('success')
        time.sleep(60)
        i = 1
        self.updated.emit(str(i))

class Windows(QWidget):
    def __init__(self, parent=None):
        super(Windows, self).__init__(parent)

        self.app = QApplication(sys.argv)
        icon = QIcon("message.ico")
        self.menu = QMenu(self)
        self.exitAction1 = self.menu.addAction('Start')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        self.exitAction1.triggered.connect(self.start)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        self.tray.setToolTip("HPC SMS Alarm")
        self.tray.showMessage("HPC SMS Alarm on the tray", "monitoring...")

        self._thread = MyThread(self)
        self._thread.updated.connect(self.updateText)

    def start(self):
        self.tray.showMessage("HPC SMS Alarm on the tray", "Alarm ON")         
        self.menu.clear()
        self.exitAction1 = self.menu.addAction('Stop')
        self.exitAction2 = self.menu.addAction('Setup')
        self.exitAction3 = self.menu.addAction('Exit')
        self._thread = MyThread(App)
        self._thread.updated.connect(self.auto_stop)
        self._thread.start

    def updateText( self, text ):
        print(text)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = App()
    window.show()
    app.exec_()