# BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# JCS 06/07/14
# Convert to python3 and fix all the bugs in this code
# Fix rssi and txpower is in twos complement




DEBUG = False
# BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py

# https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
# https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

# performs a simple device inquiry, and returns a list of ble advertizements 
# discovered device

# NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
# should be used for BLE. Always start a struct.pack() format string with "<"

import os
import sys
import struct
import bluetooth._bluetooth as bluez
import bluetooth
#import PositionKalman as PosKal
import kalman as Kal
import numpy as np
from time import sleep



LE_META_EVENT = 0x3e
LE_PUBLIC_ADDRESS=0x00
LE_RANDOM_ADDRESS=0x01
LE_SET_SCAN_PARAMETERS_CP_SIZE=7
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_PARAMETERS=0x000B
OCF_LE_SET_SCAN_ENABLE=0x000C
OCF_LE_CREATE_CONN=0x000D

LE_ROLE_MASTER = 0x00
LE_ROLE_SLAVE = 0x01

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02
EVT_LE_CONN_UPDATE_COMPLETE=0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE=0x04

# Advertisment event types
ADV_IND=0x00
ADV_DIRECT_IND=0x01
ADV_SCAN_IND=0x02
ADV_NONCONN_IND=0x03
ADV_SCAN_RSP=0x04




def twosComplement(value, bitWidth):
    if value >=2**bitWidth:
        raise ValueError("Value: {} out of range of {}-bit value.".format(value, bitWidth))
    else:
        return value - int((value << 1) & 2**bitWidth)

def GetDistance(rssi, n, A0):
    # RSSI = -10 *n * log(d/d0) + A0
    # n = 2 (In Free Space)
    # d = 10 ^ ((A) - RSSI)/ (10 * n))
    # A0 calibrated value at 1 meter
    
    return pow(10, (float)(A0-rssi) / (10 * 2))


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
    
def returnnumberpacket(pkt):
    myInteger = 0
    multiple = 256
    for c in pkt:
        myInteger +=  c * multiple
        multiple = 1
    return myInteger 

def returnstringpacket(pkt):
    myString = "";
    for c in pkt:
        myString +=  "%02x" % c
    return myString 

def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % c)

def get_packed_bdaddr(bdaddr_string):
    packable_addr = []
    addr = bdaddr_string.split(':')
    addr.reverse()
    for b in addr: 
        packable_addr.append(int(b, 16))
    return struct.pack("<BBBBBB", *packable_addr)

def packed_bdaddr_to_string(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
# hci_le_set_scan_enable(dd, 0x01, filter_dup, 1000);
# memset(&scan_cp, 0, sizeof(scan_cp));
 #uint8_t         enable;
 #       uint8_t         filter_dup;
#        scan_cp.enable = enable;
#        scan_cp.filter_dup = filter_dup;
#
#        memset(&rq, 0, sizeof(rq));
#        rq.ogf = OGF_LE_CTL;
#        rq.ocf = OCF_LE_SET_SCAN_ENABLE;
#        rq.cparam = &scan_cp;
#        rq.clen = LE_SET_SCAN_ENABLE_CP_SIZE;
#        rq.rparam = &status;
#        rq.rlen = 1;

#        if (hci_send_req(dd, &rq, to) < 0)
#                return -1;
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)


