import darknet_module
a=[0,0.270433,0.401442,0.242788,0.250000]
#b=[0,0.344156,0.101732,0.096320,0.077922]
b=[0,0.215368,0.404221,0.230519,0.245671]

boxA = [float(a[1])-float(a[3])/2,
    float(a[2])-float(a[4])/2,
    float(a[1])+float(a[3])/2,
    float(a[2])+float(a[4])/2]

boxB = [float(b[1])-float(b[3])/2,
    float(b[2])-float(b[4])/2,
    float(b[1])+float(b[3])/2,
    float(b[2])+float(b[4])/2]


print (str(boxA)+':'+str(boxB))
print(round(darknet_module.iou(boxA,boxB),4))