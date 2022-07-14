# from time import sleep
# from threading import Timer
# from datetime import datetime

# class MyInfiniteTimer():
#     """
#     A Thread that executes infinitely
#     """
#     def __init__(self, t, hFunction):
#         self.t = t
#         self.hFunction = hFunction
#         self.thread = Timer(self.t, self.handle_function)
        
#     def handle_function(self):
#         self.hFunction()
#         self.thread = Timer(self.t, self.handle_function)
#         self.thread.start()
        
#     def start(self):
#         self.thread = Timer(self.t, self.handle_function)
#         self.thread.start()
        
#     def cancel(self):
#         self.thread.cancel()

# def print_current_datetime():
#     print(datetime.today())

# t = MyInfiniteTimer(1, print_current_datetime)
# t.start()
# sleep(5)
# t.cancel()
# sleep(5)
# t.start()
# sleep(5)
# t.cancel()

import SW_sms_alarm_v4 as swa
interval = 70
swa.MyThread().excute_program(interval)