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



def flip(f,position):
    new_posX=1-float(position[1])
    new_posY=float(position[2])
    new_width=float(position[3])
    new_height=float(position[4])
    data2="{0} {1:.6f} {2:.6f} {3:.6f} {4:.6f}".format(position[0],new_posX,new_posY,new_width,new_height)
    f.write(data2+'\n')
    return image


def g_noise(img,row,col):
    #row,col,ch = img.shape
    # 白
    rand_noise=random.randrange(3000,10000,1)
    pts_x = np.random.randint(0, col-1 , rand_noise) #0から(col-1)までの乱数を千個作る
    pts_y = np.random.randint(0, row-1 , rand_noise)
    img[(pts_y,pts_x)] = (255,255,255) #y,xの順番になることに注意

    # 黒
    pts_x = np.random.randint(0, col-1 , rand_noise)
    pts_y = np.random.randint(0, row-1 , rand_noise)
    img[(pts_y,pts_x)] = (0,0,0)
    return img

start=1
end=1235
i=start
while i<=end:
#   print(str(i))
    name_IMG='IMG_'+str(i)+'.png'
    name_IMG_mod='IMG_'+str(i+end)+'.png'
    name_TXT='IMG_'+str(i)+'.txt'
    name_TXT_mod='IMG_'+str(i+end)+'.txt'
    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width,ch = image.shape[:3]
    noise_image=g_noise(image,height,width)
    cv2.imwrite(name_IMG_mod, noise_image)
    with open(name_TXT, mode='r') as fi, open(name_TXT_mod, mode='w') as fw:
        for line in fi:
            fw.write(line )
    print(name_IMG_mod)
    i+=1
i=1
while i<=end*2:
#    print(str(i))
    name_IMG='IMG_'+str(i)+'.png'
    name_IMG_mod='IMG_'+str(i+(end*2))+'.png'
    name_TXT='IMG_'+str(i)+'.txt'
    name_TXT_mod='IMG_'+str(i+(end*2))+'.txt'
    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    with open(name_TXT, mode='r') as f, open(name_TXT_mod, mode='w') as fw:
        datalist = f.readlines()
        count_row=0
        for data in datalist:
            position=data.split()
            flip(fw,position)
            count_row+=1
    image = image[:, ::-1, :]
    cv2.imwrite(name_IMG_mod, image)
    print(name_IMG_mod)
    i+=1

