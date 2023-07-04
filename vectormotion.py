import os
import numpy as np
import picamera
from picamera.array import PiMotionAnalysis
#from picamera import PiCamera
import glob
import shutil

from time import sleep
import ftp
from datetime import datetime

#print("picamera version : ",picamera.__version__)


class GestureDetector(PiMotionAnalysis):
    QUEUE_SIZE = 10 # the number of consecutive frames to analyze
    THRESHOLD = 4.0 # the minimum average motion required in either axis

    def __init__(self, camera):
        super(GestureDetector, self).__init__(camera)
        self.x_queue = np.zeros(self.QUEUE_SIZE, dtype=np.float64)
        self.y_queue = np.zeros(self.QUEUE_SIZE, dtype=np.float64)
        self.last_move = ''
        #print('init')

    def analyze(self, a):
        # Roll the queues and overwrite the first element with a new
        # mean (equivalent to pop and append, but faster)
        self.x_queue[1:] = self.x_queue[:-1]
        self.y_queue[1:] = self.y_queue[:-1]
        self.x_queue[0] = a['x'].mean()
        self.y_queue[0] = a['y'].mean()
        # Calculate the mean of both queues
        x_mean = self.x_queue.mean()
        y_mean = self.y_queue.mean()
        # Convert left/up to -1, right/down to 1, and movement below
        # the threshold to 0
        x_move = (
            '' if abs(x_mean) < self.THRESHOLD else
            'left' if x_mean < 0.0 else
            'right')
        y_move = (
            '' if abs(y_mean) < self.THRESHOLD else
            'down' if y_mean < 0.0 else
            'up')
        # Update the display
        movement = ('%s %s' % (x_move, y_move)).strip()
        if movement != self.last_move:
            #print('Last : ',self.last_move)
            #if (len(movement) > 0):
            #    self.last_move = movement
            if movement:
                print('Last : ',self.last_move)
            
                self.last_move = movement
                print('Move : ', movement,' Last : ',self.last_move )
                if (y_move == 'down'):
                    print('PIC')
                 #   camera.stop_recording()
                   # camera = PiCamera()
                  #  camera.rotation = 180
                   # camera.resolution = (1280, 1024)
                   # camera.start_preview();
                    sleep(1)
                    #sleep(1)
                   # now = datetime.now()
                   # date_time = now.strftime("%m%d%Y%H%M%S")
                    #print(date_time)
                    SerialNumber = '12345'
                    print('Capture')
                    #use_video_port= True
                    iErr = camera.capture('/home/pi/images/image.jpg',use_video_port=False)
                    print('FTP',iErr)
                    shutil.copy('/home/pi/images/image.jpg', '/home/pi/images/image2.jpg')
                    #camera.release()
                    newfile = ftp.FTPUpload('10.83.52.29','picam','picam', SerialNumber, '/home/pi/images/image2.jpg')
                    print('rFTP',newfile)
                    camera.start_preview();
                    
                   # camera.start_recording(os.devnull, format='h264', motion_output=detector)
                    sleep(2)
                    #  camera.resolution = ('VGA')
                    camera.stop_preview()
                    #2592×1944 for still photos, and 1920×1080 for video recording.
                    #raspistill -f
                    #resolution=(1280, 1024), (1280, 720) camera.MAX_RESOLUTION fr = 15
            else:
                if movement:
                    print('Move : ', movement,' Last : ',self.last_move )
                    self.last_move = ''
   
                    
with picamera.PiCamera(framerate=24) as camera:
    camera.resolution=(1280, 720)
    camera.rotation = 180
    with GestureDetector(camera) as detector:
        camera.start_recording(os.devnull, format='h264', motion_output=detector)
        try:
            while True:
                record_results = camera.wait_recording(1)
                if record_results is not None:
                    print(type(record_results))
        finally:
            camera.stop_recording()
            
            