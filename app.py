import os
from flask import Flask,render_template,url_for,redirect    
from modules.general import ReadJsonFile
from formapp import FormHttpReq,FormLog,FormCdr
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog
from modules.sdplog import GetSdpLog
from modules.ReadSdpLog import ExtractScmLog

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tO$&!|0wkamvVia0?n$NqIRVWOG'

app.app_context().push()

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
                #Extemp=ExtractScmLog(temp)
                list_txt.append(temp)  
        form.dt.data='mm/dd/yyyy'
        form.trxid.data=''
        form.logtype.data=''   
    return render_template('logtransaction.html',formlog=form,flag=flag,data=list_txt,logtype=log,trxid=trx)

@app.route('/cdr')
def cdrresult():
    return render_template('cdrtransaction.html')

@app.route('/mtsimulator', methods=['GET', 'POST'])
def MtSim():
    flag=False
    form=FormHttpReq()
    rcode=''
    rtext=''
    uri=''
    if form.validate_on_submit():
        flag=True
        if str(form.msisdn.data)[0] == 0 :
            msisdn=str(form.msisdn.data)[1:]
        else :
            msisdn=str(form.msisdn.data)[2:]
        uri="http://{0}/push?TYPE=0&MESSAGE={1}&MOBILENO={2}&ORIGIN_ADDR={3}&REG_DELIVERY=1&PASSWORD={4}&USERNAME={5}".format(form.sdpenv.data,form.msg.data,msisdn,form.sdc.data,form.passw.data,form.username.data)
        #rcode,rtext=ReqHttp(uri)
        form.sdpenv.data=''
        form.msg.data=''
        form.msisdn.data=''
        form.passw.data=''
        form.sdc.data=''
        form.username.data=''
    return render_template('simulatorform.html',formsim=form,uri=uri,http_respon_code=rcode,http_respon_text=rtext)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8086')