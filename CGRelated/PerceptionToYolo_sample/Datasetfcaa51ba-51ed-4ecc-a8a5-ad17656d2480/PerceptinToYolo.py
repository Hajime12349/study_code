import sys
import json
import os

def main():
    print("hello")
    json_count=0
    data_count=0
    image_size=416
    while True:
        json_path=f'captures_{str(json_count).zfill(3)}.json'
        try:
            detected_datas=json.load(open(json_path,'r'))
        except:
            print("End")
            break
        print(f'{json_path} is openning')
        for detect_cap in detected_datas["captures"]:
            data_count+=1
            print(f'Now:{data_count}')
            annotations=detect_cap["annotations"][0]
            yolo_str=''
            for detect in annotations["values"]:
                class_index=0
                width=detect['width']/image_size
                height=detect['height']/image_size
                center_x=detect['x']/image_size+width/2
                center_y=detect['y']/image_size+height/2
                yolo_str+=format("{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(class_index,center_x,center_y,width,height))
            with open(rf'yolo\data_{data_count}.txt', mode='w') as f:
                f.write(yolo_str)

        json_count+=1

if __name__ == "__main__":
    main()
