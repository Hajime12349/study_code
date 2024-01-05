import matplotlib.pyplot as plt
import csv
import re
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['xtick.direction'] = 'in' # x axis in
plt.rcParams['ytick.direction'] = 'in' # y axis in 
plt.rcParams['axes.linewidth'] = 1.0 # axis line width
plt.rcParams['axes.grid'] = True # make grid

interval=100
markers=["o","s", "v", "^", "2", "3"]

def plot_graqh(names,data,metric):


    # 折れ線グラフの描画
    plt.figure(figsize=(8, 6))  # グラフのサイズを設定
    
    index=0
    for name in names:    
        #print(F'x:{len(x)},y:{len(data[index])}')
        #print(name)
        print(index)
        x = list(range(25, len(data[index])*25+1, 25))
        #x = list(range(100, len(data[index])*100+1, 100))
        #x = list(range(25, 601, 25))
        #x = list(range(25, 501, 25))
        
        y=data[index]
        
        x=x[1::2]
        y=y[1::2]
        #data[index]=data[index][::interval]
        
        plt.plot(x,y,marker=markers[index], label=name,markersize=6)
        #plt.plot(x,data[index][:12],marker=markers[index], label=name,markersize=6)
        index+=1

    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))

    plt.xlabel('Epoch',fontsize=20)
    #plt.ylabel('Recall',fontsize=16)
    #plt.ylabel('Precision',fontsize=16)
    plt.ylabel('F2 - score',fontsize=20)
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.yticks(np.arange(0.5,0.951,0.1))
    #plt.yticks(np.arange(0.8,0.951,0.05))


    #Y軸範囲指定
    plt.ylim(0.45,0.95)
    #plt.ylim(0.8,0.95)
    

    # 凡例を表示
    plt.legend(fontsize=18).get_frame().set_alpha(0.6)

    
    plt.savefig(f'{metric}_f2.png', format="png", dpi=600)
    #plt.savefig(f'{metric}_f2_mix.png', format="png", dpi=600)
    
    # グラフを表示
    plt.show()

def load_metric(target_metric,target_models):
    result=[]
    before=''
    with open(f'analsys_result_{target_metric}.csv') as f:
        reader=csv.reader(f)
        tmp_result=[]
        count=0

        for row in reader:
            for target in target_models:
                count+=1
                if count == 1:
                    before=target
                pattern=f'{target}_\d*epoch'
                pt_obj=re.compile(pattern)
                match=pt_obj.fullmatch(row[0])    
                if match:
                    print(f'{before}:{target}')
                    if before != target:
                        #print('hi')
                        result.append(tmp_result)
                        tmp_result=[]
                        before=target
                    tmp_result.append(float(row[1]))

    result.append(tmp_result)
    return result
    
def calc_f2(list_recall,list_precision,targets):
    
    index=0
    f2=[]
    for target in targets:
        # print(index)
        # print(list_recall)
        recall_np=np.array(list_recall[index])
        precision_np=np.array(list_precision[index])
        A=5*(recall_np*precision_np)
        B=((4*precision_np)+recall_np)
        f2_np=np.divide(A, B, out=np.zeros_like(A), where=B!=0)
        f2.append(list(f2_np))


        max_f2=np.max(f2_np)
        max_index=np.argmax(f2_np)
        
        # max_f2=np.max(f2_np[:12])
        # max_index=np.argmax(f2_np[:12])
        target_f2=f2_np[11]
        
        print(f'Model:{target},f2:{max_f2},epoch:{max_index*25+25},recall:{recall_np[max_index],}precision:{precision_np[max_index]}')
        #print(f'Model:{target},f2:{target_f2},epoch:{11*25+25}')
        
        print()
        index+=1
    return f2

        



#target_metric='map'
#target_metric='recall_0.5'
#target_metric='recall_0.75'
#target_metric='precision_0.5'
#target_metric='precision_0.75'

#targets=['Real_1235','CG_1235','t2_cycle_200','t2_retina_200']
#targets=['Real_1235','t2_real_CG','t2_real_cycle','t2_real_retina']
targets=['t2_real_100_1000','t2_real_CG_100_1000','t2_real_cycle_100_1000','t2_real_retina_100_1000']

#def_names=['Real-Image','CGI','CycleGAN-Generated','RetinaGAN-Generated']
#def_names=['Real','CG','CycleGAN','RetinaGAN']
def_names=['Real','Real+CG','Real+CycleGAN','Real+RetinaGAN']




#targets=['Real_1235','t2_real_CG','t2_real_cycle','t2_real_retina']

recall=load_metric('recall_0.5',targets)
precision=load_metric('precision_0.5',targets)

f2=calc_f2(recall,precision,targets)
plot_graqh(def_names,f2,'F2')

# print(name)
# print(result)
