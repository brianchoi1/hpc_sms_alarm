from datetime import datetime
now_ = datetime.now().hour

dd = now_ - datetime.now().hour
print(dd)
# duration_ = 12
# if now_ + duration_ >= 24:
#     end_time = abs(24 - (now_ + duration_))
# else:
#     end_time = now_ + duration_

print(end_time)
# # import subprocess
# # from tendo import singleton 
# # me = singleton.SingleInstance()


# # proc = subprocess.Popen(['echo', 'Hello world'], stdout=subprocess.PIPE)
# # out, err = proc.communicate()
# # print(out)
# # print(out.decode('utf-8'))

# ##################################################################################

# import threading 
# import ctypes 
# import time 
   
# class thread_with_exception(threading.Thread): 
#     def __init__(self): 
#         threading.Thread.__init__(self) 

#     def run(self): 
#         i = 10
#         while i > 0:
#             print('ongoing process')
#             time.sleep(3)
#             i -= 1
           
#     def get_id(self): 
#         # returns id of the respective thread 
#         if hasattr(self, '_thread_id'): 
#             return self._thread_id 
#         for id, thread in threading._active.items(): 
#             if thread is self: 
#                 return id
   
#     def raise_exception(self): 
#         thread_id = self.get_id() 
#         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
#               ctypes.py_object(SystemExit)) 
#         print('stop')
#         if res > 1: 
#             ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
#             print('Exception raise failure') 
#         return thread_id
       
# t1 = thread_with_exception() 
# t1.start() 
# t1.join()
# print('finish')
# # time.sleep(5) 
# # t1.raise_exception() 
# # t1.join()
# # time.sleep(5)

# # t2 = thread_with_exception() 
# # t2.start()
# # time.sleep(5)
# # t2.raise_exception()
# # t2.join()
# # time.sleep(5)

# # time.sleep(600)
# # print('finish')


# # import threading, time

# # class Me(threading.Thread):
# #     def __init__(self):
# #         threading.Thread.__init__(self)
# #         #flag to pause thread
# #         self.paused = False
# #         # Explicitly using Lock over RLock since the use of self.paused
# #         # break reentrancy anyway, and I believe using Lock could allow
# #         # one thread to pause the worker, while another resumes; haven't
# #         # checked if Condition imposes additional limitations that would 
# #         # prevent that. In Python 2, use of Lock instead of RLock also
# #         # boosts performance.
# #         self.pause_cond = threading.Condition(threading.Lock())

# #     def run(self):
# #         while True:
# #             with self.pause_cond:
# #                 while self.paused:
# #                     self.pause_cond.wait()

# #                 #thread should do the thing if
# #                 #not paused
# #                 self.print_machine()
# #                 # i=5
# #                 # for ii in range(i) :
# #                 #     print(ii)
# #                 #     time.sleep(5)
# #                 # print('dd')
# #             time.sleep(5)

# #     def pause(self):
# #         self.paused = True
# #         # If in sleep, we acquire immediately, otherwise we wait for thread
# #         # to release condition. In race, worker will still see self.paused
# #         # and begin waiting until it's set back to False
# #         self.pause_cond.acquire()
# #         print('pause')

# #     #should just resume the thread
# #     def resume(self):
# #         self.paused = False
# #         # Notify so thread will wake after lock released
# #         self.pause_cond.notify()
# #         # Now release the lock
# #         self.pause_cond.release()
# #         print('restart')
    
# #     def print_machine(self):
# #         # i=1
# #         # while i > 0:
# #         #     print('actioning')
# #         #     time.sleep(5)
        
# #         i=5
# #         for ii in range(i) :
# #             print(ii)
# #             time.sleep(5)

# # t1 = Me()
# # t1.start()
# # time.sleep(5)
# # t1.pause()
# # time.sleep(5)
# # t1.resume()
# # time.sleep(5)
# # t1.pause()



# # import threading, time

# # def do_this():

# #     global dead
# #     i=1
# #     while i > 0:
# #         print('qwd')
# #         time.sleep(3)
# #     while (not dead):
# #         pass
# # def main():
# #     global dead
# #     dead = False

# #     our_thread = threading.Thread(target=do_this)
# #     our_thread.start()

# # def stopp():
# #     dead = True

# # main()
# # time.sleep(10)
