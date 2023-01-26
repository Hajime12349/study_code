#coding: utf-8

import numpy as np
from PIL import Image



i=1
data_list=[]
while i<=4940:
    name_TXT='IMG_'+str(i)+'.txt'
    print(name_TXT)
    with open(name_TXT, "r") as f:
        datalist = f.readlines()
        
    with open(name_TXT, "w") as f:
        for data in datalist:
            position=data.split()
            ns=f'{0} {position[1]} {position[2]} {position[3]} {position[4]}\n'
            f.write(ns)
    i+=1
