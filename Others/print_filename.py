import glob
files=glob.glob("*")
s=""
for f in files:
    s+=f"{f} "
print(s)