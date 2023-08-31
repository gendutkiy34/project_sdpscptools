import os
from flask import Flask,render_template,url_for,redirect,request
from modules.general import ReadJsonFile,ReadTxtFile,ConvertListToDict
from formapp import FormHttpReq,FormLog,FormCdr,FormCpId
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog,ExtractScpLog
from modules.sdplog import GetSdpLog
from modules.ReadSdpLog import ExtractScmLog
from modules.DbQuery import ReadConfig,ReadTrx
from modules.general import ConvertListToDict
from modules.extractcdr import ExtractCdrSdp

tempresult=GetScpLog(tgl='2023-08-31',trxid='542834968')
result=ExtractScpLog(list_log=tempresult)
for t in result:
    print(t)


