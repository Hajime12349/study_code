#coding: utf-8

import cv2
import numpy as np
import glob
import re
from PIL import Image,ImageDraw
import random

def bbox2points(bbox):
    """
    From bounding box yolo format
    to corner points cv2 rectangle
    """
    x, y, w, h = bbox
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

def image_detection(detections,image,height, width):
    # width = darknet.network_width(network)
    # height = darknet.network_height(network)
    # darknet_image = darknet.make_image(width, height, 3)

    for detect_str in detections:
        tmp_sp=detect_str.split()
        detect=[float(i)*height for i in tmp_sp]
        detect=detect[1:]
        #print(detect)
        boxes=[detect[0]-detect[2]/2,
                detect[1]-detect[3]/2,
                detect[0]+detect[2]/2,
                detect[1]+detect[3]/2]
    
        pil_image = Image.fromarray(image)
        draw=ImageDraw.Draw(pil_image)
        draw.rectangle((boxes[0],boxes[1],boxes[2],boxes[3]),None,(0, 255,0),width=3)
        #pil_image.show()
        image = np.array(pil_image)
        #image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections


    return image

class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h




def show(image):
    #print(str(width)+str(height))
    
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow('img', image)
    cv2.waitKey()

i=0

names_IMG=glob.glob('./*.jpg')
names_TXT=glob.glob('./*.txt')


for name_IMG,name_TXT in zip(names_IMG,names_TXT):
    i+=1
    print(str(name_IMG))
    # name_IMG='IMG_'+str(i)+'.jpg'
    # name_TXT='IMG_'+str(i)+'.txt'
    num_IMG=re.sub(r"\D", "", name_IMG)

    if(num_IMG!=re.sub(r"\D", "", name_TXT)):
        raise ValueError("error!")
    
    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width, channels = image.shape[:3]

    with open(name_TXT, "r") as f:
        datalist = f.readlines()
        if(len(datalist)!=0):
            out_image=image_detection(datalist,image,height, width)
            #show(image)
            cv2.imwrite(fr'./output/out_{num_IMG}.jpg', out_image)
            print(num_IMG)
        else:
            cv2.imwrite(fr'./output/out_{num_IMG}.jpg', image)
    f.close()

