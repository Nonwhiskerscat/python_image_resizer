from imgpy import Img
from datetime import date
import os
import math

# 날짜별 파일분류
today = date.today()
today_str = today.strftime("%Y%m%d")

# 수동입력
# root = input("폴더 경로를 입력하세요: ")

# 자동화
root = os.getcwd()

root_dir = root.replace("\\", "/").strip('"')

bighead_dir = root_dir + "/bighead"
origin_dir = bighead_dir + "/original"
thum_dir = bighead_dir + "/thumbnail"
prev_dir = bighead_dir + "/preview"

possible_img_extension = [
    ".jpg",
    ".jpeg",
    ".JPG",
    ".bmp",
    ".png",
    ".webp",
    ".gif",
    ".bmp",
    ".tiff",
]


class imageCustom:
    thumbnail_width = 200
    preview_width = 500

    def _thumbnail_height(cat):
        return math.ceil((imageCustom.thumbnail_width / cat.width) * cat.height)

    def _preview_height(cat):
        return math.ceil((imageCustom.preview_width / cat.width) * cat.height)

    def _thumbnail_size(cat):
        return (imageCustom.thumbnail_width, imageCustom._thumbnail_height(cat))

    def _preview_size(cat):
        return (imageCustom.preview_width, imageCustom._preview_height(cat))


def createDir(path):
    t_isdir = os.path.isdir(path)
    if t_isdir == False:
        os.mkdir(path)


def originConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        while os.path.isfile(save_path) == True:
            save_path = (
                origin_dir
                + "/"
                + os.path.splitext(file_name)[-2]
                + " ("
                + str(file_idx)
                + ")"
                + os.path.splitext(file_name)[-1]
            )
            file_idx += 1
        im.save(fp=save_path)
        print(file_name + " 원본 다운 완료")


def thumbnailConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        im.resize(imageCustom._thumbnail_size(im))
        while os.path.isfile(save_path) == True:
            save_path = (
                thum_dir
                + "/"
                + os.path.splitext(file_name)[-2]
                + " ("
                + str(file_idx)
                + ")"
                + os.path.splitext(file_name)[-1]
            )
            file_idx += 1
        im.save(fp=save_path)
        print(file_name + " 썸네일 변환 완료")


def previewConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        im.resize(imageCustom._preview_size(im))
        while os.path.isfile(save_path) == True:
            save_path = (
                prev_dir
                + "/"
                + os.path.splitext(file_name)[-2]
                + " ("
                + str(file_idx)
                + ")"
                + os.path.splitext(file_name)[-1]
            )
            file_idx += 1
        im.save(fp=save_path)
        print(file_name + " 프리뷰 변환 완료")


def cropImg(file_path, save_path):
    with Img(fp=file_path) as im:
        im.crop(box=(10, 10, 110, 110))
        im.save(fp=save_path)


if os.path.isdir(root_dir) == False:
    print("해당 경로에 폴더가 존재하지 않습니다.")

else:
    for root, dirs, files in os.walk(root_dir):
        if len(files) > 0:
            for file_name in files:
                if (
                    os.path.splitext(file_name)[-1] in possible_img_extension
                    and root == root_dir
                ):
                    createDir(bighead_dir)
                    createDir(origin_dir)
                    createDir(thum_dir)
                    createDir(prev_dir)
                    img_path = root + "/" + file_name
                    originConverter(img_path, origin_dir + "/" + file_name)
                    thumbnailConverter(img_path, thum_dir + "/" + file_name)
                    previewConverter(img_path, prev_dir + "/" + file_name)

    print("모든 작업이 끝났습니다.")

# 수동 입력 시 사용
# os.system("pause")
