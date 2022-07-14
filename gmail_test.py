# import smtplib
# from email.mime.text import MIMEText
# from datetime import datetime
# now = datetime.now()
# now_time = now.time()

# data = open('sms_alarm.setup').readlines()                        #setting파일 한줄씩 읽어서 변수지정
# data = [line.rstrip('\n') for line in data]                 #엔터 제거 공백 제거
# ip = str(data[0])
# id = str(data[1])      
# smtp = smtplib.SMTP('smtp.gmail.com', 587)
# smtp.starttls()  # TLS 사용시 필요
# smtp.login('skyiling4', '#c01020667742jy')
 
# msg = MIMEText(' ')
# msg['Subject'] = id + ' is playing at ' + str(now_time)
# smtp.sendmail('skyiling4@gmail.com', 'jaeyoung.choi@lge.com', msg.as_string())
 
# smtp.quit()



def dd():
    try:
        print('s')
        time.sleep(5)
    except:
        pass

import time
while True:
    try:
        dd()
        while True:
            print('s')
            time.sleep(5)
    except:
        continue