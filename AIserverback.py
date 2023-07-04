# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 10:53:21 2020

@author: uidq9030
"""

import sys
import os
import socket
import json
import pickle
import time
import ftp
import cameracapture
#import runonnxtopmodelYOLO as runonnx
#import database as Db
from datetime import datetime

TCP_IP = '172.20.15.104'
#TCP_IP = '0.0.0.0'

TCP_PORT = 3001
BUFFER_SIZE = 2000


#jdata = '{"Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"alexnet.onnx"}'
#jdata = '{"Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"alexnet.onnx"}'
jdata = '{"SerialNumber":"C1234567","imageUploadType":"FTP","IPAddress":"172.20.15.100","user":"picam","password":"picam","Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"RangerHScrewE88.onnx"}'


json_string = json.dumps(jdata)
#print (json_string)

# Conver to json
obj= json.loads(json_string)
#print (obj)
#print (type(obj))
#onnxclass = runonnx.onnexmodelYOLO(0.5, 0.3)    
 
print("Server Started", TCP_IP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP,TCP_PORT))
s.listen()

conn, addr = s.accept()
print("Connected address", addr)

try:

   
    
    while 1:
        data = conn.recv(BUFFER_SIZE).decode('utf-8')
      #  data = conn.recv(BUFFER_SIZE)
        if not data: break
        print ("Received data: ", data)
        print (type(data))
        
        
        # Convert to dict
        parsed_data = json.loads(data)     
    #    print (type(parsed_data))
        
        #onnxclass = runonnx.onnexmodelYOLO(0.5, 0.3)    

        
        InPrediction = parsed_data['Prediction']
        print (InPrediction) 
     
        #run the model from JSON data
         #Set return values to fail
     #   parsed_data['Prediction'] = "FAIL"
     #   parsed_data['NOKConfidence'] = -1
    #    parsed_data['OKConfidence'] = -1
      #  #imagefile = "E:/images/overrides/Overrideimages/Bottom1/14/OK/0320003200330534_FNT_BTM_1.jpg"
       # filename = r"D:\AIData\data\Top\test\NOK\0320032500340431_BK_TOP.jpg"
        filename = parsed_data['strFileLocation']
        print (filename)

        parsed_data['Prediction'] = 'NOK';
     
        start = time.time()
   
        cameracapture.Capture('/home/pi/images/image.jpg')
  #     ftp.FTPUpload(parsed_data['IPAddress'],parsed_data['user'],parsed_data['password'], parsed_data['SerialNumber'], '/home/pi/images/image.jpg')

        # Prediction,NOKConfidence,OKConfidence = AI.runonnxAI(imagefile, .6)
        #overallresult,results  = runonnx.ClassifyImage(onnxclass, filename, False, 0.7)
        #FTP image
      # if parsed_data['bFTP']:
      #      overallresult,results  = onnxclass.classifyYOLODetector (filename, False, 0.8, True)
      #  else:    
      #      overallresult,results  = onnxclass.classifyYOLODetector (filename, False, 0.8, False)


    #    print ('Results: ', overallresult,results)
    
        print ('Results: ', results[0], 'Type:', type(results[0]))
    
        #Set return values
        #if (overallresult == "OK"):
        #    Prediction = "GOOD"
            
        
        '''    
        parsed_data['Prediction'] = overallresult
        parsed_data['Results1'] = str(results[0])
        parsed_data['Results2'] = str(results[1])
       
        
        if len(results) > 1:
            NOKConf = results[0][2]
            if (NOKConf > results[1][2]):
                NOKConf = results[1][2]
            
            OKConf = results[0][3]
            if (OKConf > results[1][3]):
                OKConf = results[1][3]
        
        else:            
            NOKConf = 100
            OKConf = 0

        parsed_data['OKConfidence'] = str(OKConf)
        parsed_data['NOKConfidence'] = str(NOKConf)
  #      print ('Conflevel:', OKConf, NOKConf, type(OKConf))


        if (NOKConf > OKConf):
            OverallConf = NOKConf
        else:
            OverallConf = OKConf
        OverallConf = OKConf


      #  print (OverallConf)
        parsed_data['Score'] = str(OverallConf)
                                          
       # print (RXData["strModelLocation"])
        #obj['Prediction'] = 'FAIL'
       '''
       ''' 
        #Convert to string
        json_string = json.dumps(parsed_data)
        print (type(json_string))
        
    
        #Convert to bytes and send back
        print(type(pickle.dumps(json_string)))
        conn.sendall(pickle.dumps(json_string))
       # print('Out->', json_string)
        
        end = time.time()
        cycletime = round((end - start),2)
        print(" Time: {:.2f} ".format((end - start)), " seconds")
        '''
        
        '''
        #Log to DB
        now = datetime.now()
        dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
        val = (dt_string, parsed_data['strSerialNumber'], parsed_data['NOKConfidence'], parsed_data['OKConfidence'], parsed_data['Score'], overallresult, cycletime,parsed_data['strFileLocation'],parsed_data['strDirectory'],0,str(results[0]),str(results[1]))
        print ('Val:', val)
        db = Db.database()
        data = db.insert_row(val)
        print (data)
'''
        
        
        
except Exception as e:
     print ("Exception: classifyYOLODetector() in level argument",e.args[0], 'File:', filename)

finally:
    print ("Closing Connection")
    conn.close()
    
    
conn.close()
    
