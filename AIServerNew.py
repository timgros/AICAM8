# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import socket
import bluetooth._bluetooth as bluez
import fcntl, os
import errno
from time import sleep
import kalman as kal
import json

TCP_IP = '192.168.127.100'

TCP_PORT = 2000
BUFFER_SIZE = 1024
MESSAGE = "Hello, Server"


dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print ("ble thread started")

except:
    print ("error accessing bluetooth device...")
    sys.exit(1)
    

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

bconnected = False

try:
    s.connect((TCP_IP, TCP_PORT))
    s.setblocking(0)
    socket.settimeout(1)
    fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
    print ("Connected to server device...")
    bconnected = True
except:
    s.close()
    print ("error connecting to server device...")
   
#Kalman settings
global g_mu;
global g_sig;


g_mu = 0.
g_sig = 1000.
global g_accumulator
global g_count

g_accumulator = 0.
g_count = 0

CalIn = -49
CalTemp = -49
kFilter = kal.KalmanFilter(0.008, 4.0)

print ("Waiting for Ble connection")
while True:
    
    returnedList = blescan.parse_events(sock, kFilter, CalIn, 2, g_mu, g_sig, g_accumulator, g_count)
    #print (returnedList)
    #print ("----------")
    for beacon in returnedList:
        message = '\x02' + "Beacon1," + beacon + '\x03'
        print (message)
        if (bconnected == True):
            try:
            
                s.send(message.encode('ascii'))
                try:
                    data = s.recv(BUFFER_SIZE)
                    #if 'quit' in data:
                        #s.close()
                    #else:
                    BeaconRXData = json.loads(data)
                    if BeaconRXData.get('Cal') != None:
                        CalIn = BeaconRXData['Cal']
                        print ("Cal: ",CalIn)
                       
                    #print ("Received data", data)
                    sleep(1)
                except (BlockingIOError, socket.timeout, AttributeError, OSError):
                    print ("Receive timeout")
                    sleep(1)
                except:
                    sleep(1)
                    print ("Receive exception")
                    
                    
                    
            except:
                print ("Connected dropped...")
                try:
                    s.close()
                    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    s.setblocking(0)
                    print ("Connected...")
                    sleep(1)
                except:
                    bconnected = False
                    #s.shutdown(2)
                    s.close()
                    print ("Unable to Connect2...")
                    sleep(1)
        else:
            try:
                print ("Try Connect...")
                s.close()
                s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                s.setblocking(0)
                sleep(1)
                bconnected = True
                print ("Connected...")
            except:
                s.close()
                bconnected = False
                print ("Unable to Connect1...")
                sleep(1)
                
   

print ("Exit", data)
