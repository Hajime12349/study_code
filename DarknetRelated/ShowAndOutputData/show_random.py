#coding: utf-8

import cv2
import numpy as np
from PIL import Image
import random
import os
import sys
from pathlib import Path

#arg1:number of image
#arg2:random coefication


class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h




def show(image, boxes, color, alpha,i):
    #print(str(width)+str(height))
    image = image.copy()
    for b in boxes:
        overlay = image.copy()
        p1 = (int(b.x), int(b.y))
        p2 = (int(b.x + b.w), int(b.y + b.h))
        cv2.rectangle(overlay, p1, p2, color, -1)
        image = cv2.addWeighted(image, alpha, overlay, 1-alpha, 0)
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow('img', image)
    cv2.waitKey()

i=0
#diff=10000
diff=0
# sys.argv[1]=32
# sys.argv[2]=3
while i<=int(sys.argv[1])-int(sys.argv[2]):
    i+=random.randint(1, int(sys.argv[2]))
    name_IMG=f'IMG_{diff+i}.png'
    #name_IMG=f'IMG_{diff+i}.jpg'
    name_TXT=f'IMG_{diff+i}.txt'
    
    IMG_path=fr'./datasets/{name_IMG}'
    TXT_path=fr'./datasets/{name_TXT}'
    print(IMG_path)
    if(os.path.exists(IMG_path)):
        image = cv2.imread(IMG_path, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
        height, width, channels = image.shape[:3]

        with open(TXT_path, "r") as f:
            datalist = f.readlines()
            count_row=0
            if(len(datalist)==0):
                cv2.namedWindow("img", cv2.WINDOW_NORMAL)
                cv2.imshow('img', image)
                cv2.waitKey()
            for data in datalist:
                position=data.split()
                boxes =[Box(float(position[1])*width-(float(position[3])*width/2),float(position[2])*height-(float(position[4])*height/2),float(position[3])*width,float(position[4])*height)] 
                top=(float(position[1])*width-(float(position[3])*width/2),float(position[2])*height-(float(position[4])*height/2))
                bottom=(top[0]+(float(position[3])*width),top[1]+(float(position[4])*height))
                show(image, boxes, (255, 0, 0), 0.5,count_row)
                count_row+=1


