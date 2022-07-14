from datetime import datetime
import time

now = datetime.now()
now_time = now.hour

start_time = 22
end_time = 8

def start_func():
    print(now_time)

i = 1
while i > 0:

    if now_time >= start_time:
        start_func()
        break
    elif now_time <= end_time:
        start_func()
        break
    else:
        time.sleep(300) 

