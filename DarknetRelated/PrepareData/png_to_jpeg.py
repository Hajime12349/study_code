#coding: utf-8
#coding: utf-8

from os import name
from PIL import Image
start=4941
end=9880
i=start
while i<=end:
    name_IMG='IMG_'+str(i)+'.png'
    print(name_IMG)
    im = Image.open(name_IMG)
    im = im.convert("RGB")
    im.save('IMG_'+str(i)+'.jpg')
    i+=1