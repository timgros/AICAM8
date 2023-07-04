
import serialreader
import kalman as kal

count = 0




try:
    ser = serialreader.Open()
    print (ser)
except:
   print (ser)
   print ("error opening serial...")
 
    
#serialreader.Read(ser)

#Kalman settings
global g_mu;
global g_sig;


g_mu = 0.
g_sig = 1000.
global g_accumulator
global g_count

g_accumulator = 0.
g_count = 0

CalIn = -69
CalTemp = -69
kFilter = kal.KalmanFilter(0.008, 4.0)


while count < 10:
   # bFound, Packet = serialreader.GetPacketParse(ser, kFilter, CalIn, 2, g_mu, g_sig, g_accumulator, g_count)
    bFound, Packet = serialreader.GetPacket(ser)
    print('Packet:', Packet, bFound)
    count = count + 1
if (ser != None):
    ser.flush()
    serialreader.Close(ser)



