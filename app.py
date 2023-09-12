import os
from flask import Flask,render_template,url_for,redirect,request
from modules.general import ReadJsonFile,ReadTxtFile,ConvertListToDict,GetToday,ConvertDatetoStr,Sum2list
from formapp import FormHttpReq,FormLog,FormCdr,FormCpId
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog,ExtractScpLog
from modules.sdplog import GetSdpLog
from modules.ReadSdpLog import ExtractScmLog
from modules.DbQuery import ReadConfig,ReadTrx,GetDataToday,GetListSuccessRate
from modules.extractcdr import ExtractCdrSdp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

app.app_context().push()

list_hour=['00','01','02','03','04','05','06','08','09','10','11',
               '12','14','15','16','17','18','19','20','21','22',
               '23']



@app.route('/')
def index():
    print('service : index')
    list_bmosr=[]
    list_bmtsr=[]
    list_digsr=[]
    list_smosr=[]
    list_smtsr=[]
    list_vsr=[]
    list_vsucc=[]
    list_vbsf=[]
    today=GetToday()
    dt_string=ConvertDatetoStr(today,'%Y-%m-%d')
    dbscp=('./connections/scpprodtrx.json')
    dbsdp=('./connections/sdpprodtrx.json')
    sqlscp=ReadTxtFile('./sql/scphourlytoday.sql')
    sqlsdp=ReadTxtFile('./sql/sdphourlytoday.sql')
    data_scp=GetDataToday(conpath=dbscp,tgl=dt_string,cdrtype='scp',sqlraw=sqlscp)
    print('data scp : {}'.format(len(data_scp)))
    vattempt=sum(data_scp[1]) + sum(data_scp[2])
    vsuccess=sum(data_scp[3]) + sum(data_scp[4])
    vbsf=sum(data_scp[5])+sum(data_scp[6])
    vsr=round(((vsuccess+vbsf) /vattempt )*100,2)
    list_vsucc=Sum2list(list1=data_scp[3],list2=data_scp[4])
    list_vbsf=Sum2list(list1=data_scp[5],list2=data_scp[6])
    print('voice sr : {3}% , voice attempt : {0} , voice success = {1} , voice bussines fail = {2}'.format(vattempt,vsuccess,vbsf,vsr))
    list_vsr=GetListSuccessRate(listattempt=data_scp[1],listsuccess=list_vsucc,listbsf=list_vbsf)
    print('total data sr scp : {0}'.format(len(list_vsr)))
    data_sdp=GetDataToday(conpath=dbsdp,tgl=dt_string,cdrtype='sdp',sqlraw=sqlsdp)
    print('data sdp : {}'.format(len(data_sdp)))
    bmoattempt=sum(data_sdp[1])
    bmosr= round(((sum(data_sdp[6])+sum(data_sdp[9]) )/bmoattempt)*100,2)
    bmtattempt=sum(data_sdp[2])
    bmtsr= round(((sum(data_sdp[7])+sum(data_sdp[12]) )/bmtattempt)*100,2)
    print('bulk_mo sr : {1}% , bulk_mo attempt : {0} , bulk_mt sr = {3} , bulk_mt attempt= {2}'.format(bmoattempt,bmosr,bmtattempt,bmtsr))
    digattempt=sum(data_sdp[3])
    digsr= round(((sum(data_sdp[8])+sum(data_sdp[13]) )/digattempt)*100,2)
    print('digital_service sr : {1}% , bulk_mo attempt : {0}'.format(digattempt,digsr))
    smoattempt=sum(data_sdp[14])
    smosr= round(((sum(data_sdp[9])+sum(data_sdp[14]) )/smoattempt)*100,2)
    smtattempt=sum(data_sdp[5])
    smtsr= round(((sum(data_sdp[10])+sum(data_sdp[15]) )/smtattempt)*100,2)
    print('subscription_mo sr : {1}% , subscription_mo attempt : {0} , subscription_mt sr = {1} , subscription_mt attempt= {2}'.format(smoattempt,smosr,smtattempt,smtsr))
    list_bmosr=GetListSuccessRate(listattempt=data_sdp[1],listsuccess=data_sdp[6],listbsf=data_sdp[11])
    list_bmtsr=GetListSuccessRate(listattempt=data_sdp[2],listsuccess=data_sdp[7],listbsf=data_sdp[12])
    list_digsr=GetListSuccessRate(listattempt=data_sdp[3],listsuccess=data_sdp[8],listbsf=data_sdp[13])
    list_smosr=GetListSuccessRate(listattempt=data_sdp[4],listsuccess=data_sdp[9],listbsf=data_sdp[14])
    list_smtsr=GetListSuccessRate(listattempt=data_sdp[5],listsuccess=data_sdp[10],listbsf=data_sdp[15])
    print('total data list_bmosr : {0} , total data list_bmtsr : {1} , total data list_digsr : {2} , total data list_smosr : {3} , total data list_smtsr : {4}'.format(len(list_bmosr),len(list_bmtsr),
                                                                                                                                                                       len(list_digsr),len(list_smosr),
                                                                                                                                                                       len(list_smtsr)))
    return render_template('homenew.html',voiceattempt=vattempt,voicesr=vsr,bulkmoattempt=bmoattempt,bulkmosr=bmosr,
                           bulkmtattempt=bmtattempt,bulkmtsr=bmtsr,digattempt=digattempt,digsr=digsr,
                           submoattempt=smoattempt,submosr=smosr,submtattempt=smtattempt,submtsr=smtsr,listhour=list_hour,
                           listvoice=list_vsr,listbmosr=list_bmosr,listbmtsr=list_bmtsr,listdigsr=list_digsr,listsmosr=list_bmosr,
                           listsmtsr=list_smtsr)

