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
#import datetime
import shutil
import requests
from RestAPI import *
import socket
print(sys.version)


hostname = socket.gethostname()
longhostname = hostname+'.st.us.int.vitesco.com'
print(longhostname)

ip = socket.gethostbyname(longhostname)
print(hostname, ip)
#TCP_IP = '172.20.15.104'
#TCP_IP = '10.83.30.77'
TCP_IP = ip
#TCP_IP = '192.168.0.5'
#TCP_IP = '0.0.0.0'

TCP_PORT = 3001
BUFFER_SIZE = 2000

picPath = "/home/pi/images/"
imagefile = '/home/pi/images/image.jpg'

#jdata = '{"Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"alexnet.onnx"}'
#jdata = '{"Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"alexnet.onnx"}'
jdata = '{"SerialNumber":"C1234567","imageUploadType":"FTP","IPAddress":"172.20.15.100","user":"picam","password":"picam","Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"None"}'
#jdata = '{"SerialNumber":"C1234567","strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"RangerHScrewE88.onnx"}'


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

            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            if data:
                #print ("Received data: ", data)
                #print (type(data))
            
                # Convert to dict
                parsed_data = json.loads(data)     
                #    print (type(parsed_data))
            
      
                SerialNumber = parsed_data['SerialNumber']
                print (SerialNumber)
                cameracapture.resolution=(1024, 1024)
                cameracapture.rotation = 90
                currentTime = datetime.now()
                cameracapture.Capture(imagefile)
                
                #DO AI on image here 
                                            
                newfile = ftp.FTPUpload('10.83.52.29','aicam8','aicam8', SerialNumber, imagefile)
                #Read in image and stream to client
                file_size = os.path.getsize('/home/pi/images/image.jpg')
                #print("File Size is :", file_size, "bytes")
              
                #jsonresp = ClassifyImage('10.83.106.106:5000/classifyYOLOv7', "/home/pi/images/image.jpg")
                jsonresp = ClassifyImage('10.83.52.29:5001/classifyYOLOv7', "/home/pi/images/image.jpg")
                
                
                jsonresp['SerialNumber'] = SerialNumber
                jsonresp['strFileName'] = newfile;
                jsonresp['strModelName'] = parsed_data['strModelName'];
                
                jsonresp['imglocation'] = "/home/pi/images/image.jpg";
                #print(jsonresp['SerialNumber'])
                #print ('Response' , jsonresp)
                
  #"Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"RangerHScrewE88.onnx"}'
                
                results = jsonresp['Result']
                print(results)
               # index = results.find(':')
               # if (index > 0):
              #      parsed_data['Prediction'] = results[0:index]
                
             #   index2 = results.find('GCnt')
              #  if (index2 > 0):
                #    parsed_data['Confidence'] = results[index:index2]
                   
             #   print(parsed_data['Prediction'],parsed_data['Confidence'])
               # jresults = json.dump(results)
                #print(jresults['Result'])
                
                 #Convert to string
              #  parsed_data['SerialNumber'] = SerialNumber
               # parsed_data['strFileLocation'] = newfile;
               
                json_string = json.dumps(jsonresp)
               
                #json_string = json.dumps(parsed_data)
               
               # print (type(json_string))
                
                #Convert to bytes and send image back
              #  print(type(pickle.dumps(json_string)))
                conn.sendall(pickle.dumps(json_string))
                
                print('Send :',pickle.dumps(json_string))
                #Add delay to allow tcp to finish sending data
                time.sleep(0.1)
                #image_data = file.read(2048)
 #               image_data = file.read()
                
              #  print ('File read : ',len(image_data))
                #while image_data:
#                conn.send(image_data)
                #image_data = file.read(2048)
                 #   print ('File read : ',len(image_data))
                
                
                
                
                
            else:
                print(sys.stderr, 'No more data from client:',addr)
              #  break

        finally:
            conn.close()
        
        
except Exception as e:
     print ("Exception: AIServer() in level argument",e.args[0])

finally:
    print ("Closing Connection")
    conn.close()
    s.close()
    
    
