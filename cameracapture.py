from picamera import PiCamera
from time import sleep
import os
import sys


def Capture(SaveFileLocation):
    
    
    try:
        camera = PiCamera()

        camera.start_preview()
        #sleep(5)

        camera.capture(SaveFileLocation)
           
    except:
        e = sys.exc_info() [0]
        
        print('Capture Exception Error:' %e);
        
    finally:
        camera.stop_preview()
        camera.close()
        
def View(TimeSecs):
    
    
    try:
        camera = PiCamera()

        camera.start_preview();
        sleep(TimeSecs)
       # sleep(10)
            
    except:
        e = sys.exc_info() [0]
        
       # print('Capture Exception Error:' %e);
        
    finally:
        camera.stop_preview()
        camera.close()
                