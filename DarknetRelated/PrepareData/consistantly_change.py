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


mod_value=0.01
i=1
while i<=1234:
    print(str(i))
    name_IMG='IMG_'+str(i)+'.jpg'
    name_TXT='IMG_'+str(i)+'.txt'

    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width, channels = image.shape[:3]
    with open(name_TXT, "r") as f:
        datas=""
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
            if 0>top_left[0]:
                print(str(i))
                print("top_outx")
                position[1]=str(float(position[1])+mod_value)
            elif 0>top_left[1]:
                print(str(i))
                print("top_outy")
                position[2]=str(float(position[2])+mod_value)
            elif width<bottom_right[0]:
                print(str(i))
                print("bottom_outx")
                position[1]=str(float(position[1])-mod_value)
            elif height<bottom_right[1]:
                print(str(i))
                print("bottom_outy")
                position[2]=str(float(position[2])-mod_value)
            datas+="{0} {1:.6f} {2:.6f} {3:.6f} {4:.6f}\n".format(int(position[0]),float(position[1]),float(position[2]),float(position[3]),float(position[4]))
            count_row+=1
        f.close()
    with open(name_TXT, "w") as fw:
        fw.write(datas)
        fw.close()
    i+=1
    #size = (608, 608)
    #resized_image = cv2.resize(img_trim, size)
    #cv2.imwrite(name_IMG, resized_image)


#image, boxes=resize(image,boxes,384,384)

# height, width, channels = image.shape[:3]
# print(str(width)+str(height))
# show(image, boxes, (255, 0, 0), 0.5)

