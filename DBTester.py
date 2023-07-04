# -*- coding: utf-8 -*-
"""
Created on Sun May  9 11:03:36 2021

@author: uidq9030
"""

import database as Db
from datetime import datetime
#DBclass.open_connection()

now = datetime.now()
dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
val = (dt_string, 123456, 0.6, 0.7, 0.7, 'NOK', 0.4,'test','dirtest',0,'result1 sdfdf','result2 scds')
print ('val:' ,val)

db = Db.database()
data = db.insert_row(val)
print (data)

#db .openclose()
#query = "SELECT * FROM aiholeandfillettopresults"
#data = db.run_query(query)
#print(data)
#val2 = '2021-05-10 12:24:06', '0320934600316036_FNT_TOP', 0.0, 0.0, 0.0, 'OK', 0.90, 'D:\\AIData\\data\\Top\\test\\OK\\0320934600316036_FNT_TOP.jpg', None, 0, ['OK', 'OK', 0.21644607, 0.78355396, 'TopRightMEMES'], ['OK', 'OK', 0.054698065, 0.945302, 'BottomLeftMEMES']
#val2 = '2021-05-10 12:24:06', '0320934600316036_FNT_TOP', 0.0, 0.0, 0.0, 'OK', 0.90, 'jpg', 'None', 0, str(['OK', 'OK', 0.21644607, 0.78355396, 'TopRightMEMES']), 'result2'

#print ('val2: ', val2)
#data = db.insert_row(val2)
#print (data)
'''
test0 = ['OK', 'OK', 0.21644607, 0.78355396, 'TopRightMEMES']
test1 = ['OK', 'OK', 0.08248541, 0.91751456, 'BottomLeftMEMES']

test0NOK = test0[2]
test0OK = test0[3]

test1NOK = test1[2]
test1OK = test1[3]
 
NOKConf = test0NOK
if (NOKConf > test1NOK):
    NOKConf = test1NOK
    
OKConf = test0OK
if (OKConf > test1OK):
    OKConf = test1OK

print (OKConf, NOKConf)

if (NOKConf > OKConf):
    OverallConf = NOKConf
else:
    OverallConf = OKConf


print (OverallConf)


#print (test0[3])


test = str(['OK', 'OK', 0.21644607, 0.78355396, 'TopRightMEMES'])

print (test, type(test))
'''