import os
from flask import Flask,render_template,url_for,redirect    
from modules.general import ReadJsonFile
from formapp import FormHttpReq,FormLog
from modules.htttprequest import ReqHttp
from modules.scplog import GetScpLog

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
        output,err=GetScpLog(tgl=form.dt.data,trxid=form.trxid.data)
        for t in output:
            temp=t.replace('\n','')
            list_txt.append(temp)  
        form.dt.data='mm/dd/yyyy'
        form.trxid.data=''
        form.logtype.data=''   
    return render_template('logtransaction.html',formlog=form,flag=flag,data=list_txt,logtype=log,trxid=trx)

@app.route('/logresult')
def resultlog():
    return render_template('logresult.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8086')