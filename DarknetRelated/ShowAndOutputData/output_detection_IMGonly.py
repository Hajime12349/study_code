#from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import NamedTuple

import cv2

import darknet_module
from darknet_module import DarknetParameters, Detection




def save_data_sequentially(
    dn_comp:DarknetParameters,
    img_save_dir: Path,
    img,
    count:int
) -> None:

    """画像、検出データをすべて保存する

    Args:
        dn_comp (DarknetComponent): Darknetに使用するパラメータ
        img_info_list (list[ImageInfo]): 受信画像
        img_save_dir (Path): 画像の保存先ディレクトリのパス
        txt_save_dir (Path): 検出データの保存先ディレクトリのパス
    """
    # キクラゲの検出
    img_detected, detections = darknet_module.image_detection(
        img, dn_comp.network, dn_comp.class_names, dn_comp.class_colors,dn_comp.txt_widht, dn_comp.thresh
    )

    # 画像の保存
    filename = f"IMG_{count}"
    img_save_path = img_save_dir / f"{filename}.jpg"
    cv2.imwrite(str(img_save_path), img_detected)  # detected image
    #cv2.imwrite(str(img_save_path), img_np)  # original image

    # # 検出データの保存
    # txt_save_path = txt_save_dir / f"{filename}.txt"
    # with open(txt_save_path, mode="w") as f:
    #     f.write(str(detections))
    #     print(txt_save_path)


def main() -> None:
    # 保存先のディレクトリの定義と作成
    dn_comp = DarknetParameters()
    save_root = Path(".")
    img_save_root = save_root / "python_result"
    print(img_save_root)
    test_txt_path=r"C:\Taguchi\seityoudo_Darknet\darknet-master\build\darknet\x64\data\test.txt"
    with open(test_txt_path) as f:
        list_test_txt = f.readlines()
    count_img=1
    for test_txt in list_test_txt:
        test_txt=test_txt.replace('/','\\')
        test_txt=test_txt.rstrip('\n')
        #original_image=cv2.imread("./"+test_txt)
        print(test_txt)
        original_image=cv2.imread(test_txt)
        #cv2.imshow("a",original_image)
        save_data_sequentially(
            dn_comp,
            img_save_root,
            original_image,
            count_img
        )
        count_img+=1
if __name__ == "__main__":
    main()