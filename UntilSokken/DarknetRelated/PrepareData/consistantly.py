#coding: utf-8

import cv2
import numpy as np
from PIL import Image


class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h



i=1
while i<=849:
    #print(str(i))
    name_IMG='IMG_'+str(i)+'.jpg'
    name_TXT='IMG_'+str(i)+'.txt'

    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width, channels = image.shape[:3]

    with open(name_TXT, "r+") as f:

        datalist = f.readlines()
        count_row=0
        #f.seek(0)
        for data in datalist:
            position=data.split()

            boxes =[Box(float(position[1])*width-(float(position[3])*width/2),float(position[2])*height-(float(position[4])*height/2),float(position[3])*width,float(position[4])*height)]  
            #横、縦
            top_left=(float(position[1])*width-(float(position[3])*width/2),float(position[2])*height-(float(position[4])*height/2))
            bottom_right=(float(position[1])*width+(float(position[3])*width/2),float(position[2])*height+(float(position[4])*height/2))
            #print(str(width-x_cut)+" "+str(top[0]))
            ##show(image, boxes, (255, 0, 0), 0.5,count_row)
            #print(str(top[1])+":"+str(top[0])+":"+str(bottom[1])+":"+str(bottom[0]))
            if 0>=top_left[0]:
                print(str(i))
                print("top_outx")
            elif 0>=top_left[1]:
                print(str(i))
                print("top_outy")
            elif width<=bottom_right[0]:
                print(str(i))
                print("bottom_outx")
            elif height<=bottom_right[1]:
                print(str(i))
                print("bottom_outy")
            count_row+=1
        f.close()
    i+=1
    #size = (608, 608)
    #resized_image = cv2.resize(img_trim, size)
    #cv2.imwrite(name_IMG, resized_image)


#image, boxes=resize(image,boxes,384,384)

# height, width, channels = image.shape[:3]
# print(str(width)+str(height))
# show(image, boxes, (255, 0, 0), 0.5)

