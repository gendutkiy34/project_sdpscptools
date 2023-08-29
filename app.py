import os
from flask import Flask,render_template,url_for,redirect,request
from modules.general import ReadJsonFile,ReadTxtFile,ConvertListToDict
from formapp import FormHttpReq,FormLog,FormCdr,FormCpId
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog
from modules.sdplog import GetSdpLog
from modules.ReadSdpLog import ExtractScmLog
from modules.DbQuery import ReadConfig,ReadTrx

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

app.app_context().push()

list_hour=['00','01','02','03','04','05','06','08','09','10','11',
               '12','14','15','16','17','18','19','20','21','22',
               '23']

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/scpconfig')
def scpconfig():
    return render_template('baseconfigscp.html')

@app.route('/scdconfig')
def sdpconfig():
    return render_template('baseconfigsdp.html')


@app.route('/transactionlog', methods=['GET', 'POST'])
def trxlog():
    flag=False
    form = FormLog()
    list_txt=[]
    log=""
    trx="" 
    if form.validate_on_submit():
        flag=True
        log=form.logtype.data
        trx=form.trxid.data
        if log == "scp" :
            output,err=GetScpLog(tgl=form.dt.data,trxid=form.trxid.data)
            for t in output:
                temp=t.replace('\n','')
                list_txt.append(Extemp)  
        else :
            output=GetSdpLog(tgl=form.dt.data,trx=form.trxid.data)
            for t in output:
                temp=t.replace('\n','')
                xtemp=ExtractScmLog(temp)
                list_txt.append(temp)  
        form.dt.data='mm/dd/yyyy'
        form.trxid.data=''
        form.logtype.data='' 
        if len(list_txt) < 1 :
                list_txt.append('data not found')  
    return render_template('logtransaction.html',formlog=form,flag=flag,data=list_txt,logtype=log,trxid=trx)

@app.route('/cdr', methods=['GET', 'POST'])
def cdrresult():
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
        if str(request.form['msisdn'])[0] == 0 :
            msisdn="62{0}".format(str(request.form['msisdn'])[1:])
        else :
            msisdn=request.form['msisdn']
        cdrtype=request.form['cdrtype'] 
        hour=request.form['hour'] 
        date=request.form['date'] 
        if  request.form['cdrtype'] == "scp" :
            list_key=["CDR_TIMESTAMP","CALL_REFERENCE_NUMBER","TRANSACTION_ID","CALLING_PARTY","CALLED_PARTY",
                      "SUBSCRIBER_TYPE","CALL_STATUS","DIAMETER_RESULT_CODES","DIAMETER_ERROR_MESSAGE",
                      "CELL_ID","MSC_ADDRESS","VLR_ADDRESS","DIAMTER_SESSION_ID","INSTANCE_ID","CALL_TYPE",
                      "SUB_CALL_TYPE","IS_ROAMING","IS_CHARGING_OVERRULED","ISBFT","CALL_START_TIME",
                      "CALL_DISCONNECTING_TIME","CALL_DURATION","NORMALISED_NUMBER","TRANSLATED_NUMBER",
                      "SERVICE_KEY","IS_FOC"]
            dbcon=('./connections/scpprodtrx.json')
            sqltxt=ReadTxtFile('./sql/scptrx.sql')
            trxs=ReadTrx(conpath=dbcon,tgl=date,msisdn=msisdn,hour=hour,logtype=request.form['cdrtype'],sqlraw=sqltxt)
        else :
            pass
    if len(trxs) > 0 :
        list_trx=ConvertListToDict(listkey=list_key,listvalue=trxs)
    else :
        list_trx.append('data not found')
    return render_template('cdrtransaction.html',list_hour=list_hour,cdrs=cdrtype ,msisdns=msisdn,hours=hour,dates=date,status=status,listtrx=list_trx)

@app.route('/mtsimulator', methods=['GET', 'POST'])
def MtSim():
    status=False
    rcode=''
    rtext=''
    uri=''
    msisdn=''
    if request.method == 'POST' :
        status=True
        if request.form['env'] == 'prod' :
            serv='192.168.86.208:9003'
        elif request.form['env'] == 'sit'  :
            serv='10.64.30.95:9480'
        else :
            serv='xxxx'
        if str(request.form['msisdn'])[0] == 0 :
            msisdn=str(request.form['msisdn'])[1:]
        else :
            msisdn=str(request.form['msisdn'])[2:]
        uri="http://{0}/push?TYPE=0&MESSAGE={1}&MOBILENO={2}&ORIGIN_ADDR={3}&REG_DELIVERY=1&PASSWORD={4}&USERNAME={5}".format(serv,request.form['message'],msisdn,request.form['shortcode'],request.form['password'],request.form['systemid'])
        rcode,rtext=ReqHttp(uri)
    return render_template('simulatorform.html',status=status,msisdn=msisdn,uri=uri,http_respon_code=rcode,http_respon_text=rtext)

@app.route('/sdpconfig', methods=['GET', 'POST'])
def SdpConfig():
    return render_template('baseconfigsdp.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8086')