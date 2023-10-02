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
    flag_scp=""
    flag_bulk=""
    flag_dig=""
    flag_subs=""
    nflag=False
    today=GetToday()
    dt_string=ConvertDatetoStr(today,'%Y-%m-%d')
    dbscp=('./connections/scpprodtrx.json')
    dbsdp=('./connections/sdpprodtrx.json')
    sqlscp=ReadTxtFile('./sql/scphourlytoday.sql')
    sqlbulk=ReadTxtFile('./sql/bulkservicetoday.sql')
    sqldig=ReadTxtFile('./sql/digitalservicetoday.sql')
    sqlsubs=ReadTxtFile('./sql/subscriptionservicetoday.sql')
    data_scp=GetDataToday(conpath=dbscp,tgl=dt_string,cdrtype='scp',sqlraw=sqlscp)
    if isinstance(data_scp,list) :
        flag_scp=1
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
    else :
        flag_scp=0
    data_bulk=GetDataToday(conpath=dbsdp,tgl=dt_string,cdrtype='sdp',sqlraw=sqlbulk)
    if isinstance(data_bulk,list):
        flag_bulk=1
        print('data bulk : {}'.format(len(data_bulk)))
        bmoattempt=sum(data_bulk[1])
        bmosuccess=sum(data_bulk[2])
        bmobsf=sum(data_bulk[3])
        bmosr= round(((bmosuccess+bmobsf)/bmoattempt)*100,2)
        print('bulk mo sr : {0}% , bulk mo attempt : {1} , bulk mo success = {2} , bulk mo bussines fail = {3}'.format(bmosr,bmoattempt,bmosuccess,bmobsf))
        list_bmosr=GetListSuccessRate(listattempt=data_bulk[1],listsuccess=data_bulk[2],listbsf=data_bulk[3])
        print('list bulk mo sr hourly : {}'.format(list_bmosr))
        bmtattempt=sum(data_bulk[4])
        bmtsuccess=sum(data_bulk[5])
        bmtbsf=sum(data_bulk[6])
        bmtsr= round(((bmtsuccess+bmtbsf)/bmtattempt)*100,2)
        print('bulk mt sr : {0}% , bulk mt attempt : {1} , bulk mt success = {2} , bulk mt bussines fail = {3}'.format(bmtsr,bmtattempt,bmtsuccess,bmtbsf))
        listhour=data_bulk[0]
        list_bmtsr=GetListSuccessRate(listattempt=data_bulk[1],listsuccess=data_bulk[2],listbsf=data_bulk[3])
        print('list bulk mt sr hourly : {}'.format(list_bmtsr))
    else :
        flag_bulk=0
    data_dig=GetDataToday(conpath=dbsdp,tgl=dt_string,cdrtype='sdp',sqlraw=sqldig)
    if isinstance(data_dig,list) :
        flag_dig=1
        print('data digital service : {}'.format(len(data_dig)))
        digattempt=sum(data_dig[1])
        digsuccess=sum(data_dig[2])
        digbsf=sum(data_dig[3])
        digsr= round(((digsuccess+digbsf)/digattempt)*100,2)
        print('digital sr : {0}% , digital attempt : {1} , digital success = {2} , digital bussines fail = {3}'.format(digsr,digattempt,digsuccess,digbsf))
        list_digsr=GetListSuccessRate(listattempt=data_dig[1],listsuccess=data_dig[2],listbsf=data_dig[3])
        print('list digital  sr hourly : {}'.format(list_digsr))
    else :
        flag_dig=0
    data_subs=GetDataToday(conpath=dbsdp,tgl=dt_string,cdrtype='sdp',sqlraw=sqlsubs)
    if isinstance(data_subs,list) :
        flag_subs=1
        print('data subscription : {}'.format(len(data_subs)))
        smoattempt=sum(data_subs[1])
        smosuccess=sum(data_subs[2])
        smobsf=sum(data_subs[3])
        smosr= round(((smosuccess+smobsf)/smoattempt)*100,2)
        print('subs mo sr : {0}% , subs mo attempt : {1} , subs mo success = {2} , subs mo bussines fail = {3}'.format(smosr,smoattempt,smosuccess,smobsf))
        list_smosr=GetListSuccessRate(listattempt=data_subs[1],listsuccess=data_subs[2],listbsf=data_subs[3])
        print('list subscription mo  sr hourly : {}'.format(list_smosr))
        smtattempt=sum(data_subs[4])
        smtsuccess=sum(data_subs[5])
        smtbsf=sum(data_subs[6])
        smtsr= round(((smtsuccess+smtbsf)/smtattempt)*100,2)
        print('subs mt sr : {0}% , subs mt attempt : {1} , subs mt success = {2} , subs mt bussines fail = {3}'.format(smtsr,smtattempt,smtsuccess,smtbsf))    
        list_smtsr=GetListSuccessRate(listattempt=data_subs[4],listsuccess=data_subs[5],listbsf=data_subs[6])
        print('list subscription mt  sr hourly : {}'.format(list_smtsr))
    else :
        flag_subs=0                                                                                                                                                                   
    if flag_scp == 1 and flag_bulk ==1 and flag_dig ==1 and flag_subs == 1 :
        vscr=round((vsuccess/vattempt)*100,2)  
        vbfr=round((vbsf/vattempt)*100,2)  
        vflr=round(((vattempt-(vsuccess+vbsf))/vattempt)*100,2) 
        bulkmoscr=round((bmosuccess/bmoattempt)*100,2)  
        bulkmobfr=round((bmobsf/bmoattempt)*100,2)  
        bulkmoflr=round(((bmoattempt-(bmosuccess+bmobsf))/bmoattempt)*100,2)  
        bulkmtscr=round((bmtsuccess/bmtattempt)*100,2)  
        bulkmtbfr=round((bmtbsf/bmtattempt)*100,2)  
        bulkmtflr=round(((bmtattempt-(bmtsuccess+bmtbsf))/bmtattempt)*100,2)   
        digiscr=round((digsuccess/digattempt)*100,2)
        digibfr=round((digbsf/digattempt)*100,2)
        digiflr=round(((digattempt-(digsuccess+digbsf))/digattempt)*100,2)
        subsmoscr=round((smosuccess/smoattempt)*100,2)
        subsmobfr=round((smobsf/smoattempt)*100,2) 
        subsmoflr=round(((smoattempt-(smosuccess+smobsf))/smoattempt)*100,2) 
        subsmtscr=round((smtsuccess/smtattempt)*100,2)
        subsmtbfr=round((smtbsf/smtattempt)*100,2) 
        subsmtflr=round(((smtattempt-(smtsuccess+smtbsf))/smtattempt)*100,2) 
        list_scr=[vscr,bulkmoscr,bulkmtscr,digiscr,subsmoscr,subsmtscr]
        print('list success : {}'.format(list_scr))
        list_bfr=[vbfr,bulkmobfr,bulkmtbfr,digibfr,subsmobfr,subsmtbfr]
        print('list bussiness faile : {}'.format(list_bfr))
        list_flr=[vflr,bulkmoflr,bulkmtflr,digiflr,subsmoflr,subsmtflr]
        print('list failed : {}'.format(list_flr))
        return render_template('homenew.html',voiceattempt=vattempt,voicesr=vsr,bulkmoattempt=bmoattempt,bulkmosr=bmosr,
                           bulkmtattempt=bmtattempt,bulkmtsr=bmtsr,digattempt=digattempt,digsr=digsr,
                           submoattempt=smoattempt,submosr=smosr,submtattempt=smtattempt,submtsr=smtsr,listhour=listhour,
                           listvoice=list_vsr,listbmosr=list_bmosr,listbmtsr=list_bmtsr,listdigsr=list_digsr,listsmosr=list_smosr,
                           listsmtsr=list_smtsr,listscr=list_scr,listbfr=list_bfr,listflr=list_flr)
    else :
        print('flag 0 happens')
        redirect (url_for('errorloading'))
    

