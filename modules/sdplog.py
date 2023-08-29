import os
import paramiko
from modules.general import ConvertStrtoDate,ConvertDatetoStr,GetToday,SshNode

list_node=[
    {"nodename":"jktmmpsdplog01",
     "host":"10.64.27.85",
     "username":"sdpuser",
     "password":"0neT1meP@55"},
    {"nodename":"jktpkpsdplog01",
     "host":"10.64.84.107",
     "username":"sdpuser",
     "password":"0neT1meP@55"}
]


def GetSdpLog(tgl=None,trx=None):
    basedir='/logs01/SCM'
    dt1=GetToday()
    dt2=ConvertStrtoDate(str(tgl),'%Y-%m-%d')
    if dt1.date() == dt2.date() :
        flag=1
        cmd="grep -ah {0} {1}/*{2}*".format(trx,basedir,tgl)
    else :
        flag=0
        cmd="zgrep -ah {0} {1}/backup/*{2}*".format(trx,basedir,tgl)
    stdout,sterr=SshNode(host=list_node[0]['host'],user=list_node[0]['username']
                                 ,pwd=list_node[0]['password'],cmd=cmd)
    return stdout