@app.route('/scdconfig')
def sdpconfig():
    return render_template('baseconfigsdp.html')

@app.route('/scpconfig')
def scpconfig():
    return render_template('baseconfigscp.html')


@app.route('/transactionlog', methods=['GET', 'POST'])
def trxlog():
    print('service : log transaction')
    flag=False
    list_txt=[]
    logtype=""
    trxid=""
    date=""
    restext=''
    if request.method == 'POST' :
        flag=True
        logtype=request.form['logtype'] 
        trxid=request.form['trxid'] 
        date=request.form['date'] 
        print('data received : ',trxid,',',date,',',logtype)
        if logtype == 'scp' :
            restext=GetScpLog(tgl=date,trxid=trxid)
            list_txt=ExtractScpLog(list_log=restext)
        else :
            list_txt=GetSdpLog(tgl=date,trxid=trxid)
    nlines=len(list_txt)
    print("result log : ",nlines)
    return render_template('logtransaction.html',flag=flag,data=list_txt,logtype=logtype,trxid=trxid,total=nlines)


@app.route('/cdr', methods=['GET',  'POST'])
def cdrresult():
    print('service : cdr transaction')
    status=False
    cdrtype=''
    msisdn=''
    hour=''
    date=''
    trxs=[]
    temptrxs=''
    list_trx=[]
    if request.method == 'POST' :
        status=True
        if str(request.form['msisdn'])[0] == '0' :
            msisdn2=str(request.form['msisdn'])[1:]
        elif str(request.form['msisdn'])[:2] == '62':
            msisdn2=str(request.form['msisdn'])[2:]
        else :
            msisdn2=str(request.form['msisdn'])[2:]
        cdrtype=request.form['cdrtype'] 
        hour=request.form['hour'] 
        date=request.form['date'] 
        msisdn=request.form['msisdn']
        print('data received : ',msisdn ,',',date,',',hour,',',cdrtype,)
        if  request.form['cdrtype'] == "scp" :
            list_key=["CDR_TIMESTAMP","CALL_REFERENCE_NUMBER","TRANSACTION_ID","CALLING_PARTY","CALLED_PARTY",
                      "SUBSCRIBER_TYPE","CALL_STATUS","DIAMETER_RESULT_CODES","DIAMETER_ERROR_MESSAGE",
                      "CELL_ID","MSC_ADDRESS","VLR_ADDRESS","DIAMTER_SESSION_ID","INSTANCE_ID","CALL_TYPE",
                      "SUB_CALL_TYPE","IS_ROAMING","IS_CHARGING_OVERRULED","ISBFT","CALL_START_TIME",
                      "CALL_DISCONNECTING_TIME","CALL_DURATION","NORMALISED_NUMBER","TRANSLATED_NUMBER",
                      "SERVICE_KEY","IS_FOC"]
            dbcon=('./connections/scpprodtrx.json')
            sqltxt=ReadTxtFile('./sql/scptrx.sql')
            trxs=ReadTrx(conpath=dbcon,tgl=date,msisdn=msisdn2,hour=hour,logtype=request.form['cdrtype'],sqlraw=sqltxt)
            print('data process in scp : ',msisdn2 ,',',date,',',hour,',',cdrtype)
        elif  request.form['cdrtype'] == "sdp" : 
            list_key=["CDRTIME","TASKID ","CLIENTTRANSACTIONID","TRANSACTIONID","APARTY","BASICCAUSE",
                      "INTERNALCAUSE","CALLCHARGE","OFFERCODE","CP_NAME","CONTENTPROVIDERID","NETWORKMODE",
                      "SHORTCODE ","KEYWORD ","CATEGORYID","THIRDPARTYERRORCODE"]
            dbcon=('./connections/sdpprodtrx.json')
            sqltxt=ReadTxtFile('./sql/sdptrx.sql')
            trxs=ReadTrx(conpath=dbcon,tgl=date,msisdn=msisdn2,hour=hour,logtype=request.form['cdrtype'],sqlraw=sqltxt)
            print('data process in sdp : ',msisdn2 ,',',date,',',hour,',',cdrtype)
        else :
            print('data not process: ',msisdn2 ,',',date,',',hour,',',cdrtype)
        if len(trxs) > 0 :
          if request.form['cdrtype'] == "sdp" :
            templist=ConvertListToDict(listkey=list_key,listvalue=trxs)
            list_trx=ExtractCdrSdp(listdict=templist)
          elif request.form['cdrtype'] == "scp" : 
            list_trx=ConvertListToDict(listkey=list_key,listvalue=trxs)
          else :
            pass
        else :
          pass
        print(list_trx)
    nlines=len(list_trx)
    return render_template('cdrtransaction.html',list_hour=list_hour,cdrs=cdrtype ,msisdns=msisdn,hours=hour,dates=date,status=status,listtrx=list_trx,total=nlines)


