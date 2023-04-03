#coding: utf-8

import cv2
import numpy as np
from PIL import Image
import os


i=1
while i<=2000:
    print(str(i))
    name_IMG='IMG_'+str(i)+'.jpg'
    name_TXT='IMG_'+str(i)+'.txt'
    if(os.path.exists(name_IMG)):
        non_data=False
        if not os.path.exists(name_TXT):
            non_data=True
        if(non_data):
            mod_IMG='mod_'+name_IMG
            os.rename(name_IMG,mod_IMG)
            print('change:'+mod_IMG)
    i+=1

