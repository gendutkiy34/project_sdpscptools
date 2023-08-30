import os
import paramiko
from modules.general import ConvertStrtoDate,ConvertDatetoStr,GetToday,SshNode

list_node=[
    {"nodename":"jktpkpscplog01",
     "host":"10.64.88.126",
     "username":"scpuser",
     "password":"0neT1meP@55"},
    {"nodename":"jktmmpscplog01",
     "host":"10.64.65.197",
     "username":"scpuser",
     "password":"0neT1meP@55"}
]
def GetScpLog(tgl=None,trxid=None):
    dt1=GetToday()
    dt2=ConvertStrtoDate(str(tgl),'%Y-%m-%d')
    if dt1.date() == dt2.date() :
        for nd in list_node :
            cmd=''
            SshNode(host=nd['host'],user=nd['username'],pwd=nd['password'],cmd=None)
    else :
        flag=0
        dt_string=ConvertDatetoStr(dt2,'%Y-%m-%d')
        for nd in list_node :
            cmd='ls -ltr /opt/logs/scp_app | grep {0}'.format(dt_string)
            stdout,sterr=SshNode(host=nd['host'],user=nd['username'],pwd=nd['password'],cmd=cmd)
    return stdout,sterr