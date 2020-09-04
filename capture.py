import numpy as np
import cv2
from mss import mss
from PIL import Image
import io
import base64

sct = mss()

def resize(image,window_height = 500):
    aspect_ratio = float(image.shape[1])/float(image.shape[0])
    window_width = window_height/aspect_ratio
    image = cv2.resize(image, (int(window_height),int(window_width)))
    return image
n=1

def capture_image():

    w, h = 1920, 1080
    monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}
    img = Image.frombytes('RGB', (w,h), sct.grab(monitor).rgb)
    
    im = np.array(img) 
    im = im[:, :, ::-1].copy()
    # im_grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY
    
    im = resize(image = im, window_height = 370) #370
    # im = cv2.resize(im, (300, 250))
    ima = Image.fromarray(im.astype("uint8"))
    
    # encoded, buffer = cv2.imencode('.jpg', im)
  
    rawBytes = io.BytesIO()
    ima.save(rawBytes, "JPEG")
    rawBytes.seek(0)  # return to the start of the file
    
    s = base64.b64encode(rawBytes.read())
    
    # f = io.BytesIO(base64.b64decode(s))
    
    # pilimage = Image.open(f)
    # pilimage.save("save.jpg")
    
    return s
        # cv2.imwrite('test.jpg', im)
        
        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break