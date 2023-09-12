import shutil
import pathlib

start=4940
end=9881
input_dir=Path('/home/owner/taguchi/data/kikurage_data')
output_dir=Path('/home/owner/taguchi/RetinaGan/cyclegan/datasets/obj/testA')
count=0

for num in range(start,end):
    count=count+1
    img_input=Path(f'IMG_{num}.jpg')
    txt_input=Path(f'IMG_{num}.txt')
    img_output=Path(f'IMG_{count}.jpg')
    txt_output=Path(f'IMG_{count}.txt')
    shutil.copyfile(input_dir/img_name,output_dir/img_output)
    shutil.copyfile(input_dir/txt_name,output_dir/txt_output)


