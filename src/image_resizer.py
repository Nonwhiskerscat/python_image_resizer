from imgpy import Img
import datetime as dt
import os
import math
import configparser
from common import *

# ConfigParser 객체 생성
config = configparser.ConfigParser()

f_rt, i_rt = input("파일 경로, 변경 이미지 idx(1:원본 2:썸네일 3:프리뷰 그 외: 전체): ").split()
print(f_rt, i_rt)

# 자동화
possible_img_resize = []

config.read("image_custom.ini", encoding="UTF-8")
for key in config["Resize_Type"].keys():
    possible_img_resize.append(key)


class imageCustom:
    thumbnail_width = int(config["Size_List"]["thumbnail"])
    preview_width = int(config["Size_List"]["preview"])

    def _thumbnail_height(cat):
        return math.ceil((imageCustom.thumbnail_width / cat.width) * cat.height)

    def _preview_height(cat):
        return math.ceil((imageCustom.preview_width / cat.width) * cat.height)

    def _thumbnail_size(cat):
        return (imageCustom.thumbnail_width, imageCustom._thumbnail_height(cat))

    def _preview_size(cat):
        return (imageCustom.preview_width, imageCustom._preview_height(cat))


def originConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        try:
            while os.path.isfile(save_path) == True:
                save_path = (
                    FileRoot.SubDir(f_rt, "origin")
                    + "/"
                    + os.path.splitext(file_name)[-2]
                    + " ("
                    + str(file_idx)
                    + ")"
                    + os.path.splitext(file_name)[-1]
                )
                file_idx += 1
            im.save(fp=save_path)
            print(save_path + " 원본 다운 완료")
        except Exception as error:
            CommonDef.errorLogMaker(
                file_path, str(error), FileRoot.SubDir(f_rt, "resize")
            )


def thumbnailConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        im.resize(imageCustom._thumbnail_size(im))
        try:
            while os.path.isfile(save_path) == True:
                save_path = (
                    FileRoot.SubDir(f_rt, "thumbnail")
                    + "/"
                    + os.path.splitext(file_name)[-2]
                    + " ("
                    + str(file_idx)
                    + ")"
                    + os.path.splitext(file_name)[-1]
                )
                file_idx += 1
            im.save(fp=save_path)
            print(save_path + " 썸네일 변환 완료")
        except Exception as error:
            CommonDef.errorLogMaker(
                file_path, str(error), FileRoot.SubDir(f_rt, "resize")
            )


def previewConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        im.resize(imageCustom._preview_size(im))
        try:
            while os.path.isfile(save_path) == True:
                save_path = (
                    FileRoot.SubDir(f_rt, "preview")
                    + "/"
                    + os.path.splitext(file_name)[-2]
                    + " ("
                    + str(file_idx)
                    + ")"
                    + os.path.splitext(file_name)[-1]
                )
                file_idx += 1
            im.save(fp=save_path)
            print(save_path + " 프리뷰 변환 완료")
        except Exception as error:
            CommonDef.errorLogMaker(
                file_path, str(error), FileRoot.SubDir(f_rt, "resize")
            )


def cropImg(file_path, save_path):
    with Img(fp=file_path) as im:
        im.crop(box=(10, 10, 110, 110))
        im.save(fp=save_path)


if os.path.isdir(str(FileRoot.RootDir(f_rt))) == False:
    CommonDef.errorLogMaker(
        FileRoot.RootDir(f_rt), "폴더가 존재하지 않습니다.", FileRoot.SubDir(f_rt, "resize")
    )

else:
    for root, dirs, files in os.walk(FileRoot.RootDir(f_rt)):
        if len(files) > 0:
            for file_name in files:
                if os.path.splitext(file_name)[
                    -1
                ].lower() in possible_img_resize and root == FileRoot.RootDir(f_rt):
                    CommonDef.createDir(FileRoot.SubDir(f_rt, "resize"))
                    img_path = root + "/" + file_name

                    if i_rt == "1" or (i_rt != "2" and i_rt != "3"):
                        CommonDef.createDir(FileRoot.SubDir(f_rt, "origin"))
                        originConverter(
                            img_path, FileRoot.SubDir(f_rt, "origin") + "/" + file_name
                        )

                    if i_rt == "2" or (i_rt != "1" and i_rt != "3"):
                        CommonDef.createDir(FileRoot.SubDir(f_rt, "thumbnail"))
                        thumbnailConverter(
                            img_path,
                            FileRoot.SubDir(f_rt, "thumbnail") + "/" + file_name,
                        )

                    if i_rt == "3" or (i_rt != "1" and i_rt != "2"):
                        CommonDef.createDir(FileRoot.SubDir(f_rt, "preview"))
                        previewConverter(
                            img_path, FileRoot.SubDir(f_rt, "preview") + "/" + file_name
                        )
                elif root == FileRoot.RootDir(f_rt):
                    CommonDef.createDir(FileRoot.SubDir(f_rt, "resize"))
                    CommonDef.errorLogMaker(
                        file_name, "지원하지 않는 파일 확장자입니다.", FileRoot.SubDir(f_rt, "resize")
                    )


print("모든 작업이 끝났습니다.")

# 수동 입력 시 사용
os.system("pause")
