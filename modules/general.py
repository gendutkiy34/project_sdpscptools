import json
import os

basedir=os.path.abspath(os.path.dirname(__file__))

def ReadJsonFile(pathfile):
    with open(pathfile,'r') as f:
        data=json.load(f)
    return data