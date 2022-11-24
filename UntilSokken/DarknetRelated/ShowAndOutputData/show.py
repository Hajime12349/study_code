#coding: utf-8

import cv2
import numpy as np
from PIL import Image
import random


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
while i<=3:
    i+=1
    print(str(i))
    name_IMG='test'+str(i)+'.jpg'
    name_TXT='test'+str(i)+'.txt'

    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width, channels = image.shape[:3]

    with open(name_TXT, "r") as f:
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
    f.close()

