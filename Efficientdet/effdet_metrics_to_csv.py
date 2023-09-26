import csv
import pprint
import matplotlib.pyplot as plt
import numpy as np

def is_numeric(string):
    try:
        float(string)  # ここで float() を使用して数値に変換を試みます
        return True   # 変換成功
    except ValueError:
        return False  # 変換失敗



with open('./metrics.csv') as f:
    reader=csv.reader(f)
    raw_data=[row for row in reader]
    datas=[]
    names=[]
    for column in reversed(range(0,4)):
        value=0
        datas. append([])
        for row in raw_data:
            tmp_value=row[column]
            if tmp_value :
                if is_numeric(tmp_value):
                    if value!=tmp_value and column==3:
                        value=tmp_value
                        datas[3-column].append(int(value))
                    elif column!=3:
                        value=tmp_value
                        datas[3-column].append(float(value))
                else:
                    names.append(tmp_value)
        #names.append(datas[3-column].pop(0))
    print(names)
    print(datas)
    print([len(v) for v in datas])
    #plt.plot(datas[0],datas[1],datas[0],datas[2],datas[0],datas[3])
    #print(max(datas[0]))
    #plt.axis((0, max(datas[0]), 0, max(datas[1])))
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax1.plot(datas[0], datas[1], color = "red")
    ax1.set_xlabel(names[0])
    ax1.set_ylabel(names[1])

    ax2 = fig.add_subplot(312)
    ax2.plot(datas[0], datas[2], color = "blue")
    ax2.set_xlabel(names[0])
    ax2.set_ylabel(names[2])

    ax3 = fig.add_subplot(313)
    ax3.plot(datas[0], datas[3], color = "green")
    ax3.set_xlabel(names[0])
    ax3.set_ylabel(names[3])
    
    #ax.set_xticks(np.arange(0,max(datas[0]),25))
    #ax.set_yticks(np.arange(0,max(datas[1]),max(datas[1])/10))
    plt.show()
