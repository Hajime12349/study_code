import matplotlib.pyplot as plt
import csv
import re
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman' #全体のフォントを設定
plt.rcParams['xtick.direction'] = 'in' # x axis in
plt.rcParams['ytick.direction'] = 'in' # y axis in 
plt.rcParams['axes.linewidth'] = 1.0 # axis line width
plt.rcParams['axes.grid'] = True # make grid

markers=["o","s", "v", "^", "2", "3"]

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
                    #print(f'{before}:{target}')
                    if before != target:
                        result.append(tmp_result)
                        tmp_result=[]
                        before=target
                    tmp_result.append(float(row[1]))

    result.append(tmp_result)

    return result
    
def calc_max_f2(list_recall,list_precision,targets):
    
    index=0
    for target in targets:
        
        recall_np=np.array(list_recall[index])
        precision_np=np.array(list_precision[index])

        f2_np=5*((recall_np*precision_np)/((4*precision_np)+recall_np))
        max_f2=np.max(f2_np)
        max_index=np.argmax(f2_np)
        print(f'Model:{target},f2:{max_f2},epoch:{max_index*25+25},recall:{recall_np[max_index],}precision:{precision_np[max_index]}')
        print()
        index+=1

        



target_metric='map'
#target_metric='recall_0.5'
#target_metric='recall_0.75'
#target_metric='precision_0.5'
#target_metric='precision_0.75'

targets=['Real_1235','CG_1235','t2_cycle_200','t2_retina_200','t2_real_CG','t2_real_cycle','t2_real_retina']
#targets=['Real_1235','t2_real_CG','t2_real_cycle','t2_real_retina']

recall=load_metric('recall_0.5',targets)
precision=load_metric('precision_0.5',targets)

calc_max_f2(recall,precision,targets)
# print(name)
# print(result)
