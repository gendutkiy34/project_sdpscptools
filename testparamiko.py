import paramiko

cmd = "hostnamectl"

# Update the next three lines with your
# server's information

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
    print(t)
client.close()