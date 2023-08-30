import os
from flask import Flask,render_template,url_for,redirect,request
from modules.general import ReadJsonFile,ReadTxtFile,ConvertListToDict
from formapp import FormHttpReq,FormLog,FormCdr,FormCpId
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog
from modules.sdplog import GetSdpLog
from modules.ReadSdpLog import ExtractScmLog
from modules.DbQuery import ReadConfig,ReadTrx
from modules.general import ConvertListToDict
from modules.extractcdr import ExtractCdrSdp


dbcon=('./connections/sdpprodtrx.json')
sqltxt=ReadTxtFile('./sql/sdptrx.sql')
temptrxs=ReadTrx(conpath=dbcon,tgl='2023-08-30',msisdn='89668399434',hour='09',logtype='scp',sqlraw=sqltxt)

list_key=["CDRTIME","TASKID ","CLIENTTRANSACTIONID","TRANSACTIONID","APARTY","BASICCAUSE",
                      "INTERNALCAUSE","CALLCHARGE","OFFERCODE","CP_NAME","CONTENTPROVIDERID","NETWORKMODE",
                      "SHORTCODE ","KEYWORD ","CATEGORYID","THIRDPARTYERRORCODE"]
list_trx=ConvertListToDict(listkey=list_key,listvalue=temptrxs)
list_trx_clean=ExtractCdrSdp(listdict=list_trx)

for t in list_trx_clean:
    print('\n',t,'\n')



