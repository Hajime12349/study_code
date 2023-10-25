import shutil
from pathlib import Path

#start:start number
#end:end number
start=1
end=1235
end=end+1
#input_dir=Path('/home/owner/taguchi/data/kikurage_data')
input_dir=Path('/home/owner/taguchi/RetinaGan/cyclegan/test/t2_cycle_200/datasets')
#output_dir=Path('/home/owner/taguchi/RetinaGan/cyclegan/datasets/obj/testA')
#output_dir=Path('/home/owner/taguchi/data/test_real')
output_dir=Path('/home/owner/taguchi/RetinaGan/cyclegan/test/t2_retina_200_box1_prcp0.5/datasets')

count=0

for num in range(start,end):
    count=count+1
    img_input=Path(f'IMG_{num}.jpg')
    txt_input=Path(f'IMG_{num}.txt')
    #img_output=Path(f'IMG_{count}.jpg')
    #txt_output=Path(f'IMG_{count}.txt')
    img_output=img_input
    txt_output=txt_input
    #shutil.copyfile(input_dir/img_input,output_dir/img_output)
    shutil.copyfile(input_dir/txt_input,output_dir/txt_output)
    print(img_input)

