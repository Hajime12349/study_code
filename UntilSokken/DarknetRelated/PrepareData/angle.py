import os
import glob
import shutil
from PIL import Image
start=125
end=132
i=start
while i<=end:
	f_name='IMG_'+str(i)+'.jpg'
	im = Image.open(f_name)
	im_rotate = im.rotate(-90)
	im_rotate.save(f_name, quality=95)
	i+=1



