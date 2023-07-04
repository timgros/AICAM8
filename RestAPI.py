
import requests
from PIL import Image, ImageOps  # Install pillow instead of PIL
import io
import os


def ClassifyImage(url, imagepath):
    
    url = os.path.join('http://',url)
 
   
    with open(imagepath, 'rb') as fh:
              #img_binary = _read_data_to_bytes(fh.read())
              img_binary = io.BytesIO(fh.read())


    payload=img_binary
    headers = {
      'Content-Type': 'application/octet-stream'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

  #  print(response.text,type(response))
    jsonresp = response.json()
   # print(jsonresp)

   # print(jsonresp['label'], jsonresp['predictions'])

    return jsonresp


if __name__ == '__main__':
    
    jsonresp = ClassifyImage('10.83.106.64:5000/classifyYOLOv7', "/home/pi/images/image.jpg")
    print(jsonresp)
