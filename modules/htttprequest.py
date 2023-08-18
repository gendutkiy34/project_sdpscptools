import os
import requests


def ReqHttp(urllink):
    r=requests.get(urllink)
    respcode=r.status_code
    resptext=r.text
    return respcode,resptext


"""
#TESTING
uri="http://10.64.30.95:9480/push?TYPE=0&MESSAGE=TEST%20MT&MOBILENO=6289684005222&ORIGIN_ADDR=KUNCIE&REG_DELIVERY=1&PASSWORD=tegraM12&USERNAME=SD_210903_0080"
rcode,rtext=ReqHttp(uri)
print(rcode)
print(rtext)
"""