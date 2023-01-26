from pathlib import Path
from PIL import Image
from tqdm import tqdm
import yaml


def main():
    config_path = "./config.yaml"
    conf = yaml.safe_load(open(config_path))

    p_in = Path(conf["background_img_dir"])
    p_out = Path(conf["croped_img_dir"])
    p_out.mkdir(parents=True, exist_ok=True)

    exts = ["jpg", "png", "bmp", "gif", "jpeg"]
    img_list = [x for ext in exts for x in p_in.glob(f"*.{ext}") if x.is_file()]

    pbar = tqdm(img_list, desc="Processing")

    for i, f in enumerate(pbar):
        img = Image.open(str(f))

        # 小さい画素数に合わせる
        min_ = min(img.size)
        img = crop_center(img, width=min_, height=min_)

        out = p_out.joinpath(f"{f.stem}.jpg")
        img.convert("RGB").save(out)


def crop_center(img: Image.Image, width: int, height: int):
    w, h = img.size
    box = ((w - width) // 2, (h - height) // 2, (w + width) // 2, (h + height) // 2)
    return img.crop(box)


if __name__ == "__main__":
    main()
