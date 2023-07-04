'''-------------------------------------------------------------
Ble Beacon Serial Scan Program

connects as a client to the server on defined TCP_IP address

Date            Version        Developer               Comments
12/1/2019       1.0.0.0        TJG                     Inital release
02/15/2020      1.0.0.1        TJG                     Add option to use serial port for Bluetooth data

-------------------------------------------------------------'''


#import blescan
import serialreader
import sys
import socket
#import bluetooth._bluetooth as bluez
import fcntl, os
import errno
from time import sleep
import kalman as kal
import json

#TCP_IP = '192.168.127.100'
TCP_IP = '10.83.7.39'
TCP_IP2 = ''
TCP_HOST = 'STL3503W.auto.contiwan.com'

TCP_PORT = 2000
BUFFER_SIZE = 1024

MESSAGE = "Hello, Server"

'''
dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print ("ble thread started")

except:
    print ("error accessing bluetooth device...")
    sys.exit(1)
    

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)
'''
print ('starting')
#Open the serial port
ser = serialreader.Open()
if (ser == None):
    print("Unable to oper serial Port: ")
else:    
    print("Serial Opened: ")


s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Opened")
bconnected = False

try:
    TCP_IP2 = socket.gethostbyname(TCP_HOST)
    print (" IP Address from hostname found :", TCP_IP2)
    if ("10.83." in TCP_IP2):
        TCP_IP = TCP_IP2
        print (" Changing IP Address from hostname:", TCP_IP)
        
        
except socket.error:
    print('Failed to get IP address from server')

#TCP_IP = '10.198.177.128'
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

CalIn = -54
CalTemp = -54
kFilter = kal.KalmanFilter(0.008, 4)
n = 1.6
#n = 0.9

print ("Waiting for Ble connection")
while True:
    
    #bFound, Packet = serialreader.GetPacket(ser);
    if (ser != None):
        bFound, Packet = serialreader.GetPacketParse(ser, kFilter, CalIn, n, 2, g_mu, g_sig, g_accumulator, g_count)
    else:
        # If comport cannot be opened send error message and trry to reopen
        bFound = False;
        message = '\x02' + "Beacon5,v1.0,ERROR, Comport" + '\x03'
        print (message)
        if (bconnected == True):
            try:
                s.send(message.encode('ascii'))
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
                
        ser = serialreader.Open()
        if (ser == None):
            print("retry Unable to open serial Port: ")
        else:    
            print("retry Serial Opened: ")
    
    
    if bFound == True:
        message = '\x02' + "Beacon5,v1.0," + Packet + '\x03'
        print (message)
        if (bconnected == True):
            try:
            
                s.send(message.encode('ascii'))
                try:
                    data = s.recv(26)
                    print("Rx Data:% Len: ", data ,len(data))
                 #   print(len(data))
                    #if 'quit' in data:
                        #s.close()
                    #else:
                    BeaconRXData = json.loads(data)
                  #  print(BeaconRxData)
                    if BeaconRXData.get('SetCal') != None:
                        CalIn = BeaconRXData['SetCal']
                        print ("SetCal In: ",CalIn)
                     
                    if BeaconRXData.get('SetN') != None:
                        SetNIn = BeaconRXData['SetN']
                        print ("SetN: ",SetNIn)
                        n = SetNIn
                        
                    #print ("Received data", data)
                    sleep(1)
                except (BlockingIOError, socket.timeout, AttributeError, OSError):
                    #print ("Receive timeout")
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
