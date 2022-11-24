#coding: utf-8

import cv2
import numpy as np
from PIL import Image
import os


class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

def resize(image, boxes, width, height):
    # 現在の高さと幅を取得しておく
    c_height, c_width = image.shape[:2]
    img = cv2.resize(image, (width, height))

    # 圧縮する比率(rate)を計算
    r_width = width / c_width
    r_height = width / c_height

    # 比率を使ってBoundingBoxの座標を修正
    new_boxes = []
    for box in boxes:
        x = int(box.x * r_width)
        y = int(box.y * r_height)
        w = int(box.w * r_width)
        h = int(box.h * r_height)
        new_box = Box(x, y, w, h)
        new_boxes.append(new_box)
    return img, new_boxes


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
    write_name='img'+str(i)+'.jpg'
    #cv2.imwrite(write_name,image)
i=1
while i<=500:
    print(str(i))
    name_IMG='IMG_'+str(i)+'.jpg'
    name_TXT='IMG_'+str(i)+'.txt'

    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width, channels = image.shape[:3]

    x_cut=0
    y_cut=0
    if height>width:
        y_cut=(height-width)//2
        x_cut=0
    elif width>height:
        y_cut=0
        x_cut=(width-height)//2
    print(str(width)+' : '+str(height)+'\n')
    print(str(x_cut)+' : '+str(y_cut)+'\n')
    img_trim = image[y_cut:height-y_cut, x_cut:width-x_cut]
    #cv2.imshow("trim", img_trim)
    height2, width2 = img_trim.shape[:2]
    print(str(width2)+' : '+str(height2)+'\n')
    #cv2.imwrite("trim.png",image)
    boxes2=[Box(x_cut,y_cut,width-x_cut*2,height-y_cut*2)]
    #show(image, boxes2, (255, 0, 0), 0.5)
    non_data=False
    if not os.path.exists(name_TXT):
        with open(name_TXT,"w") as f:
            f.close()
    with open(name_TXT, "r") as f:

        datalist = f.readlines()
        if len(datalist)==0:
            non_data=True
            cv2.namedWindow("img", cv2.WINDOW_NORMAL)
            cv2.imshow('img', image)
            cv2.waitKey()
        f.close()
    if(non_data):
        if ((input("delete?")=='d')):
            mod_TXT='mod_'+name_TXT
            mod_IMG='mod_'+name_IMG
            os.rename(name_TXT,mod_TXT)
            os.rename(name_IMG,mod_IMG)
            print('delete'+name_IMG)
    i+=1
    #size = (608, 608)
    #resized_image = cv2.resize(img_trim, size)
    #cv2.imwrite(name_IMG, resized_image)
#image, boxes=resize(image,boxes,384,384)

# height, width, channels = image.shape[:3]
# print(str(width)+str(height))
# show(image, boxes, (255, 0, 0), 0.5)