@app.route('/mtsimulator', methods=['GET', 'POST'])
def MtSim():
    status=False
    rcode=''
    rtext=''
    uri=''
    msisdn=''
    if request.method == 'POST' :
        print('data received : ',request.form['msisdn'],',',request.form['env'],',',request.form['shortcode'],',',request.form['systemid'],',',request.form['password'],',',request.form['message'])
        status=True
        if request.form['env'] == 'prod' :
            serv='192.168.86.208:9003'
        elif request.form['env'] == 'sit'  :
            serv='10.64.30.95:9480'
        else :
            serv='xxxx'
        if str(request.form['msisdn'])[0] == 0 :
            msisdn='62{}'.format(str(request.form['msisdn'])[1:])
        else :
            msisdn=str(request.form['msisdn'])
        uri="http://{0}/push?TYPE=0&MESSAGE={1}&MOBILENO={2}&ORIGIN_ADDR={3}&REG_DELIVERY=1&PASSWORD={4}&USERNAME={5}".format(serv,request.form['message'],msisdn,request.form['shortcode'],request.form['password'],request.form['systemid'])
        print('URI : ',uri)
        rcode,rtext=ReqHttp(uri)
        print('HTTP RESPOND CODE : ',rcode)
        print('SDP RESPOND : ',rtext)
    return render_template('simulatorform.html',status=status,msisdn=msisdn,uri=uri,http_respon_code=rcode,http_respon_text=rtext)

@app.route('/sdpconfig', methods=['GET', 'POST'])
def SdpConfig():
    return render_template('baseconfigsdp.html')


@app.route('/offer', methods=['GET',  'POST'])
def offermanagement():
    return render_template('baseconfigsdp.html')


@app.route('/cpconfig', methods=['GET',  'POST'])
def cpconfig():
    print('service cp config ')
    cpid=''
    flag=False
    pathfile="./connections/sdpprodconfig.json"
    if request.method == 'POST' :
        flag=True
        cp_id=request.form['cpid']
        cond="WHERE CP_ID='{0}'".format(cp_id)
        sqltext=ReadTxtFile(pathfile="./sql/cpconfig.sql")
        print('data received, cp id : '.format(cp_id))
        data=ReadConfig(conpath=pathfile,condition=cond,sqlraw=sqltext)
        try :
            cpname=data[0][0]
        except Exception :
            cpname='not found'
        print('total data : '.format(len(data)))
    return render_template('cpconfig.html',cpid=cp_id,dataraw=data,cpname=cpname,flag=flag)

@app.route('/subkeyword')
def subkeyword():
    return render_template('baseconfigsdp.html')

@app.route('/sdc')
def sdclist():
    return render_template('baseconfigsdp.html')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8086')