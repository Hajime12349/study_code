#coding: utf-8

import os
import random

i=1
select_num=100
name_list=[]
while i<=1334:
    name_list+=[i]
    i+=1
    #size = (608, 608)
    #resized_image = cv2.resize(img_trim, size)
    #cv2.imwrite(name_IMG, resized_image)
random_select=random.sample(name_list, select_num)
for t in random_select:
    name_IMG='IMG_'+str(t)+'.jpg'
    name_TXT='IMG_'+str(t)+'.txt'
    mod_TXT='test_'+name_TXT
    mod_IMG='test_'+name_IMG
    print(name_IMG)
    os.rename(name_TXT,mod_TXT)
    os.rename(name_IMG,mod_IMG)

#image, boxes=resize(image,boxes,384,384)

# height, width, channels = image.shape[:3]
# print(str(width)+str(height))
# show(image, boxes, (255, 0, 0), 0.5)

