from connection import OracleCon
from general import ReadJsonFile,ReadTxtFile
import json


def ReadConfig(conpath=None,condition=None,sqlraw=None):
    try :
        conn=OracleCon(conpath)
        cur=conn.cursor()
        if condition == None :
            sql='{0}'.format(sqlraw)
            data_raw=cur.execute(sql)
        else :
            sql='{0}'.format(sqlraw)
            data_raw=cur.execute(sql.format(condition=condition))
    except Exception :
        data_raw=['data not found']
    sql="{0}".format(sqlraw)
    data_raw=cur.execute(sql.format(condition=condition))
    return data_raw


def ReadTrx(conpath=None,tgl=None,msisdn=None,hour=None,logtype=None,sqlraw=None):
    dt=tgl.split('-')
    mon=dt[1]
    day=dt[2]
    year=dt[0]
    if str(msisdn)[0] == '0' :
        msisdn=str(msisdn)[1:]
    else :
        msisdn=str(msisdn)[2:]
    try:
        conn=OracleCon(conpath)
        cur=conn.cursor()
        if logtype == 'scp' :
            sql=sqlraw
            trxsql=sql.format(day=day,mon=mon,hour=hour,msisdn=msisdn)
            data_raw=cur.execute(trxsql)
        else :
            sql=sqlraw
            trxsql=sql.format(day=day,mon=mon,hour=hour,msisdn=msisdn)
            data_raw=cur.execute(trxsql)
    except Exception :
        data_raw=['data not found']
    return data_raw