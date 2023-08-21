import os
from flask import Flask,render_template,url_for,redirect    
from modules.general import ReadJsonFile
from formapp import FormHttpReq,FormLog
from modules.htttprequest import ReqHttp


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


@app.route('/transactionlog')
def trxlog():
    return render_template('logtransaction.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8086')