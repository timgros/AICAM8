
from picamera import PiCamera
from time import sleep
import ftplib
import time
import os
import sys
import re
import subprocess
import datetime


session = ftplib.FTP('172.20.15.100','picam','picam')
now = datetime.datetime.now()

date_time = now.strftime("%m/%d/%Y::%H:%M:%S")
  
newfile = ''+date_time +':image.jpg'
session.retrlines('LIST') 
session.rename('image.jpg','name2.jpg')
#print (newfile)
#file.close()

session.quit()