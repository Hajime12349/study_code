from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import NamedTuple

import cv2

import darknet_module
from darknet_module import DarknetParameters, Detection




def save_data_sequentially(
    dn_comp:DarknetParameters,
    save_dir: Path,
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
    img_save_path = save_dir / f"{filename}.jpg"
    cv2.imwrite(str(img_save_path), img_detected)  # detected image
    #cv2.imwrite(str(img_save_path), img_np)  # original image

    # 検出データの保存
    txt_save_path = save_dir / f"{filename}.txt"
    class_number={'harvestable':0,'soon':1,'not_yet':2}
    with open(txt_save_path, mode="w") as f:
        for detect in detections:
            format_str=f'{class_number[detect[0]]} {detect[2][0]/416} {detect[2][1]/416} {detect[2][2]/416} {detect[2][3]/416} {detect[1]}\n'
            f.write(format_str)
        print(txt_save_path)


def main() -> None:
    # 保存先のディレクトリの定義と作成
    dn_comp = DarknetParameters()
    save_root = Path(".")
    save_root = save_root / "python_result"
    print(save_root)
    test_txt_path=r"C:\Taguchi\seityoudo_Darknet\darknet-master\build\darknet\x64\data\test.txt"
    with open(test_txt_path) as f:
        list_test_txt = f.readlines()
    count_img=10001
    for image_name in list_test_txt:
        image_name=image_name.replace('/','\\')
        image_name=image_name.rstrip('\n')
        print(image_name)
        original_image=cv2.imread(image_name)
        save_data_sequentially(
            dn_comp,
            save_root,
            original_image,
            count_img
        )
        count_img+=1
if __name__ == "__main__":
    main()