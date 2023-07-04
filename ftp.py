
import ftplib
import time
import os
import sys
import re
import subprocess
import datetime


def FTPUpload(IPAddress, user, password, serialnumber, imagefile):
    
    try:
        session = ftplib.FTP(IPAddress,user,password)
        now = datetime.datetime.now()

        date_time = now.strftime("%m%d%Y_%H%M%S")
          
        file = open(imagefile,'rb')
        #print (file.size)
        session.storbinary('STOR image.jpg', file)
        
       
        newfile = date_time+'_'+serialnumber+'_image.jpg'

        session.rename('image.jpg',newfile)
    except:
        e = sys.exc_info() [0]
        
        print('Exception Error:' %e);
        
    finally:    
        print (newfile)
        file.close()

        session.quit()
        
    return newfile
    
    


session = ftplib.FTP('10.83.52.29','picam','picam')

file = open('/home/pi/Desktop/imageOK7.jpg','rb')
session.storbinary('STOR imageOK7.jpg', file)

file.close()

session.quit()


