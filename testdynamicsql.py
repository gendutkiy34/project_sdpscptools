import os

basedir=os.path.abspath(os.path.dirname(__file__))
with open('{0}/sqltest.sql'.format(basedir),'r')as f:
    sqlraw=f.read()
txt=sqlraw.format(namasiswa='andi')
print(txt)