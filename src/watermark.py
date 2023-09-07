# from common import add_func, FileRoot

from wand.image import Image
import os
from imgpy import Img
import math
import configparser
from common import *


global img_cnt
img_cnt = False

root = os.getcwd()
root_dir = root.replace("\\", "/").strip('"')
watermark_dir = root_dir + "/watermark"
daily_dir = watermark_dir + "/daily"
sports_dir = watermark_dir + "/sports"
dotcom_dir = watermark_dir + "/dotcom"
error_dir = watermark_dir + "/error"

# 자동화
possible_img_watermark = []

# ConfigParser 객체 생성
config = configparser.ConfigParser()

config.read("image_custom.ini", encoding="UTF-8")
for key in config["Water_Type"].keys():
    possible_img_watermark.append(key)


w_mark_route = input("워터마크 이미지")


def wWidth(width):
    return math.ceil(width * 0.15)


def wHeight(wmark, wwidth):
    w_ratio = wmark.size[0] / wmark.size[1]
    return math.ceil(wwidth / w_ratio)


def wMake(file_path, save_path):
    with Image(filename=file_path) as im:
        print(im)
        w_mark = Image(filename=w_mark_route)
        w_mark.resize(wWidth(im.size[0]), wHeight(w_mark, wWidth(im.size[0])))
        x_axis = im.size[0] - math.ceil(1.1 * w_mark.size[0])
        y_axis = im.size[1] - w_mark.size[1] - math.ceil(0.1 * w_mark.size[0])
        im.watermark(image=w_mark, transparency=0.3, left=x_axis, top=y_axis)
        im.save(filename=save_path)


if os.path.isdir(FileRoot.root_dir) == False:
    CommonDef.errorLogMaker(FileRoot.root_dir, "폴더가 존재하지 않습니다.")
else:
    for root, dirs, files in os.walk(FileRoot.root_dir + "/연습용 사진"):
        if len(files) > 0:
            for file_name in files:
                if (
                    os.path.splitext(file_name)[-1].lower() in possible_img_watermark
                    and root == FileRoot.root_dir + "/연습용 사진"
                ):
                    CommonDef.createDir(FileRoot.watermark_dir)
                    img_path = root + "/" + file_name
                    wMake(img_path, FileRoot.watermark_dir + "/" + file_name)

                elif root == FileRoot.root_dir + "/연습용 사진":
                    CommonDef.errorLogMaker(file_name, "지원하지 않는 파일 확장자입니다.")

print("모든 작업이 끝났습니다.")
