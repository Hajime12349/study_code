import matplotlib.pyplot as plt
import csv
import re

plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['xtick.direction'] = 'in' # x axis in
plt.rcParams['ytick.direction'] = 'in' # y axis in 
plt.rcParams['axes.linewidth'] = 1.0 # axis line width
plt.rcParams['axes.grid'] = True # make grid

markers=["o","s", "v", "^", "2", "3"]

def plot_graqh(names,data,metric):

    x = list(range(25, 301, 25))

    # 折れ線グラフの描画
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    
    index=0
    for name in names:    
        #print(F'x:{len(x)},y:{len(data[index])}')
        #print(name)
        plt.plot(x,data[index],marker=markers[index], label=name,markersize=6)
        index+=1

    plt.xlabel('Epoch',fontsize=16)
    #plt.ylabel('Recall',fontsize=16)
    #plt.ylabel('Precision',fontsize=16)
    plt.ylabel('mAP',fontsize=16)
    
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    
    #Y軸範囲指定
    #plt.ylim(0.55,0.75)
    #plt.ylim(0.75,0.95)
    #plt.ylim(0.5,0.95)


    # 凡例を表示
    plt.legend(fontsize=14).get_frame().set_alpha(0.6)

    
    plt.savefig(f'{metric}_mix.png', format="png", dpi=600)
    # グラフを表示
    plt.show()

    

#target_metric='map'
target_metric='recall_0.5'
#target_metric='recall_0.75'
#target_metric='precision_0.5'
#target_metric='precision_0.75'

#targets=['Real_1235','CG_1235','t2_cycle_200','t2_retina_200']
targets=['Real_1235','t2_real_CG','t2_real_cycle','t2_real_retina']
#def_names=['Real','CG','CycleGAN-Generated','RetinaGAN-Generated']
def_names=['Real','Real+CG','Real+CycleGAN','Real+RetinaGAN']
name=[]
result=[]
before=''

with open(f'analsys_result_{target_metric}.csv') as f:
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
                    print(def_names[targets.index(before)])
                    name.append(def_names[targets.index(before)])
                    result.append(tmp_result)
                    tmp_result=[]
                    before=target
                tmp_result.append(float(row[1]))

name.append(def_names[targets.index(before)])
result.append(tmp_result)
plot_graqh(name,result,target_metric)

# print(name)
# print(result)
