import matplotlib.pyplot as plt
import csv
import re

plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['xtick.direction'] = 'in' # x axis in
plt.rcParams['ytick.direction'] = 'in' # y axis in 
plt.rcParams['axes.linewidth'] = 1.0 # axis line width
plt.rcParams['axes.grid'] = True # make grid

def plot_graqh(names,data):

    x = list(range(25, 301, 25))

    # 折れ線グラフの描画
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    
    index=0
    for name in names:    
        print(F'x:{len(x)},y:{len(data[index])}')
        plt.plot(x,data[index], "-", label=name)
        index+=1

    plt.xlabel('epoch')
    plt.ylabel('recall')
    #plt.ylim(0,1)

    # 凡例を表示
    plt.legend()

    # グラフを表示
    plt.show()


targets=['Real_1235','CG_1235','t2_cycle_200','t2_retina_200']
def_names=['Real','CG','CycleGAN-Generated','RetinaGAN-Generated']
name=[]
result=[]
before=''

with open('analsys_result_recall_0.5.csv') as f:
    reader=csv.reader(f)
    tmp_result=[]
    count=0

    for row in reader:
        for target in targets:
            count+=1
            if count == 1:
                before=target
            pattern=f'{target}_\d*epoch'
            pt_obj=re.compile(pattern)
            match=pt_obj.fullmatch(row[0])    
            if match:
                #print(f'{before}:{target}')
                if before != target:
                    name.append(def_names[targets.index(before)])
                    result.append(tmp_result)
                    tmp_result=[]
                    before=target
                tmp_result.append(float(row[1]))

name.append(def_names[targets.index(before)])
result.append(tmp_result)
plot_graqh(name,result)

# print(name)
# print(result)
