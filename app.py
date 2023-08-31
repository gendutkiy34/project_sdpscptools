import os
from flask import Flask,render_template,url_for,redirect,request
from modules.general import ReadJsonFile,ReadTxtFile,ConvertListToDict
from formapp import FormHttpReq,FormLog,FormCdr,FormCpId
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog,ExtractScpLog
from modules.sdplog import GetSdpLog
from modules.ReadSdpLog import ExtractScmLog
from modules.DbQuery import ReadConfig,ReadTrx
from modules.extractcdr import ExtractCdrSdp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

app.app_context().push()

list_hour=['00','01','02','03','04','05','06','08','09','10','11',
               '12','14','15','16','17','18','19','20','21','22',
               '23']

@app.route('/')
def index():
    return render_template('home.html')


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


@app.route('/cpconfig')
def cpconfig():
    return render_template('cpconfig.html')


@app.route('/sdc')
def sdclist():
    return render_template('baseconfigsdp.html')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8086')