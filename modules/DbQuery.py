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

def GetDataToday(conpath=None,tgl=None,cdrtype=None,sqlraw=None):
    dt=tgl.split('-')
    mon=dt[1]
    day=dt[2]
    year=dt[0]
    list_hour=[]
    list_data=[]
    try :
        conn=OracleCon(conpath)
        cur=conn.cursor()
        sql=sqlraw
        trxsql=sql.format(day=day,mon=mon)
        tempdata=cur.execute(trxsql)
        if cdrtype == "scp" :
            list_nr_attempt=[]
            list_r_attempt=[]
            list_nr_success=[]
            list_r_success=[]
            list_nr_bsf=[]
            list_r_bsf=[]
            for data in tempdata:
                list_hour.append(data[1])
                list_nr_attempt.append(data[2])
                list_r_attempt.append(data[6])
                list_nr_success.append(data[3])
                list_r_success.append(data[7])
                list_nr_bsf.append(data[4])
                list_r_bsf.append(data[8])
            list_data=[list_hour,list_nr_attempt,list_r_attempt,list_nr_success,
                       list_r_success,list_nr_bsf,list_r_bsf]
        elif cdrtype == "sdp" :
            temp_list=[]
            for d in tempdata:
                temp_list.append(d)
            list_xmo_attempt=[]
            list_xmt_attempt=[]
            list_dig_attempt=[]
            list_xmo_success=[]
            list_xmt_success=[]
            list_dig_success=[]
            list_xmo_bsf=[]
            list_xmt_bsf=[]
            list_dig_bsf=[]
            if len(temp_list[0]) > 6 :
                for data in temp_list:
                    list_hour.append(data[1])
                    list_xmo_attempt.append(data[2])
                    list_xmt_attempt.append(data[6])
                    list_xmo_success.append(data[3])
                    list_xmt_success.append(data[7])
                    list_xmo_bsf.append(data[4])
                    list_xmt_bsf.append(data[8])
                list_data=[list_hour,list_xmo_attempt,list_xmo_success,list_xmo_bsf,
                           list_xmt_attempt,list_xmt_success,list_xmt_bsf]
            else :
                for data in temp_list:
                    list_hour.append(data[1])
                    list_dig_attempt.append(data[2])
                    list_dig_success.append(data[3])
                    list_dig_bsf.append(data[4])
                list_data=[list_hour,list_dig_attempt,list_dig_success,list_dig_bsf]
    except Exception :
        pass
    return list_data

def GetListSuccessRate(listattempt=None,listsuccess=None,listbsf=None):
    list_sr=[]
    for a,s,b in zip(listattempt,listsuccess,listbsf):
        try :
            sr=round(((s+b)/a)*100,2)
        except Exception :
            sr=100
        list_sr.append(sr)
    return list_sr
    

