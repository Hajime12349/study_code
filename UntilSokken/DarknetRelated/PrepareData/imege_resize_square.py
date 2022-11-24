#coding: utf-8
#coding: utf-8

from os import name
import cv2
import numpy as np
from PIL import Image
size=(416,416)
start=1
end=1
i=start
while i<=end:
    name_IMG='IMG_'+str(i)+'.jpg'
    print(name_IMG)
    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width = image.shape[:2]
    print("Before="+str(height)+":"+str(width))
    resized_image=cv2.resize(image, size)
    height2, width2 = resized_image.shape[:2]
    print("After="+str(height2)+":"+str(width2))
    cv2.imwrite(name_IMG, resized_image)
    i+=1