import re
# from numpy import append
import paramiko
import time
import os
from twilio.rest import Client

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

def msg_writing(msg):
    f = open(msg, 'w', encoding='utf-8')     # txt파일 생성
    f.close()

def get_log_file(hpc_path_default, ssh, ip, pw, c_dir, cmd_log):
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
        msg_writing('No log file on HPC')
        exit()

def jobid_check(files_path):    
    job_read_list = open(files_path, "r").readlines()[1:]
    for pre_check in job_read_list[:]:
        if pre_check[0:8].split() == []:
            job_read_list.remove(pre_check)

    if job_read_list == []:
        msg_writing('No jobs queued')
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
            msg_writing('No jobs queued')
            exit()
        else:
            return jobname_list, jobstatus_list, jobid_list

def get_statue_file(hpc_path_default, ssh, ip, pw, c_dir, cmd_1, cmd_2, jobid_list):
    files_path_list = []
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())       # hpc 접속키 획득
    ssh.connect(ip, 22, id, pw)                  # 로그인 유효성 확인
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    for jobid in jobid_list:
        ssh.exec_command(cmd_1 + jobid + cmd_2 + 'bjobs_' + jobid + '.txt')
        time.sleep(1)
        sftp.get(hpc_path_default + '/' + id + '/bjobs_' + jobid + '.txt', c_dir + '\\' + 'bjobs_' + jobid + '.txt')
        files_path_list.append(c_dir + '\\' + 'bjobs_' + jobid + '.txt')
    return files_path_list

def jobid_status_check(files_path):
    ref_string = ["PEND", "RUN", "EXIT", "UNKWN", "DONE"]
    f = open(files_path, "r")
    f_status = f.read()
    f_status_list = f_status.split()
    b3 = list(set(ref_string).intersection(f_status_list))
    b3 = (''.join(b3))
    return b3

def send_sms(txt_writing, account_sid, auth_token, _to, _from):
    client = Client(account_sid, auth_token)
    message = client.messages.create(to=_to, from_=_from, body=txt_writing)

cmd_log = '. /etc/profile;. ~/.bash_profile;. ~/.bashrc; bjobs 2>&1 > _log_.txt' 
cmd_1 = '. /etc/profile;. ~/.bash_profile;. ~/.bashrc; bjobs '
cmd_2 = ' 2>&1 > ' 

def getlogfile():
    files_path = get_log_file(hpc_path_default, ssh, ip, pw, c_dir, cmd_log)
    return files_path

def excute_program(interval):
    interval = int(interval)
    if interval < 60:
        interval = 60
    try:
        files_path = get_log_file(hpc_path_default, ssh, ip, pw, c_dir, cmd_log)
        jobname_list, jobstatus_list, jobid_list = jobid_check(files_path)
        i = 1; endsensor = 3600*12
        while i > 0: 
            if jobid_list == []:
                time.sleep(interval)
                files_path = get_log_file()
                time.sleep(interval)
                exit()
            else:
                files_path_list = get_statue_file(hpc_path_default, ssh, ip, pw, c_dir, cmd_1, cmd_2, jobid_list)
                for files_path, jobname, jobid in zip(files_path_list, jobname_list[:], jobid_list[:]):
                    b3 = jobid_status_check(files_path)
                    if b3 == "EXIT" or b3 == "UNKWN":
                        send_sms(jobname + ' has an error', account_sid, auth_token, _to, _from)
                        jobname_list.remove(jobname)
                        jobid_list.remove(jobid)
                        continue
                    elif b3 == 'RUN' or b3 == 'PEND':
                        continue
                    else:
                        send_sms(jobname + ' is finished', account_sid, auth_token, _to, _from)
                        jobname_list.remove(jobname)
                        jobid_list.remove(jobid)
                        continue  
                time.sleep(interval)
                endsensor -= interval
                if 0 > endsensor - interval:
                    i-=1
    except:
        exit()

# interval = '60'
# excute_program(interval)
