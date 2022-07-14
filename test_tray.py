jobtype = 'fluent'

# if jobtype in ['lsdyna', 'fluent', 'moldflow', 'abaqus']:
if jobtype == 'lsdyna' or jobtype == 'fluent':
    print('included')
else:
    print('excluded')


# # from pystray import MenuItem as item
# # import pystray
# # from PIL import Image

# # def action():
# #     dlg = setupDialog()
# #     dlg.exec_()

# # image = Image.open("message.ico")
# # menu = (item('name', action), item('name', action), item('Exit', action))
# # icon = pystray.Icon("name", image, "title", menu)
# # icon.run()

# from PyQt5.QtWidgets import QPushButton, QApplication, QDialog, QLabel, QLineEdit, QGridLayout, QComboBox, QCheckBox
# from PyQt5.QtCore import Qt
# import sys

# from PyQt5.QtWidgets import QPushButton, QApplication, QDialog, QLabel, QLineEdit, QGridLayout, QComboBox, QCheckBox
# from PyQt5.QtCore import Qt

# class setupDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setupUI_d()

#     def setupUI_d(self):
#         self.time_option_key = 1
#         self.time_reserve_key = 0
#         self.interval = '600'

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
#         if text == '20:00 ~ 08:00':
#             self.time_option_key = 1
#         else:
#             self.time_option_key = 2

#     def reserve_func(self, state):
#         if state == Qt.Checked:
#             self.time_reserve_key = 1
#         else:
#             self.time_reserve_key = 0
       
#     def pushButtonClicked(self):
#         self.interval = self.lineEdit1.text()
#         if self.time_option_key == 1:
#             self.start_time = '20:00'
#             self.end_time = '08:00'
#         else:
#             self.start_time = '08:00'
#             self.end_time = '20:00'
#         self.close()

# def setupp():
#     if __name__ == "__main__":
#         app = QApplication(sys.argv)
#         window = setupDialog()
#         window.show()
#         app.exec_()
#     return

# setupp()