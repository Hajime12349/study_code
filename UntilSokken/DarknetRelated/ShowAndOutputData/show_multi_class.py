#coding: utf-8

'''
成長度３クラスのYOLO形式テキストと画像からPIL形式の確認画像を生成して表示するプログラム
'''

import cv2
import numpy as np
import random
from PIL import Image, ImageDraw,ImageFont
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
total_image_number=4

class Box:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


def show(image, boxes,i,id):
    label=['car']
    colors =[
        (0, 255,0),
        (0,150,255),
        (0, 0,255),
    ]
    text_width =[
        90,38,60
    ]
    #print(str(width)+str(height))
    #image = image.copy()
    for b in boxes:
        left=int(b.x)
        top=int(b.y)
        right=int(b.x + b.w)
        bottom = int(b.y + b.h)
        #cv2.rectangle(image, (left, top), (right, bottom), colors[label], 1)
        pil_image = Image.fromarray(image)
        draw=ImageDraw.Draw(pil_image)
        font_selected = ImageFont.truetype("meiryo.ttc", 16)
        draw.rectangle((left,top,right,bottom),None,colors[id],width=3)
        draw.rectangle((left,top-18,left+text_width[id],top), fill=colors[id])
        draw.text( (left, top - 20), label[id], fill='black',font=font_selected)
        image = np.array(pil_image)
    write_name='img'+str(i)+'.jpg'
    #cv2.imwrite(write_name,image)
    return image
i=0
while i<=total_image_number:
    i+=1
    print(str(i))
    name_IMG='test'+str(i)+'.jpg'
    name_TXT='test'+str(i)+'.txt'
    write_name='test_result'+str(i)+'.jpg'
    image = cv2.imread(name_IMG, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    height, width, channels = image.shape[:3]

    with open(name_TXT, "r") as f:
        datalist = f.readlines()
        count_row=0
        label=['harvestable','soon','not_yet']
        for data in datalist:
            position=data.split()
            boxes =[Box(float(position[1])*width-(float(position[3])*width/2),float(position[2])*height-(float(position[4])*height/2),float(position[3])*width,float(position[4])*height)]
            top=(float(position[1])*width-(float(position[3])*width/2),float(position[2])*height-(float(position[4])*height/2))
            bottom=(top[0]+(float(position[3])*width),top[1]+(float(position[4])*height))
            #print(int(position[0]))
            image=show(image, boxes,count_row,int(position[0]))
            count_row+=1
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.imshow('img', image)
        cv2.waitKey()
        cv2.imwrite(write_name,image)
        f.close()

