from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from tkinter import W
from typing import NamedTuple

import cv2
import re
import csv

import darknet_module
from darknet_module import DarknetParameters, Detection


def main() -> None:
    evaluate_class=1

    # 保存先のディレクトリの定義と作成
    save_root = Path(".") / r'python_result\evaluate'
    csv_output = save_root/"iou_result.csv"
    # print(save_root)

    # テストデータのpath読み込み
    test_txt_path = Path(".") / r'data\test.txt'
    with open(test_txt_path) as f:
        list_test_txt = f.readlines()

    # iou計算
    precision_iou_score_lists = []
    recall_iou_score_lists = []
    recall_lists=[]
    precision_lists=[]
    conf_rank_list=[] #lists list , lists=[confidence,isTP,]
    #iou_score_average = 0
    TP_count = 0
    recall_count=0
    precision_count=0
    for image_name in list_test_txt:
        #image_name = image_name.replace('/', '\\')
        image_name = image_name.rstrip('\n')
        answer_path = image_name.replace('.jpg', '.txt')
        answer_path = answer_path.replace('.png', '.txt')
        answer_path = Path('.') / answer_path
        print(answer_path)
        with open(answer_path, 'r', encoding="utf-8_sig") as answer_txt:
            answer_list = answer_txt.readlines()
            # print(answer_list)
        answer_box_list = create_box(answer_list,evaluate_class)

        trimed_name = re.search('IMG_\d*', image_name)
        file_name=trimed_name.group()+'.txt'
        detected_path = Path('.') /'python_result'/file_name
        #print(detected_path)
        with open(detected_path, 'r', encoding="utf-8_sig") as detected_txt:
            detected_list = detected_txt.readlines()
        detected_box_list = create_box(detected_list,evaluate_class)

        #recallのIoUを計測
        iou_score_list_tmp = []
        recall_list_tmp = []
        print(len(answer_box_list))
        for i in range(len(answer_box_list)):
            iou_score = 0
            for j in range(len(detected_box_list)):
                # 最も高いスコアのボックスが対応するボックスであるとして適応
                score_tmp = darknet_module.iou(answer_box_list[i], detected_box_list[j])
                #print(str(answer_box_list[i])+':'+str(detected_box_list[j]))
                #print(score_tmp)
                iou_score=round(max(iou_score, score_tmp),3)
            #print(iou_score)
            #iou_score_average = (iou_count*iou_score_average+iou_score)/(iou_count+1)
            recall_count += 1
            iou_score_list_tmp.append(iou_score)
            judge=iou_judge(iou_score)
            recall_list_tmp.append(judge)
            if judge=='T':
                TP_count+=1
        if not iou_score_list_tmp:
            recall_iou_score_lists.append(['empty'])
            recall_lists.append(['empty'])
        else:
            recall_iou_score_lists.append(iou_score_list_tmp)
            recall_lists.append(recall_list_tmp)

        #precisionのIoUを計測
        iou_score_list_tmp = []
        precision_list_tmp = []
        for i in range(len(detected_box_list)):
            iou_score = 0
            for j in range(len(answer_box_list)):
                # 最も高いスコアのボックスが対応するボックスであるとして適応
                score_tmp = darknet_module.iou(answer_box_list[j], detected_box_list[i])
                #print(str(answer_box_list[i])+':'+str(detected_box_list[j]))
                #print(score_tmp)
                iou_score=round(max(iou_score, score_tmp),3)
            #print(iou_score)
            #iou_score_average = (iou_count*iou_score_average+iou_score)/(iou_count+1)
            precision_count += 1
            iou_score_list_tmp.append(iou_score)
            judge=iou_judge(iou_score)
            precision_list_tmp.append(judge)
            confidence=detected_list[i].split()
            conf_rank_list.append([confidence[5],judge])
            # if judge=='T':
            #     precision_TP_count+=1
        if not iou_score_list_tmp:
            precision_iou_score_lists.append(['empty'])
            precision_lists.append(['empty'])
        else:
            precision_iou_score_lists.append(iou_score_list_tmp)
            precision_lists.append(precision_list_tmp)

    #APを算出
    # conf_rank_list=sorted(conf_rank_list, reverse=True, key=lambda x: x[0])
    # print(len(conf_rank_list))
    # ap_score=0
    # count_data=0
    # count_now_TP=0
    # count_continuous_TP=0
    # for data in conf_rank_list:
    #     count_data+=1
    #     if data[1]=='F':
    #         count_now_TP+=count_continuous_TP
    #         now_precision=count_now_TP/count_data
    #         ap_score+=now_precision*count_continuous_TP
    #         count_continuous_TP=0
    #     else:
    #         count_continuous_TP+=1

    #     print(f'{data[0]}:{data[1]}')
    # print(count_now_TP)

    # 結果の表示・出力
    #print(f'iou_count:{iou_count}\niou_average:{iou_score_average}\n')
    precision=TP_count/precision_count
    recall=TP_count/recall_count
    F_measure=(2*recall*precision)/(recall+precision)
    with open(csv_output, 'w', newline="") as f:
        print(recall_count)
        writer = csv.writer(f)
        writer.writerow([f'precision:',precision])
        writer.writerow([f'recall:',recall])
        writer.writerow([f'F_measure:',F_measure])
        writer.writerow([])
        writer.writerow(['\nここからPrecision\n'])
        for iou_list,precision_list in zip(precision_iou_score_lists,precision_lists):
            writer.writerow(iou_list)
            writer.writerow(precision_list)
            writer.writerow([])
        writer.writerow(['\nここからRecall\n'])
        for iou_list,recall_list in zip(recall_iou_score_lists,recall_lists):
            writer.writerow(iou_list)
            writer.writerow(recall_list)
            writer.writerow([])

def create_box(raw_data,evaluate_class):
    data_list = []
    for data_tmp in raw_data:
        data = data_tmp.split()
        if int(data[0])==evaluate_class:
            #print(data_tmp)
            box = [float(data[1])-float(data[3])/2,
                    float(data[2])-float(data[4])/2,
                    float(data[1])+float(data[3])/2,
                    float(data[2])+float(data[4])/2]
            data_list.append(box)
    return data_list

def iou_judge(iou):
    if iou>0.5:
        return 'T'
    return 'F'



if __name__ == "__main__":
    main()