def hci_le_set_scan_parameters(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01


   
def parse_events(sock, kFilter, Cal, loop_count=10, mu=0., sig=2., accumulator= 0., count=0):

    try:
        old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

        #Kalman settings
        measurement_sig = 0.0001;
        motion_sig = 1.;
        
        # perform a device inquiry on bluetooth device #0
        # The inquiry should last 8 * 1.28 = 10.24 seconds
        # before the inquiry is performed, bluez should flush its cache of
        # previously discovered devices
        flt = bluez.hci_filter_new()
        bluez.hci_filter_all_events(flt)
        bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
        sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
        done = False
        results = []
        myFullList = []
        for i in range(0, loop_count):
            #sleep(1)
            pkt = sock.recv(255)
            ptype, event, plen = struct.unpack("BBB", pkt[:3])
            #print "--------------" 
            if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
                i =0
            elif event == bluez.EVT_NUM_COMP_PKTS:
                i =0 
            elif event == bluez.EVT_DISCONN_COMPLETE:
                i =0 
            elif event == LE_META_EVENT:
                #print ("\n LE_META_EVENT event: ", event);
               # print (pkt[3])            
                           
                
                #subevent, = struct.unpack("B", pkt[3])
                subevent = pkt[3]
                pkt = pkt[4:]
                if subevent == EVT_LE_CONN_COMPLETE:
                    le_handle_connection_complete(pkt)
                elif subevent == EVT_LE_ADVERTISING_REPORT:
                    #print "advertising report"
                    #num_reports = struct.unpack("B", pkt[0])[0]
                    num_reports = 1
                    report_pkt_offset = 0
                    #print(pkt)
                    #print ("\tUDID: ", printpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6]))
                    #print ("\tMAC address: ", packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9]))
                    nrsp = bluetooth.get_byte(pkt[0])
                    #print (len(pkt))
                    if len(pkt) > 16:
                        #for i in range(nrsp):
                            #addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                        addr = bluez.ba2str( pkt[3:9] )
                            #rssi = 0
                        
                       
                        
                        if 'FB:4D:0A:2F:A3:5A' in addr:
                            rssidbm = twosComplement(pkt[report_pkt_offset -1], 8)
                            txpowerdbm = twosComplement(pkt[report_pkt_offset -2], 8)    
                            #distance = GetDistance(rssidbm, 2, -64)
                            kRssi = kFilter.filter(int(rssidbm))
                            #print ("Filtered rssi:%3f" % kRssi)
                            
                            distance = GetDistance(kRssi, 2, Cal)
                            #Acc = calculate_accuracy(txpowerdbm, kRssi)
                            #Acc =  1.00
                            #print("[%s] RSSI: [%i]  TXPwr: [%i] dbm Dist : [%3f]" % (addr, rssidbm, txpowerdbm, distance))
                            Adstring = "%s, RSSI: %i,  TXPwr: %i, Dist : %5.2f, Cal: %i, RawRSSI: %5.2f" % (addr, kRssi, txpowerdbm, distance, Cal, rssidbm)
                            #Adstring += ","
                            g_accumulator = accumulator + kRssi
                            g_count = count + 1
                            avg = g_accumulator/g_count
                            print('avg rssi: {0:6.2f}'.format(avg))
                            
                            #print ("Filtered distance:" , kFilter.filter(float(distance)))
                            
                            #mu, sig = PosKal.update(mu, sig, rssidbm, measurement_sig)
                            #print('Update: [{}, {}]'.format(mu, sig))
                            #mu, sig = PosKal.predict(mu, sig, distance, motion_sig)
                            g_mu = mu
                            g_sig = sig
                            #print ('Predict: [{}, {}]'.format(mu, sig))
                            
                            myFullList.append(Adstring)
                            #print (Adstring)
                            #print(pkt)
                            #print (len(pkt))
                            #if len(pkt) > 34:
                            #    print (bluetooth.byte_to_signed_int(bluetooth.get_byte(pkt[16])))
                        
                    #data = bluez.ba2str( pkt[0:20] )
                    
                    #print ("Results: [%s]",pkt);
                    
                    for i in range(0, num_reports):
                        if (DEBUG == True and 'FB:4D:0A:2F:A3:5A' in addr):
                            print ("-------------")
                                #print "\tfullpacket: ", printpacket(pkt)
                            print ("\tUDID: ", printpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6]))
                            print ("\tMAJOR: ", printpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4]))
                            print ("\tMINOR: ", printpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2]))
                            print ("\tMAC address: ", packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9]))
                            # commented out - don't know what this byte is.  It's NOT TXPower
                            txpower = pkt[report_pkt_offset -2]
                            txpowerdbm = twosComplement(int(txpower), 8)
                            print ("\tTxPwr: ", txpowerdbm)
                            
                            rssi = pkt[report_pkt_offset -1]
                            rssidbm = twosComplement(int(rssi), 8)
                            print ("\tRSSI: %i" % rssidbm)
                            
                            # build the return string
                            Adstring = packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9])
                            Adstring += ","
                            Adstring += returnstringpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6]) 
                            Adstring += ","
                            Adstring += "%i" % returnnumberpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4]) 
                            Adstring += ","
                            Adstring += "%i" % returnnumberpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2]) 
                            Adstring += ","
                            Adstring += "%i" % pkt[report_pkt_offset -2]
                            Adstring += ","
                            Adstring += "%i" % pkt[report_pkt_offset -1]

                            #print "\tAdstring=", Adstring
                            myFullList.append(Adstring)
                            #ftxpower = float(txpower)
                            #print ("%i (%3X)" % (rssi, rssi))
                            #frssi = float(rssi)
                            #distance = calculate_accuracy(ftxpower, frssi)
                            #print ("\tdistance:", distance)
                            #Realrssi = twosComplement(int(rssi), 8)
                            #print (Realrssi)
                            done = True
                    
       
        sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
        
    except:
        print ("error parse_events()...")
        sleep(1)
       
    return myFullList


dev_id = 0
try:
    print ("accessing bluetooth device...")
    
    sock = bluez.hci_open_dev(dev_id)
except:
    print ("error accessing bluetooth device...")
    sys.exit(1)
    
