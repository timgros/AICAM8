import cv2

import numpy as np
import matplotlib.pyplot as plt
import glob
import random
import time


class Objectdetector:

  
   
    def __init__(self):

        self.classes = ['GoodScrew','BadScrew','NoScrew']
        self.class_ids = []
        self.confidences = []
        self.boxes = []

        print('init', np.__version__)
        print(cv2.__version__)


    def Loadmodel(self):
        
        print('Model Loading')
        self.net = cv2.dnn.readNet(r"/home/pi/MagPi/model/yolov3_custom.cfg",r"/home/pi/MagPi/model/alamohscrew-10-12-2022.weights")

        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        print('Model Loaded')
        

    def Classify_image(self, imagefile, verbose = False):
        img = cv2.imread(r"/home/pi/images/image.jpg")
        height, width, channels = img.shape

        #Detecting Object
        blob = cv2.dnn.blobFromImage(img,0.00392,(416, 416), (0,0,0), True, crop=False)

        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
              #  print(scores,class_id, confidence )
                if confidence > 0.4:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)
                    if verbose:
                        print(x, y, w, h,confidence,class_id )
                    
                    self.boxes.append([x, y, w, h])
                    self.confidences.append(float(confidence))
                    self.class_ids.append(class_id)

        print(len(self.boxes))  
        number_objects_detected = len(self.boxes)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(self.boxes)):
            x, y, w, h = self.boxes[i]
            label = str(self.classes[self.class_ids[i]])
    
       # indices = cv2.dnn.NMSBoxes(boxes[i], )
        if verbose:
            
           # print (label)
            if (self.class_ids[i] == 0):
                cv2.rectangle(img, (x,y),(x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (x,y),(x + w, y + h), (0, 0, 255), 2)
                
            cv2.putText(img, label,(x, y + 30), font, 1, (0,0,0), 2)
     
            cv2.imshow("Image", img)

            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    
    Obj = Objectdetector()
    
    Obj.Loadmodel()

    start = time.time()
    Obj.Classify_image(r"/home/pi/images/image.jpg")
    end = time.time()
    #if verbose:
    print(" Time: {:.2f} ".format((end - start)), " seconds")




