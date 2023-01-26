from pathlib import Path
import re
import csv

# YOLO形式データから矩形領域データを抽出
# raw_data  :YOLO形式データ
# data_list :矩形領域の各頂点の位置データ
def create_box(raw_data):
    data_list = []
    for data_tmp in raw_data:
        data = data_tmp.split()
        #print(data_tmp)
        box = [float(data[1])-float(data[3])/2,
                float(data[2])-float(data[4])/2,
                float(data[1])+float(data[3])/2,
                float(data[2])+float(data[4])/2]
        data_list.append(box)
    return data_list

#IoUスコアを算出する関数
#a,d    :矩形領域のリスト
#return :IoUのスコア
def iou(a, d):
    eps=0.00001 #ε：計算結果がゼロになるのを防ぐための微小値
    #xy軸で矩形領域の抽出
    ax_min, ay_min, ax_max, ay_max = a[0], a[1], a[2], a[3]
    dx_min, dy_min, dx_max, dy_max = d[0], d[1], d[2], d[3]

    #各矩形の面積を計算
    a_area = (ax_max - ax_min + eps) * (ay_max - ay_min + eps)
    d_area = (dx_max - dx_min + eps) * (dy_max - dy_min + eps)

    #矩形の積集合の面積を計算
    adx_min = max(ax_min, dx_min)
    ady_min = max(ay_min, dy_min)
    adx_max = min(ax_max, dx_max)
    ady_max = min(ay_max, dy_max)
    w = max(0, adx_max - adx_min + eps)
    h = max(0, ady_max - ady_min + eps)
    intersect = w*h

    #矩形の和集合の面積を計算
    union=a_area + d_area - intersect

    #IoUスコア算出
    iou = intersect / union
    return iou

#TPであるかどうか判定
#iou    :IoUのスコア
#return :判定結果
def iou_judge(iou):
    if iou>=0.5:    #閾値0.5
        return 'T'
    return 'F'

#適合率を計算
#answer_list：正解の矩形データリスト,detected_list：検出した矩形データリスト
#return:適合率
def calc_precision(answer_list,detected_list):
    iou_score_list_tmp = []
    precision_list_tmp = []
    precision_count=0
    TP_count=0
    for i in range(len(detected_list)):
        iou_score = 0
        for j in range(len(answer_list)):
            # 最も高いスコアのボックスが対応するボックスであるとして適応
            score_tmp = iou(answer_list[j], detected_list[i])
            iou_score=round(max(iou_score, score_tmp),3)
        precision_count += 1
        iou_score_list_tmp.append(iou_score)
        judge=iou_judge(iou_score)
        precision_list_tmp.append(judge)
        if judge=='T':
            TP_count+=1
    precision=TP_count/precision_count
    return precision

#再現率を計算
#answer_list：正解の矩形データリスト,detected_list：検出した矩形データリスト
#return:再現率
def calc_recall(answer_list,detected_list):
    iou_score_list_tmp = []
    recall_list_tmp = []
    recall_count=0
    TP_count=0
    for i in range(len(answer_list)):
        iou_score = 0
        for j in range(len(detected_list)):
            # 最も高いスコアのボックスが対応するボックスであるとして適応
            score_tmp = iou(answer_list[i], detected_list[j])
            iou_score=round(max(iou_score, score_tmp),3)
        recall_count += 1
        iou_score_list_tmp.append(iou_score)
        judge=iou_judge(iou_score)
        recall_list_tmp.append(judge)
        if judge=='T':
            TP_count+=1
    recall=TP_count/recall_count
    return recall


#F値を計算
#precision:適合率,recall:再現率
#return:F値
def calc_f(precision,recall):
    f=(2*precision*recall)/(precision+recall+0.0001)
    return f

# 逐次平均計算
def calc_average(previous_average,value,count):
    average=1/(1+count)*(count*previous_average+value)
    return average


def main() -> None:
    # 保存先のディレクトリの定義と作成
    save_root = Path(".") / r'python_result\evaluate'
    csv_output = save_root/"iou_result.csv"
    # print(save_root)

    # テストデータのpath読み込み
    test_txt_path = Path(".") / r'data\test.txt'
    with open(test_txt_path) as f:
        list_test_txt = f.readlines()

    #全テストデータの評価を行う
    count=0
    precision=0
    recall=0
    f_score=0
    for image_name in list_test_txt:
        #正解データの抽出
        image_name = image_name.rstrip('\n')
        answer_path = image_name.replace('.jpg', '.txt')
        answer_path = answer_path.replace('.png', '.txt')
        answer_path = Path('.') / answer_path
        print(answer_path)
        with open(answer_path, 'r', encoding="utf-8_sig") as answer_txt:
            answer_list = answer_txt.readlines()
        answer_box_list = create_box(answer_list)

        # 検出データの抽出
        trimed_name = re.search('IMG_\d*', image_name)
        file_name=trimed_name.group()+'.txt'
        detected_path = Path('.') /'python_result'/file_name
        with open(detected_path, 'r', encoding="utf-8_sig") as detected_txt:
            detected_list = detected_txt.readlines()
        detected_box_list = create_box(detected_list)

        # 評価結果の算出
        if len(detected_box_list)!=0:
            p=calc_precision(answer_box_list,detected_box_list)
            precision=calc_average(precision,p,count)
        if len(answer_box_list)!=0:
            r=calc_recall(answer_box_list,detected_box_list)
            recall=calc_average(recall,r,count)

        count+=1

    # 結果の表示・出力
    print(f'Precision:{precision}')
    print(f'Recall:{recall}')
    print(f'F-score:{calc_f(precision,recall)}')

if __name__ == "__main__":
    main()
