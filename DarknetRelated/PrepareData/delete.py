#coding: utf-8
import numpy as np
import cv2
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


def show(image, boxes, color, alpha):
    #print(str(width)+str(height))
    image = image.copy()
    for boxes_one in boxes:
        for b in boxes_one:
            overlay = image.copy()
            p1 = (int(b.x), int(b.y))
            p2 = (int(b.x + b.w), int(b.y + b.h))
            cv2.rectangle(overlay, p1, p2, color, -1)
            image = cv2.addWeighted(image, alpha, overlay, 1-alpha, 0)
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow('img', image)
    cv2.waitKey()
    #write_name='img'+str(i)+'.jpg'
    #cv2.imwrite(write_name,image)
f = open('myfile.txt', 'w')
i=1
while i<=100:
    miss=-1
    mod_str=''
    fm = open('myfile.txt', 'w')
    fm.write(str(i))
    fm.write('\n')
    fm.close()
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
    print(str(width)+' : '+str(height)+'\n')
    #cv2.imwrite("trim.png",image)
    boxes2=[Box(x_cut,y_cut,width-x_cut*2,height-y_cut*2)]
    #show(image, boxes2, (255, 0, 0), 0.5)

    with open(name_TXT, "r+") as f:

        datalist = f.readlines()
        count_row=0
        count_show=0
        boxes_list=[]
        #f.seek(0)
        for data in datalist:
            count_show+=1
            position=data.split()
            if ((float(position[1])+(float(position[3])/2))>width):
                print('miss_X_high')
                position[1]=str(float(position[1])-((float(position[1])+(float(position[3])/2))-width)-0.005)
                miss=count_row
            if((float(position[1])-(float(position[3])/2))<0 ):
                print('miss_X_low')
                position[1]=str(float(position[1])-(float(position[1])-(float(position[3])/2))+0.005)
                print(position[1])
                miss=count_row
            if(((float(position[2])+(float(position[4])/2))>height)):
                print('miss_Y_high')
                position[2]=str(float(position[2])-((float(position[2])+(float(position[4])/2))-height)-0.005)
                miss=count_row
            if(((float(position[2])-(float(position[4])/2))<0 )):
                print('miss_Y_low')
                position[2]=str(float(position[2])-(float(position[2])-(float(position[4])/2))+0.005)
                miss=count_row
            if(miss!=-1):
                mod_str='0 '+position[1]+' '+position[2]+' '+position[3]+' '+position[4]
                break
            #    # or ((float(position[1])-(float(position[3])/2))<0 )or ((float(position[2])+(float(position[4])/2))>height) or ((float(position[2])-(float(position[4])/2))<0)
            #    #print('missing_Annotation')
            boxes =[Box(float(position[1])*width-(float(position[3])*width/2),float(position[2])*height-(float(position[4])*height/2),float(position[3])*width,float(position[4])*height)]  
            for bo in boxes:
                print(str(int(bo.x))+'x:'+str(int(bo.y))+'y:'+str(int(bo.h))+'h:'+str(int(bo.w))+'w')
                top=(bo.x,bo.y)
                bottom=(bo.x+bo.w,bo.y+bo.h)
            #print(str(width-x_cut)+" "+str(top[0]))
            boxes_list.append(boxes)
            if(x_cut>top[0] or y_cut>top[1] or width-x_cut<bottom[0] or height-y_cut<bottom[1]):
                print('delete'+str(count_row))
            #    #miss=True
            #    #show(image, boxes, (255, 0, 0), 0.5)
            #else:
            #    new_posX=(float(position[1])*width-x_cut)/width2
            #    new_posY=(float(position[2])*height-y_cut)/height2
            #    new_width=(float(position[3])*width)/width2
            #    new_height=(float(position[4])*height)/height2
            #    data2="0 {0:.6f} {1:.6f} {2:.6f} {3:.6f}".format(new_posX,new_posY,new_width,new_height)
            #    #print(data2)
            #    #f.write(data2+'\n')
            count_row+=1
        if(count_show==0):
            cv2.namedWindow("img", cv2.WINDOW_NORMAL)
            cv2.imshow('img', image)
            cv2.waitKey()
        else:
            show(image, boxes_list, (255, 0, 0), 0.7)
        f.close()
    i+=1
    size = (608, 608)
    resized_image = cv2.resize(img_trim, size)
    #cv2.imwrite(name_IMG, resized_image)
    if(miss!=-1):
        with open(name_TXT, mode='w') as fr:
             c=0
             for data in datalist:
                 if(c==count_row):
                     fr.write(mod_str)
                 else:
                     fr.write(data)
                 c+=1
        i-=1
    elif ((input("delete?")=='d')):
        mod_TXT='mod_'+name_TXT
        mod_IMG='mod_'+name_IMG
        os.rename(name_TXT,mod_TXT)
        os.rename(name_IMG,mod_IMG)
        print('delete'+name_IMG)


#image, boxes=resize(image,boxes,384,384)

# height, width, channels = image.shape[:3]
# print(str(width)+str(height))
# show(image, boxes, (255, 0, 0), 0.5)

