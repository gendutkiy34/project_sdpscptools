from modules.sdplog import GetSdpLog

output=GetSdpLog(tgl='2023-08-24',trx='10182386468652577057')
list_txt=[]
for t in output:
            temp=t.replace('\n','')
            list_txt.append(temp)  
for n in list_txt:
        print(n)