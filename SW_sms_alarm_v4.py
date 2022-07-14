import re
from PyQt5.QtCore import QThread, pyqtSignal
import paramiko
import time
import os
from twilio.rest import Client
from datetime import datetime

class MyThread(QThread):
    finished = pyqtSignal()
    updated = pyqtSignal(int)
    ssh = paramiko.SSHClient()                                  #paramiko 셋업
    hpc_path_default = '/nas/users/HA'                          #hpc기본주소세팅
    path = './'                                                 #경로 접미사
    c_dir = os.getcwd()
    data = open('sms_alarm.setup').readlines()                        #setting파일 한줄씩 읽어서 변수지정
    data = [line.rstrip('\n') for line in data]                 #엔터 제거 공백 제거
    ip = str(data[0])
    id = str(data[1])                                           #아이디 저장
    pw = str(data[2]) 
    account_sid = str(data[3])
    auth_token = str(data[4])
    _to = str(data[5])
    _from = str(data[6])
    ref_string = ["PEND", "RUN", "EXIT", "UNKWN", "DONE"]
    jobname_list = []
    jobid_list = []
    jobstatus_list = []  
    jobtype_list = []
    data2 = open('sms_interval.setup').readlines()
    data2 = [line.rstrip('\n') for line in data2]
    interval = str(data2[0])

    cmd_log = '. /etc/profile;. ~/.bash_profile;. ~/.bashrc; bjobs 2>&1 > _log_.txt' 
    cmd_1 = '. /etc/profile;. ~/.bash_profile;. ~/.bashrc; bjobs '
    cmd_2 = ' 2>&1 > ' 

    def msg_writing(self, msg):
        f = open(msg, 'w', encoding='utf-8')     # txt파일 생성
        f.close()

    def get_log_file(self, hpc_path_default, ssh, ip, id, pw, c_dir, cmd_log):
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       # hpc 접속키 획득
            ssh.connect(ip, 22, id, pw)                  # 로그인 유효성 확인
            sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
            ssh.exec_command(cmd_log)
            time.sleep(1)
            sftp.get(hpc_path_default + '/' + id + '/_log_.txt', c_dir + '\\' + '_log_.txt')
            files_path = c_dir + '\\' + '_log_.txt'
            return files_path
        except:
            self.msg_writing('No log file on HPC')
            exit()

    def jobid_check(self, files_path):    
        jobname_list = []
        jobid_list = []
        jobstatus_list = []  
        jobtype_list = []
        job_read_list = open(files_path, "r").readlines()[1:]
        for pre_check in job_read_list[:]:
            if pre_check[0:8].split() == []:
                job_read_list.remove(pre_check)

        if job_read_list == []:
            self.msg_writing('No jobs queued')
            exit()
        else:
            for job_read in job_read_list:
                jobtype = str(job_read[22:33].split()[0])
                jobname = str(job_read[-24:-14].split()[0])
                if jobtype in ['lsdyna', 'fluent', 'moldflow', 'abaqus']:
                    if jobname == 'abaqus':
                        continue
                    else:
                        jobname_list.append(job_read[-24:-14])
                        jobstatus_list.append(str(job_read[16:22].split()[0]))
                        jobid_list.append(str(re.findall('\d+', job_read)[0]))
                else:
                    continue
            if jobname_list == []:
                self.msg_writing('No jobs queued')
                exit()
            else:
                return jobname_list, jobstatus_list, jobid_list

    def get_statue_file(self, hpc_path_default, ssh, ip, id, pw, c_dir, cmd_1, cmd_2, jobid_list):
        files_path_list = []
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       # hpc 접속키 획득
        ssh.connect(ip, 22, id, pw)                  # 로그인 유효성 확인
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        for jobid in jobid_list:
            ssh.exec_command(cmd_1 + jobid + cmd_2 + 'bjobs_' + jobid + '.txt')
            time.sleep(5)
            sftp.get(hpc_path_default + '/' + id + '/bjobs_' + jobid + '.txt', c_dir + '\\' + 'bjobs_' + jobid + '.txt')
            time.sleep(5)
            files_path_list.append(c_dir + '\\' + 'bjobs_' + jobid + '.txt')
        return files_path_list

    def jobid_status_check(self, files_path):
        ref_string = ["PEND", "RUN", "EXIT", "UNKWN", "DONE"]
        f = open(files_path, "r")
        f_status = f.read()
        f_status_list = f_status.split()
        b3 = list(set(ref_string).intersection(f_status_list))
        b3 = (''.join(b3))
        return b3

    def send_sms(self, txt_writing, account_sid, auth_token, _to, _from):
        client = Client(account_sid, auth_token)
        message = client.messages.create(to=_to, from_=_from, body=txt_writing)

    def getlogfile(self, hpc_path_default, ssh, ip, pw, c_dir, cmd_log):
        files_path = self.get_log_file(hpc_path_default, ssh, ip, pw, c_dir, cmd_log)
        return files_path

    def run(self):
        pre_now_ = datetime.now().hour
        duration_ = 12
        if pre_now_ + duration_ >= 24:
            end_time = abs(24 - (pre_now_ + duration_))
        else:
            end_time = pre_now_ + duration_
        interval = int(self.interval)
        if interval < 60:
            interval = 60
        try:
            files_path = self.get_log_file(self.hpc_path_default, self.ssh, self.ip, self.id, self.pw, self.c_dir, self.cmd_log)
            jobname_list, jobstatus_list, jobid_list = self.jobid_check(files_path)
            i = 1
            while i > 0: 
                if jobid_list == []:
                    time.sleep(interval)
                    files_path = self.get_log_file(self.hpc_path_default, self.ssh, self.ip, self.id, self.pw, self.c_dir, self.cmd_log)
                    time.sleep(interval)
                    exit()
                else:
                    files_path_list = self.get_statue_file(self.hpc_path_default, self.ssh, self.ip, self.id, self.pw, self.c_dir, self.cmd_1, self.cmd_2, jobid_list)
                    for files_path, jobname, jobid in zip(files_path_list, jobname_list[:], jobid_list[:]):
                        b3 = self.jobid_status_check(files_path)
                        if b3 == "EXIT" or b3 == "UNKWN":
                            self.send_sms(jobname + ' has an error', self.account_sid, self.auth_token, self._to, self._from)
                            jobname_list.remove(jobname)
                            jobid_list.remove(jobid)
                            continue
                        elif b3 == 'RUN' or b3 == 'PEND':
                            continue
                        else:
                            self.send_sms(jobname + ' is finished', self.account_sid, self.auth_token, self._to, self._from)
                            jobname_list.remove(jobname)
                            jobid_list.remove(jobid)
                            continue  
                    time.sleep(interval)
                    now_ = datetime.now().hour
                    if 0 == end_time - now_:
                        i-=1
            self.finished.emit()
        except:
            self.finished.emit()

    def stop(self):
        self.power = False
        self.quit()
        self.wait(5)  


# MyThread().run()