import os
from flask import Flask,render_template,url_for,redirect,request
from modules.general import ReadJsonFile,ReadTxtFile,ConvertListToDict
from formapp import FormHttpReq,FormLog,FormCdr,FormCpId
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog
from modules.sdplog import GetSdpLog
from modules.ReadSdpLog import ExtractScmLog
from modules.DbQuery import ReadConfig,ReadTrx


dbcon=('./connections/sdpprodtrx.json')
sqltxt=ReadTxtFile('./sql/sdptrx.sql')
temptrxs=ReadTrx(conpath=dbcon,tgl='2023-08-29',msisdn='895360965930',hour='11',logtype='sdp',sqlraw=sqltxt)

for t in temptrxs:
    for x in t :
        print(x)


