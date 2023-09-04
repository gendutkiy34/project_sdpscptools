from modules.connection import OracleCon
from modules.general import ReadJsonFile,ReadTxtFile
import json


def ReadConfig(conpath=None,condition=None,sqlraw=None):
    list_data=[]
    try :
        conn=OracleCon(conpath)
        cur=conn.cursor()
        if condition == None :
            sql='{0}'.format(sqlraw)
            data_raw=cur.execute(sql)
        else :
            sql='{0}'.format(sqlraw)
            data_raw=cur.execute(sql.format(condition=condition))
        for d in data_raw:
            list_data.append(d)
    except Exception :
        list_data=['data not found']
    return list_data


def ReadTrx(conpath=None,tgl=None,msisdn=None,hour=None,logtype=None,sqlraw=None):
    dt=tgl.split('-')
    mon=dt[1]
    day=dt[2]
    year=dt[0]
    data_raw=[]
    if str(msisdn)[0] == '0' :
        msisdn=str(msisdn)[1:]
    else :
        msisdn=str(msisdn)[2:]
    try:
        conn=OracleCon(conpath)
        cur=conn.cursor()
        data_raw=[]
        if logtype == 'scp' :
            sql=sqlraw
            trxsql=sql.format(day=day,mon=mon,hour=hour,msisdn=msisdn)
            tempdata=cur.execute(trxsql)
        else :
            sql=sqlraw
            trxsql=sql.format(day=day,mon=mon,hour=hour,msisdn=msisdn)
            tempdata=cur.execute(trxsql)
        for d in tempdata:
            data_raw.append(d)
    except Exception :
        data_raw.append('data not found')
    return data_raw