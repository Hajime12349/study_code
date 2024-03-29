import shutil
import glob
import re
import os

if __name__ == "__main__":

    #files = glob.glob("./test_200/images/IMG_?_fake_B*")
    files = glob.glob("./test_latest/images/IMG_*_fake_B*")
    print(files)
    print(len(files))
    if not os.path.exists('./datasets'):
        os.mkdir('./datasets')
    for f in files:
        m = re.search(r'IMG_\d+', f)
        f_str=m.group()
        shutil.copyfile(f, f"datasets/{f_str}.png")