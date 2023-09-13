# from common import add_func, FileRoot

from wand.image import Image
import os
from imgpy import Img
import math
import configparser
from common import *

# import sys
# from os.path import dirname

# 자동화
possible_img_watermark = []

# ConfigParser 객체 생성


def wWidth(width):
    return math.ceil(width * 0.15)


def wHeight(wmark, wwidth):
    w_ratio = wmark.size[0] / wmark.size[1]
    return math.ceil(wwidth / w_ratio)


def wMake(file_path, save_path):
    with Image(filename=file_path) as im:
        w_mark = Image(filename=w_mark_route)
        w_mark.resize(wWidth(im.size[0]), wHeight(w_mark, wWidth(im.size[0])))
        x_axis = im.size[0] - math.ceil(1.1 * w_mark.size[0])
        y_axis = im.size[1] - w_mark.size[1] - math.ceil(0.1 * w_mark.size[0])
        im.watermark(image=w_mark, transparency=0.3, left=x_axis, top=y_axis)
        im.save(filename=save_path)
        print(save_path + "워터마크 이미지 제작 완료")


config = configparser.ConfigParser()

config.read("image_custom.ini", encoding="UTF-8")
for key in config["Water_Type"].keys():
    possible_img_watermark.append(key)

f_rt, w_rt = input("파일 경로, 워터마크 idx(1:동아일보, 4:스포츠동아, 5:동아닷컴, 그 외:동아일보): ").split()
print(f_rt, w_rt)

if w_rt == "1":
    w_mark_route = config["Water_Route"]["donga_daily"]
elif w_rt == "4":
    w_mark_route = config["Water_Route"]["donga_sports"]
elif w_rt == "5":
    w_mark_route = config["Water_Route"]["donga_dotcom"]
else:
    w_mark_route = config["Water_Route"]["donga_daily"]


if os.path.isdir(FileRoot.RootDir(f_rt)) == False:
    CommonDef.errorLogMaker(
        FileRoot.RootDir(f_rt), "폴더가 존재하지 않습니다.", FileRoot.SubDir(f_rt, "watermark")
    )
else:
    for root, dirs, files in os.walk(FileRoot.RootDir(f_rt)):
        if len(files) > 0:
            for file_name in files:
                if os.path.splitext(file_name)[
                    -1
                ].lower() in possible_img_watermark and root == FileRoot.RootDir(f_rt):
                    CommonDef.createDir(FileRoot.SubDir(f_rt, "watermark"))
                    img_path = root + "/" + file_name
                    wMake(
                        img_path, FileRoot.SubDir(f_rt, "watermark") + "/" + file_name
                    )

                elif root == FileRoot.RootDir(f_rt):
                    CommonDef.createDir(FileRoot.SubDir(f_rt, "watermark"))
                    CommonDef.errorLogMaker(
                        file_name,
                        "지원하지 않는 파일 확장자입니다.",
                        FileRoot.SubDir(f_rt, "watermark"),
                    )
print("모든 작업이 끝났습니다.")
os.system("pause")
