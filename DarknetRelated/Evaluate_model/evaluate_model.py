from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from tkinter import W
from typing import NamedTuple

import cv2
import re
import csv



def main() -> None:
    # 保存先のディレクトリの定義と作成
    save_root = Path(".")
    csv_output = save_root/"iou_result.csv"
    # print(save_root)

    # テストデータのpath読み込み
    test_txt_path = Path(".") / r'test.txt'
    with open(test_txt_path) as f:
        list_test_txt = f.readlines()

    # iou計算
    precision_iou_score_lists = []
    recall_iou_score_lists = []
    recall_lists=[]
    precision_lists=[]
    #iou_score_average = 0
    recall_TP_count = 0
    precision_TP_count = 0
    recall_count=0
    precision_count=0
    for image_name in list_test_txt:
        #image_name = image_name.replace('/', '\\')
        image_name = image_name.rstrip('\n')
        answer_path = image_name.replace('.jpg', '.txt')
        answer_path = answer_path.replace('.png', '.txt')
        detected_path=answer_path.replace('test/','')
        answer_path = Path('.') / answer_path
        print(answer_path)
        with open(answer_path, 'r', encoding="utf-8_sig") as answer_txt:
            answer_list = answer_txt.readlines()
            # print(answer_list)
        answer_box_list = create_box(answer_list)

        # trimed_name = re.search('test\d*', image_name)
        # file_name=trimed_name.group()+'.txt'
        # detected_path = Path('.') /file_name
        print(detected_path)
        with open(detected_path, 'r', encoding="utf-8_sig") as detected_txt:
            detected_list = detected_txt.readlines()
        detected_box_list = create_box(detected_list)

        #recallのIoUを計測
        iou_score_list_tmp = []
        recall_list_tmp = 0
        for i in range(len(answer_list)):
            iou_score = 0
            for j in range(len(detected_list)):
                # 最も高いスコアのボックスが対応するボックスであるとして適応
                score_tmp = iou(answer_box_list[i], detected_box_list[j])
                #print(str(answer_box_list[i])+':'+str(detected_box_list[j]))
                #print(score_tmp)
                iou_score=round(max(iou_score, score_tmp),3)
            #print(iou_score)
            #iou_score_average = (iou_count*iou_score_average+iou_score)/(iou_count+1)
            recall_count += 1
            iou_score_list_tmp.append(iou_score)
            judge=iou_judge(iou_score)
            recall_list_tmp+=judge
            if judge=='T':
                recall_TP_count+=1
        if not iou_score_list_tmp:
            recall_iou_score_lists.append(['empty'])
            recall_lists.append(['empty'])
        else:
            recall_iou_score_lists.append(iou_score_list_tmp)
            recall_lists.append([recall_list_tmp/len(answer_list)])

        #precisionのIoUを計測
        iou_score_list_tmp = []
        precision_list_tmp = 0
        for i in range(len(detected_list)):
            iou_score = 0
            for j in range(len(answer_list)):
                # 最も高いスコアのボックスが対応するボックスであるとして適応
                score_tmp = iou(answer_box_list[j], detected_box_list[i])
                #print(str(answer_box_list[i])+':'+str(detected_box_list[j]))
                #print(score_tmp)
                iou_score=round(max(iou_score, score_tmp),3)
            #print(iou_score)
            #iou_score_average = (iou_count*iou_score_average+iou_score)/(iou_count+1)
            precision_count += 1
            iou_score_list_tmp.append(iou_score)
            judge=iou_judge(iou_score)
            print(judge)
            precision_list_tmp+=judge
            if judge=='T':
                precision_TP_count+=1
        if not iou_score_list_tmp:
            precision_iou_score_lists.append(['empty'])
            precision_lists.append(['empty'])
        else:
            precision_iou_score_lists.append(iou_score_list_tmp)
            precision_lists.append([precision_list_tmp/len(detected_list)])

    # 結果の表示・出力
    #print(f'iou_count:{iou_count}\niou_average:{iou_score_average}\n')
    with open(csv_output, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f'precision:',precision_TP_count/precision_count])
        writer.writerow([f'recall:',recall_TP_count/recall_count])
        print(precision_TP_count/precision_count)
        print(recall_TP_count/recall_count)
        print(recall_TP_count)
        print(precision_TP_count)
        writer.writerow([])
        writer.writerow(['\nここからPrecision\n'])
        for iou_list in precision_lists:
            writer.writerow(iou_list)
            writer.writerow([])
        writer.writerow(['\nここからRecall\n'])
        for iou_list in recall_lists:
            writer.writerow(iou_list)
            writer.writerow([])

def create_box(raw_data):
    data_list = []
    for data_tmp in raw_data:
        data = data_tmp.split()
        #print(data_tmp)
        print(data)
        box = [float(data[1])-float(data[3])/2,
                float(data[2])-float(data[4])/2,
                float(data[1])+float(data[3])/2,
                float(data[2])+float(data[4])/2]
        data_list.append(box)
    return data_list

def iou_judge(iou):
    if iou>0.5:
        return 1
    return 0

def iou(a, b):
    eps=0.00001
    # a, bは矩形を表すリストで、a=[xmin, xmax, ymin, ymax]
    ax_mn, ay_mn, ax_mx, ay_mx = a[0], a[1], a[2], a[3]
    bx_mn, by_mn, bx_mx, by_mx = b[0], b[1], b[2], b[3]

    a_area = (ax_mx - ax_mn + eps) * (ay_mx - ay_mn + eps)
    b_area = (bx_mx - bx_mn + eps) * (by_mx - by_mn + eps)

    abx_mn = max(ax_mn, bx_mn)
    aby_mn = max(ay_mn, by_mn)
    abx_mx = min(ax_mx, bx_mx)
    aby_mx = min(ay_mx, by_mx)
    w = max(0, abx_mx - abx_mn + eps)
    h = max(0, aby_mx - aby_mn + eps)
    intersect = w*h

    iou = intersect / (a_area + b_area - intersect)
    return iou



if __name__ == "__main__":
    main()
