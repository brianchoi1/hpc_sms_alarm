from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)   
import time, sys
import SW_sms_alarm_v4
# Snip...

# Step 1: Create a worker class
class Worker(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    ii = 5
    # def rrr(self, ii, dx, qq):
    #     xx = ii + dx + qq
    # def run(self, ii, dx, qq):
    #     """Long-running task."""
    #     # xx = self.rrr(ii, dx, qq)
    #     for i in range(ii):
    #         time.sleep(1)
    #         # print(xx)
    #         self.progress.emit(i + 1)
    #     self.finished.emit()
    def __init__(self):
        super().__init__()
        self.interval = SW_sms_alarm_v4.MyThread.interval
        print(self.interval)

    def run(self):
        """Long-running task."""
        # xx = self.rrr(ii, dx, qq)
        # ii = 5
        for i in range(self.ii):
            time.sleep(1)
            # print(xx)
            self.progress.emit(i + 1)
        self.finished.emit()

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()
        self.ii = 5
        self.dx = 1
        self.qq = 2

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")
    # Snip...
    def runLongTask(self):
        tq = SW_sms_alarm_v4.MyThread()
        tq.start
        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        # self.thread.started.connect(lambda: self.worker.run(5))
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        self.thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())






# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5 import uic
# import sys


# class Worker(QThread):

#     def __init__(self):
#         super().__init__()
#         self.power = True                           # run 매소드 루프 플래그

#     def run(self):
#         while self.power:
#             if ...:
#                 print('...')

#     def stop(self):
#         # 멀티쓰레드를 종료하는 메소드
#         self.power = False
#         self.quit()
#         self.wait(3000)  # 3초 대기 (바로 안꺼질수도)


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

#         # thread start
#         self.worker = Worker()
#         self.worker.start()

#     def closeEvent(self, event):
#         quit_msg = "Are you sure you want to exit the program?"
#         reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

#         if reply == QMessageBox.Yes:
#             # 멀티쓰레드를 종료하는 stop 메소드를 실행함
#             self.worker.stop()
#             event.accept()
#         else:
#             event.ignore()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     app.exec_()