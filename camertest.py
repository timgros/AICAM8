#from picamera import PiCamera
from time import sleep
import picamera

with picamera.PiCamera(framerate=24) as camera:
    
    #camera = PiCamera()
    camera.rotation = 90
    #print(camera.resolution)
    #camera.resolution = (1280, 1024)
    camera.resolution = (1024, 1024)
    
    camera.start_preview();
    sleep(10)
    camera.capture('/home/pi/Desktop/image7.jpg')

    camera.stop_preview()

#raspistill -f
