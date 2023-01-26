from PIL import Image
import glob
import os

files=glob.glob("IMG_*.png")

for f in files:
    print(f)
    im = Image.open(f)
    im = im.convert("RGB")
    new_f=os.path.splitext(f)[0]
    im.save(f"{new_f}.jpg")
    os.remove(f)
print(len(files))