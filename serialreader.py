
#import time
import serial
import unicodedata
import re
import sys
import kalman as Kal
from time import sleep

bRun = False
#counter = 0;
#n = 1.6
#n = 0.9

def Open():

    try:
        ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout=1
            )
    except:
        ser = None
        
    return ser
    

def Read(ser):
    
    
    x=ser.readline()
    
    
    print(x)
    
    return x

def Close(ser):
    ser.close()
 
def GetPacket(ser):
    
    Packet = 'None'
    count = 0
    bFound = False
    bStart = False
    strTmpPacket = ""
    start = 0
    
    ser.flushInput()
    sleep(.1)
    while (count < 5 and bFound == False):
        tmpPacket=ser.readline()
        #print ("Count", len(tmpPacket))
        strPacket = tmpPacket.decode('utf-8')
        #print (strPacket)
        if (bStart == False):
            start = strPacket.find("\x02")
          #  print('Start',strPacket, start)
            if start >= 0:
               end =   strPacket.find("\x03")
              # print('End',strPacket,end)
               if (end >= 0):
                   if end > start:
                       length = end-start
                     #  print(length)
                       strTmpPacket = strPacket
                       bFound = True
                       
                   else:
                       #Bad packet here need to reset it
                       head, sep, tail = strPacket.partition('\x03')
                       if len(tail) >= 0:
                           strTmpPacket = tail
                           start = 0
                       #    print('Reset Packet: ', strTmpPacket)
                           bStart = True
                       else:
                           strTmpPacket = ''
                     #      print('Bad Packet: ', strTmpPacket)
                           bStart = False
                       
                       #strTmpPacket = strTmpPacket + strPacket
                        
               else:
                   if bStart == False:
                       strTmpPacket = strPacket.rstrip()
                       start = 0
                       bStart = True
                   else:
                       strTmpPacket.join(strPacket)
                      
           # else:
               # print("No Start")
                  
        else:
             end =   strPacket.find("\x03")
           #  print('End2',end,strPacket,start)
             if (end >= 0):
                 if end > start:
                     length = end-start
                  #   print("lenght",length)
                     head, sep, tail = strPacket.partition('\x03')
                     strTmpPacket = strTmpPacket + head
                   #  print ('Pack join : ',strTmpPacket)
                     bFound = True
                       
                 else:
                     strTmpPacket = strTmpPacket + strPacket
                        
             else:
                 strTmpPacket = strTmpPacket + strPacket
                  
             
             
        count = count + 1      
    
    if bFound == True:
        Packet = re.sub(r'[\x00-\x1f\x7f-\x9f]]','',strTmpPacket)
        #remove 0x02 if there
        head, sep, tail = Packet.partition('\x02')
        if len(tail) >= 0:
            Packet = tail
        
        else:
            Packet = head
        
        head, sep, tail = Packet.partition('app:')
        if len(tail) >= 0:
            Packet = tail
        
        else:
            Packet = head
        
        #trim string
        Packet = Packet.strip()
    
   # msg = "\x02Message\x03"
    #cnt = msg.find("\x03")
   # print(cnt)
    if ser != 'None':
        ser.flush()
    
    return bFound, Packet
    
