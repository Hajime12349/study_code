import argparse
import io
import os
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

import darknet


@dataclass
class Detection:
    """検出データを変数に対応させる"""

    _detection: tuple

    class_name: str = field(init=False)
    confidence: str = field(init=False)
    x_center: float = field(init=False)
    y_center: float = field(init=False)
    width: float = field(init=False)
    height: float = field(init=False)

    def __post_init__(self) -> None:
        self.class_name = self._detection[0]
        self.confidence = self._detection[1]
        self.x_center = self._detection[2][0]
        self.y_center = self._detection[2][1]
        self.width = self._detection[2][2]
        self.height = self._detection[2][3]


@dataclass
class DarknetParameters:
    """Darknet のパラメータを管理"""

    network: Any = field(init=False)
    class_names: Any = field(init=False)
    class_colors: Any = field(init=False)
    txt_widht: Any = field(init=False)
    thresh: float = field(init=False)

    def __post_init__(self) -> None:
        args = parser()  # 引数をパース
        check_arguments_errors(args)  # 引数の値をチェック
        # ネットワーク構造をロード
        network, class_names, class_colors,txt_width = darknet.load_network(
            args.config_file, args.data_file, args.weights, batch_size=args.batch_size
        )

        self.network = network
        self.class_names = class_names
        self.class_colors = class_colors
        self.txt_widht=txt_width
        self.thresh = args.thresh


def parser():
    weights_path =str( Path(r"backup\yolo-obj_final_Mix.weights"))
    config_path = str(Path(".")/Path(r"yolo-obj.cfg"))
    data_path = str(Path(".")/Path(r"data\obj.data"))
    # config_path = str(Path(".")/Path(r"yolo-obj_one.cfg"))
    # data_path = str(Path(".")/Path(r"data\obj_one.data"))
    print(config_path)

    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument(
        "--input",
        type=str,
        default="",
        help="image source. It can be a single image, a"
        "txt with paths to them, or a folder. Image valid"
        " formats are jpg, jpeg or png."
        "If no input is given, ",
    )
    parser.add_argument(
        "--batch_size",
        default=1,
        type=int,
        help="number of images to be processed at the same time",
    )
    parser.add_argument("--weights", default=weights_path, help="yolo weights path")
    parser.add_argument(
        "--dont_show", action="store_true", help="windown inference display. For headless systems"
    )
    parser.add_argument(
        "--ext_output", action="store_true", help="display bbox coordinates of detected objects"
    )
    parser.add_argument(
        "--save_labels",
        action="store_true",
        help="save detections bbox for each image in yolo format",
    )
    parser.add_argument("--config_file", default=config_path, help="path to config file")
    parser.add_argument("--data_file", default=data_path, help="path to data file")
    parser.add_argument(
        "--thresh", type=float, default=0.25, help="remove detections with lower confidence"
    )
    return parser.parse_args()


def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise (ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise (ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise (ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if args.input and not os.path.exists(args.input):
        raise (ValueError("Invalid image path {}".format(os.path.abspath(args.input))))

def image_detection(image, network, class_names, class_colors,txt_width, thresh):
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height), interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    classes=[]
    boxes=[]
    scores=[]
    for detect in detections:
        classes+=[detect[0]]
        scores+=[float(detect[1])]
        boxes+=[[detect[2][0]-detect[2][2]/2,
                detect[2][1]-detect[2][3]/2,
                detect[2][0]+detect[2][2]/2,
                detect[2][1]+detect[2][3]/2]]
    boxes, scores, classes,detections = \
        soft_nms(boxes, scores, classes,detections, iou_threshold=0.3, linear=False)
    boxes, scores, classes = \
        th_bboxes(boxes, scores, classes, score_threshold=40)
    new_detections=[]
    for (class_name,score,box,detect) in zip(classes,scores,boxes,detections):
        box_tuple=(
            box[0]+detect[2][2]/2,
            box[1]+detect[2][3]/2,
            detect[2][2],
            detect[2][3],
        )
        new_detections+=[(class_name,score,box_tuple)]
    image = darknet.draw_boxes(new_detections, image, class_colors,txt_width)
    # return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections
    return image, new_detections

def convert_np(img_binary):
    img_binarystream = io.BytesIO(img_binary)

    img_pil = Image.open(img_binarystream)  # binary 形式を pil イメージに変換
    img_np = np.asarray(img_pil)  # pil から np.ndarray 形式に変換
    img_np_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)  # RGBA から RGB に変換
    return img_np_bgr

def f_linear(iou, iou_threshold=0.5):
    if iou >= iou_threshold:
        weight = 1. - iou
    else:
        weight = 1.
    return weight

# スコアの更新関数（指数関数、gauss関数）
def f_gauss(iou, sigma=0.5):
    import math
    return math.exp(-iou*iou/sigma)

def soft_nms(bboxes, scores, classes,detections, \
    iou_threshold=0.5, sigma=0.5, linear=True):
    new_bboxes = [] # Soft-NMS適用後の矩形リスト
    new_scores = [] # Soft-NMS適用後の信頼度(スコア値)リスト
    new_classes = [] # Soft-NMS適用後のクラスのリスト
    new_detections=[]
    detect_list=list(detections)

    while len(bboxes) > 0:
        # スコア最大の矩形のインデックスを取得
        argmax = scores.index(max(scores))
        # スコア最大の矩形、スコア値、クラスをそれぞれのリストから消去
        bbox = bboxes.pop(argmax)
        score = scores.pop(argmax)
        clss = classes.pop(argmax)
        detect=detect_list.pop(argmax)

        # スコア最大の矩形と、対応するスコア値、クラスをSoft-NMS適用後のリストに格納
        new_bboxes.append(bbox)
        new_scores.append(score)
        new_classes.append(clss)
        new_detections.append(detect)

        # bboxesに残存する矩形のスコアを更新
        for i, bbox_tmp in enumerate(bboxes):
            # スコア最大の矩形bboxと他の矩形のIoUを計算
            iou_tmp = iou(bbox, bbox_tmp)
            # scoreの値を更新
            if linear:
                # スコアの更新関数（線形）
                scores[i] = scores[i]*f_linear(iou_tmp, iou_threshold)
            else:
                # スコアの更新関数（指数関数、gauss関数）
                scores[i] = scores[i]*f_gauss(iou_tmp, sigma)

    return new_bboxes, new_scores, new_classes,tuple(new_detections)

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

def th_bboxes(bboxes, scores, classes, score_threshold=0.5):
    # 関数の返り値となるリストを生成
    th_bboxes = []
    th_scores = []
    th_classes = []
    for i, score in enumerate(scores):
        if score >= score_threshold:
            # スコアがscore_threshold以上の要素のみ返り値リストに保存
            th_bboxes.append(bboxes[i])
            th_scores.append(scores[i])
            th_classes.append(classes[i])

    return th_bboxes, th_scores, th_classes