@app.route('/scdconfig')
def sdpconfig():
    return render_template('baseconfigsdp.html')

@app.route('/scpconfig')
def scpconfigprod():
    return render_template('baseconfigscpprod.html')


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
    print('service : offer management ')
    flag=False
    cpoffer=""
    filter=""
    data_raw=""
    conpath="./connections/sdpprodconfig.json"
    sqltext=ReadTxtFile(pathfile="./sql/offercode.sql")
    if request.method == 'POST' :
        filter=request.form['filtertype']
        cpoffer=request.form['cpoffer']
        print('data received, filter={0} , cpoffer={1}'.format(filter,cpoffer))
        if filter == "cp" :
            condition="WHERE a.CP_ID='{}'".format(cpoffer)
        else :
            condition="WHERE a.OFFER_CODE='{}'".format(cpoffer)
        print('filter : {}'.format(condition))
        data_raw=ReadConfig(conpath=conpath,condition=condition,sqlraw=sqltext)
        print('total data : {}'.format(len(data_raw)))
        try :
            cpname=data_raw[0][0]
        except Exception :
            cpname='not found'
    if 'connection failed' not in data_raw or 'data not found' not in data_raw :
        flag=True
    return render_template('offermanagement.html',filter=filter,cpname=cpname,cpoffer=cpoffer,dataraw=data_raw)


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


