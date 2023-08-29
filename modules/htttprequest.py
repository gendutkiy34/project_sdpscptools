import os
import requests


def ReqHttp(urllink):
    r=requests.get(urllink)
    respcode=r.status_code
    resptext=r.text
    return respcode,resptext




