from picamera import PiCamera
from time import sleep
import ftplib
import time
import os
import sys
import re
import subprocess
import datetime
import ftp
import cameracapture


cameracapture.View(10)
#cameracapture.Capture('/home/pi/images/image.jpg')
#ftp.FTPUpload('172.20.15.100','picam','picam', 'c1234589', '/home/pi/images/image.jpg')

'''
camera = PiCamera()

camera.start_preview();
sleep(1)


filename = 'image.jpg'
camera.capture('/home/pi/images/image.jpg')

camera.stop_preview()
'''

#ftp.FTPUpload('172.20.15.100','picam','picam', 'c1234589', '/home/pi/images/image.jpg')

'''

session = ftplib.FTP('172.20.15.100','picam','picam')
now = datetime.datetime.now()

date_time = now.strftime("%m%d%Y_%H%M%S")
  
file = open('/home/pi/images/image.jpg','rb')
#print (file.size)
session.storbinary('STOR image.jpg', file)
newfile = ''+date_time +'image.jpg'
serialNumber = 'c1234567'
newfile = date_time+'_'+serialNumber+'_image.jpg'


session.rename('image.jpg',newfile)
print (newfile)
file.close()

session.quit()
'''