@app.route('/sdclist', methods=['GET',  'POST'])
def sdclist():
    print('service : sdc list')
    status=False
    condition=''
    filter=''
    connection="./connections/sdpprodconfig.json"
    sqltext=ReadTxtFile(pathfile="./sql/sdlist.sql")
    if request.method == 'POST' :
        status=True
        filter=request.form['conditiontype']
        cpsdc=request.form['cpsdc']
        print('data received, conditiontype={0} , cpsdc={1}'.format(request.form['conditiontype'],cpsdc))
        if str(request.form['conditiontype']) == 'cp' :
            condition="WHERE a.CP_ID='{}'".format(cpsdc)
        elif str(request.form['conditiontype']) == 'sdc' :
            condition="WHERE a.MO_SHORT_CODE='{}'".format(cpsdc)
        else :
            pass
        print('condition : {}'.format(condition))
        data_raw=ReadConfig(conpath=connection,condition=condition,sqlraw=sqltext)
        try :
            cpname=data[0][0]
        except Exception :
            cpname='not found'
        print("total data : {0}".format(len(data_raw)))
    return render_template('sdclist.html',filter=filter,cpsdc=cpsdc,dataraw=data_raw)


@app.route('/normprod')
def NormalizationProd():
    print('service : normalization prod')
    dbcon=('./connections/scpprodconfig.json')
    sqltxt="SELECT * FROM SCPUSER.NORMALIZATION_RULE_MASTER  ORDER BY RULE_ID"
    data_raw=ReadConfig(conpath=dbcon,condition=None,sqlraw=sqltxt)
    print("total data : {} ".format(data_raw))
    return render_template('normprod.html',dataraw=data_raw)


@app.route('/denormprod')
def DenormalizationProd():
    print('service : denormalization prod')
    dbcon=('./connections/scpprodconfig.json')
    sqltxt="SELECT * FROM SCPUSER.NUMBER_TRANSLATION_RULE ORDER BY RULE_ID"
    data_raw=ReadConfig(conpath=dbcon,condition=None,sqlraw=sqltxt)
    print("total data : {} ".format(data_raw))
    return render_template('denormprod.html',dataraw=data_raw)


@app.route('/bftmasterprod')
def BftRuleProd():
    print('service : BFT Rule Master prod')
    dbcon=('./connections/scpprodconfig.json')
    sqltxt=ReadTxtFile(pathfile="./sql/bftrulemasterprod.sql")
    data_raw=ReadConfig(conpath=dbcon,condition=None,sqlraw=sqltxt)
    print("total data : {} ".format(data_raw))
    return render_template('bftruleprod.html',dataraw=data_raw)

@app.route('/ocsmappingprod')
def OcsMapProd():
    print('service : OCS ERROR CODE Mapping prod')
    dbcon=('./connections/scpprodconfig.json')
    sqltxt="SELECT * FROM SCPUSER.OCS_ERRORCODE_MAPPING"
    data_raw=ReadConfig(conpath=dbcon,condition=None,sqlraw=sqltxt)
    print("total data : {} ".format(data_raw))
    return render_template('ocsmapprod.html',dataraw=data_raw)
    

@app.route('/error')
def errorloading():
    return render_template('errorpage.html')

@app.route('/test')
def testpage():
    return render_template('hometest.html')



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8086')