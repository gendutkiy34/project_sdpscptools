import os
import paramiko
from general import ConvertStrtoDate,ConvertDatetoStr,GetToday,SshNode

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
    dt2=ConvertStrtoDate(tgl,'%Y-%m-%d')
    if dt1.date() == dt2.date() :
        dt_string=ConvertDatetoStr(dt2,'%Y%m%d')
        for nd in list_node :
            cmd='grep -ah {0} /opt/logs/scp_app/*{1}* '.format(trxid,dt_string)
            SshNode(host=nd['host'],user=nd['username'],pwd=nd['password'],cmd=None)

    else :
        flag=0


GetScpLog(tgl='2023-08-22')