def GetPacketParse(ser, kFilter, Cal, n=1.5, loop_count=10, mu=0., sig=2., accumulator= 0., count=0):
    
    Packet = 'None'
    count = 0
    bFound = False
    bStart = False
    strTmpPacket = ""
    start = 0
    rssidbm = 0.00
    #Kalman settings
    measurement_sig = 0.0001;
    motion_sig = 1.;
    ser.flushInput()
    sleep(.1)
    while (count < 5 and bFound == False):
        tmpPacket=ser.readline()
        strPacket = tmpPacket.decode('utf-8')
    
        if (bStart == False):
            start = strPacket.find("\x02")
          #  print('Start',strPacket, start)
            if start >= 0:
               end =   strPacket.find("\x03")
              # print('End',strPacket,end)
               if (end >= 0):
                   if end > start:
                       length = end-start
                     #  print(length)
                       strTmpPacket = strPacket
                       bFound = True
                       
                   else:
                       #Bad packet here need to reset it
                       head, sep, tail = strPacket.partition('\x03')
                       if len(tail) >= 0:
                           strTmpPacket = tail
                           start = 0
                       #    print('Reset Packet: ', strTmpPacket)
                           bStart = True
                       else:
                           strTmpPacket = ''
                     #      print('Bad Packet: ', strTmpPacket)
                           bStart = False
                       
                       #strTmpPacket = strTmpPacket + strPacket
                        
               else:
                   if bStart == False:
                       strTmpPacket = strPacket.rstrip()
                       start = 0
                       bStart = True
                   else:
                       strTmpPacket.join(strPacket)
                      
           # else:
               # print("No Start")
                  
        else:
             end = strPacket.find("\x03")
           #  print('End2',end,strPacket,start)
             if (end >= 0):
                 if end > start:
                     length = end-start
                  #   print("lenght",length)
                     head, sep, tail = strPacket.partition('\x03')
                     strTmpPacket = strTmpPacket + head
                   #  print ('Pack join : ',strTmpPacket)
                     bFound = True
                       
                 else:
                     strTmpPacket = strTmpPacket + strPacket
                        
             else:
                 strTmpPacket = strTmpPacket + strPacket
                  
             
             
        count = count + 1      
    
    if bFound == True:
        Packet = re.sub(r'[\x00-\x1f\x7f-\x9f]]','',strTmpPacket)
        #remove 0x02 if there
        head, sep, tail = Packet.partition('\x02')
        if len(tail) >= 0:
            Packet = tail
        
        else:
            Packet = head
        
        head, sep, tail = Packet.partition('app:')
        if len(tail) >= 0:
            Packet = tail
        
        else:
            Packet = head
        
        #trim string
        
        Packet = Packet.strip()
        #Filter out based on name
        indexname = Packet.find("name:")
        name = Packet[indexname+5: indexname+10]
        print ('Tagname: ', name)
        indextag = name.find("Ta")
        if (indextag < 0):
            print ('Tagindex: ', indextag)
            bFound = False
        
        irssi = Packet.find("RSSI:")
        rssidbm = Packet[irssi + 5:irssi + 8]
      #  print(rssidbm)                 
        kRssi = kFilter.filter(int(rssidbm))
      #  print("Kalman: %5.2f"%kRssi)
        distance = GetDistance(kRssi, n, Cal)
     #   print("Distance: %5.2f"% distance)   
    #    print ("Pwr:", calculate_accuracy(4,kRssi))
        Adstring = ",Distance:%5.2f,Cal:%i,rssikal:%5.2f,N:%4.2f" % (distance, Cal, kRssi, n)
        Packet= Packet + Adstring
                                                    
       # msg = "\x02Message\x03"
        #cnt = msg.find("\x03")
       # print(cnt)
    

    return bFound, Packet
    
#This is not correct
def calculate_accuracy(txpower, rssi):
    if rssi == 0:
        return -1
    else:
        ratio = rssi/txpower
       
    if ratio < 1:
        return ratio**10
    else:
        return (float)(0.89976 * ratio**7.7095 + 0.111)
    

def GetDistance(rssi, n, A0):
    # RSSI = -10 *n * log(d/d0) + A0
    # n = 2 (In Free Space)
    # d = 10 ^ ((A) - RSSI)/ (10 * n))
    
    return pow(10, (float)(A0-rssi) / (10 * n))

#defReadLoop(ser):

#ser = serial.Serial(
#        port='/dev/ttyUSB0',
#        baudrate = 115200,
#        parity=serial.PARITY_NONE,
#       stopbits=serial.STOPBITS_ONE,
#        bytesize = serial.EIGHTBITS,
#        timeout=1
#        )

#while 1:
 #       x=ser.readline()
 #       print(x)
    
    
    

