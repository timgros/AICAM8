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
#import ftp
import cameracapture
#import runonnxtopmodelYOLO as runonnx
#import database as Db
from datetime import datetime

#TCP_IP = '172.20.15.104'
#TCP_IP = '10.83.7.26'
TCP_IP = '192.168.0.144'
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


try:

   
    
    while True:
        print("Waiting For Connection")

        conn, addr = s.accept()
        
        try:
       
            print("Connected address Client:", addr)
            cameracapture.resolution=(1024, 1024)
            cameracapture.Capture('/home/pi/images/image.jpg')
              
            file = open('/home/pi/images/image.jpg', 'rb')
            image_data = file.read()
             
            conn.send(image_data)
            print('File sent : ')
            file.close()
         
        finally:
            conn.close()
        
        
except Exception as e:
     print ("Exception: AIServer() in level argument",e.args[0])

finally:
    print ("Closing Connection")
    s.close()
    