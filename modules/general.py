import json
import os
from datetime import datetime

basedir=os.path.abspath(os.path.dirname(__file__))

def ReadJsonFile(pathfile):
    with open(pathfile,'r') as f:
        data=json.load(f)
    return data

def ConvertStrtoDate(tgl,format):
    dt=datetime.strptime(tgl,format)
    return dt

def ConvertDatetoStr(tgl,format):
    dt=datetime.strftime(tgl,format)
    return dt

def GetToday():
    dt=datetime.now()
    return dt

def SshNode(host=None,user=None,pwd=None,cmd=None):
    client =paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,username=user,password=pwd)
    stdin,stdout,stderr=client.exec_command(cmd)
    return stdour,stderr