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
        trxsql=sql.format(day=day,cdrtype=None,mon=mon)
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
            list_bmo_attempt=[]
            list_bmt_attempt=[]
            list_dig_attempt=[]
            list_smo_attempt=[]
            list_smt_attempt=[]
            list_bmo_success=[]
            list_bmt_success=[]
            list_dig_success=[]
            list_smo_success=[]
            list_smt_success=[]
            list_bmo_bsf=[]
            list_bmt_bsf=[]
            list_dig_bsf=[]
            list_smo_bsf=[]
            list_smt_bsf=[]
            for data in tempdata:
                list_hour.append(data[1])
                list_bmo_attempt.append(data[2])
                list_bmt_attempt.append(data[6])
                list_dig_attempt.append(data[10])
                list_smo_attempt.append(data[14])
                list_smt_attempt.append(data[18])
                list_bmo_success.append(data[3])
                list_bmt_success.append(data[7])
                list_dig_success.append(data[11])
                list_smo_success.append(data[15])
                list_smt_success.append(data[19])
                list_bmo_bsf.append(data[4])
                list_bmt_bsf.append(data[8])
                list_dig_bsf.append(data[12])
                list_smo_bsf.append(data[16])
                list_smt_bsf.append(data[20])
            list_data=[list_hour,list_bmo_attempt,list_bmt_attempt,list_dig_attempt,list_smo_attempt,
                       list_smt_attempt,list_bmo_success,list_bmt_success,list_dig_success,
                       list_smo_success,list_smt_success,list_bmo_bsf,list_bmt_bsf,list_dig_bsf,
                       list_smo_bsf,list_smt_bsf]
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
    

