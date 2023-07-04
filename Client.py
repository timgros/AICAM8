
import socket
import json

HOST = '10.83.30.77'  # The server's hostname or IP address
#HOST  = '10.83.1.69'
PORT = 3001       # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    try:
        s.connect((HOST, PORT))
        jdata = '{"SerialNumber":"C1234567","imageUploadType":"FTP","IPAddress":"172.20.15.100","user":"picam","password":"picam","Prediction":"PASS","NOKConfidence":-1.0,"OKConfidence":-1.0,"strFileLocation":"D:/AIData/data/test.jpg","strModelLocation":"D:/AIData/data/alexnet.onnx","strModelName":"RangerHScrewE88.onnx"}'
        json_string = json.dumps(jdata)
        #print (json_string)

        # Conver to json
        obj= json.loads(json_string)
        
        #s.sendall(b'Hello, world')
        s.sendall(obj.encode('ascii'))
        
        #data = s.recv(1024)
        data = s.recv(100)
        print('Received', repr(data))
    except Exception as e:
     print ("Exception: Client() in level argument",e.args[0])

    finally:
        print ("Closing Connection")
        s.close()    

