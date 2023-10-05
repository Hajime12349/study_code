import shutil
import os
import re
from pathlib import Path

#start:start number
#end:end number
start=25
end=300
end=end+1
step=25

dataset_list=['Real_1235',
            'CG_1235',
            't2_cycle_200',
            't2_retina_200',
            't2_retina_200_box1',
            't2_retina_200_box10',
            't2_retina_200_prcp0.5',
            't2_retina_200_prcp1',
            't2_retina_200_prcp10',
]

for dataset_name in dataset_list:
    target_dataset=Path(f'./{dataset_name}')

    input_dir=target_dataset/Path('ckpt')
    output_dir=input_dir

    count=0

    for num in range(start,end,step):
        print(num)
        count=count+1
        input_name=None
        output_name=f'epoch{num}.ckpt'
        pattern=re.compile(rf'epoch={num-1}-.*')
        
        
        for root, dirs, files in os.walk(input_dir):
            for file_name in files:
                #print(file_name)
                if re.search(pattern, file_name):
                    input_name= file_name
        
        if input_name:
            print(f'{input_name} to {output_name}')
            shutil.copyfile(input_dir/input_name,output_dir/output_name)
