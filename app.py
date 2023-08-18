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

@app.route('/test')
def test():
    return render_template('home.html')

@app.route('/log')
def logcheck():
    return render_template('home.html')

@app.route('/form', methods=['GET', 'POST'])
def Simulator():
    flag=False
    form=FormHttpReq()
    tempmsg=""
    errortext=""
    errorcode=""
    if form.validate_on_submit():
        flag=True
        tempmsg="""http://{0}/push?TYPE=0&MESSAGE={1}&MOBILENO={2}&ORIGIN_ADDR={3}&REG_DELIVERY=1&PASSWORD={4}&USERNAME={5}""".format(
            form.sdpenv.data,form.msg.data,form.msisdn.data,form.sdc.data,form.passw.data,form.username.data)
        form.msg.data=''
        form.passw.data=''
        form.sdc.data=''
        form.sdpenv.data=''
        form.username.data=''
        form.dt.data=''
        form.msisdn.data=''
        #errorcode,errortext=ReqHttp(tempmsg)
    return render_template('simulatorform.html',formsim=form,flag=flag,errcode=errorcode,errtext=errortext,txtmsg=tempmsg)

@app.route('/resultsim', methods=['GET', 'POST'])
def SimResult():
    return render_template('simulatorresult.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='5034')