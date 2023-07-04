
import io
#import StringIO
import subprocess
import os
import time
from datetime import datetime
from PIL import Image



command = "raspistill %s -w %s -h %s -t 200 -e bmp -n -o -" % ('-hf', 640, 640)

imageData = io.BytesIO()
imageData.write(subprocess.check_output(command, shell=True))
imageData.seek(0)
print(type(imageData))
im = Image.open(imageData)
print(type(im))
buffer = im.load()
imageData.close()