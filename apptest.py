import os
import cx_Oracle
import paramiko
from flask import Flask,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from modules.general import ReadJsonFile
from sqlalchemy import text
from formtest import FormMt

basedir=os.path.dirname(__file__)

credjson=ReadJsonFile('{0}/sdpconfig.json'.format(basedir))

oracle_connection_string = 'oracle+cx_oracle://{0}:{1}@'.format(credjson['username'],credjson['password']) + cx_Oracle.makedsn('{}'.format(credjson['host']), '{}'.format(credjson['port']), service_name='{}'.format(credjson['sid']))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = oracle_connection_string

app.config['SECRET_KEY'] = 'tO$&!|0wkamvVia0?n$NqIRVWOG'
#bootstrap = Bootstrap5(app)

db=SQLAlchemy(app)

#app.app_context().push()

@app.route('/test')
def test() :
    sqlraw=text("""SELECT CP_ID,SYSTEM_ID,CONNECTION_TYPE,PASSWORD,TPS,MAX_CONCURRENT_CONNECTION ,STATUS
FROM scmuser.SUBSCRIPTION_CP_CONNECTION WHERE CP_ID='167'""")
    dataraw = db.session.execute(sqlraw)
    list_data=[]
    for d in dataraw:
        subitem={}
        subitem['cpid']=d[0]
        subitem['systemid']=d[1]
        subitem['contype']=d[2]
        subitem['password']=d[3]
        subitem['tps']=d[4]
        subitem['concurent']=d[5]
        subitem['status']=d[6]
        list_data.append(subitem)
    return render_template('testextend.html',rawdata=list_data)

@app.route('/log')
def logcheck():
    cmd = "hostnamectl"
    host = "10.64.93.48"
    username = "sdpuser"
    password = "0neT1meP@55"
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout,_stderr = client.exec_command(cmd)
    listtxt=[]
    for t in _stdout :
        temp=t.replace('\t','')
        listtxt.append(temp)
    client.close()
    return render_template('logserver.html',txtmsg=listtxt)

@app.route('/   ')
def index():
    return render_template('indextest.html')

@app.route('/form', methods=['GET', 'POST'])
def TestForm():
    result=False
    mtform=FormMt()
    tempmsg=""
    tgl=""
    if mtform.validate_on_submit():
        result=True
        tgl=mtform.dt.data
        tempmsg="""http://{0}/push?TYPE=0&MESSAGE={1}&MOBILENO=6289684005222&ORIGIN_ADDR={2}&REG_DELIVERY=1&PASSWORD={3}&USERNAME={4}""".format(
            mtform.sdpenv.data,mtform.msg.data,mtform.sdc.data,mtform.passw.data,mtform.username.data)
        mtform.msg.data=''
        mtform.passw.data=''
        mtform.sdc.data=''
        mtform.sdpenv.data=''
        mtform.username.data=''
        mtform.dt.data=''
    return render_template('testform.html', formmt=mtform, txtmsg=tempmsg,flag=result,wkt=tgl)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='3034')
