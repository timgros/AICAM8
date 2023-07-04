

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


print("cv2 version",cv2.__version__)

camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

#camera.capture_continuous(
    
    
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

cv2.imshow("Image", image)
#

cv2.waitKey(0)

#key = cv2.waitKey(1) & 0xFF

#if key == ord("q"):
#    break
    



