from imgpy import Img
import datetime as dt
import os
import math
import configparser

# ConfigParser 객체 생성
config = configparser.ConfigParser()

# 날짜별 파일분류
now = dt.datetime.now()
# now_str = now.strftime("%Y%m%d")

# 수동입력
# root = input("폴더 경로를 입력하세요: ")

# 자동화
img_cnt = 0

root = os.getcwd()
root_dir = root.replace("\\", "/").strip('"')
bighead_dir = root_dir + "/bighead"
origin_dir = bighead_dir + "/original"
thum_dir = bighead_dir + "/thumbnail"
prev_dir = bighead_dir + "/preview"
error_dir = bighead_dir + "/error"
errorY_dir = error_dir + "/" + str(now.year)
errorM_dir = errorY_dir + "/" + str(now.month)
errorD_dir = errorM_dir + "/" + str(now.day)
errorB_dir = errorD_dir + "/오전"
errorA_dir = errorD_dir + "/오후"

possible_img_extension = []

config.read("C:/Users/김서용/Desktop/111/image_custom.ini", encoding="UTF-8")
for key in config["Image_Type"].keys():
    possible_img_extension.append(key)


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


def createDir(path):
    t_isdir = os.path.isdir(path)
    if t_isdir == False:
        os.mkdir(path)


def errorDateDir():
    createDir(error_dir)
    createDir(errorY_dir)
    createDir(errorM_dir)
    createDir(errorD_dir)


def errorLogMaker(path, msg):
    errorDateDir()
    if now.hour < 12:
        createDir(errorB_dir)
        tpath = errorB_dir + "/" + "오류로그.txt"
    else:
        createDir(errorA_dir)
        tpath = errorA_dir + "/" + "오류로그.txt"
    f = open(tpath, "a")
    f.write(str(now) + ": " + path + " " + msg + "\n")
    f.close()


errorLogMaker("mit.jpg", "파일 오류")


def originConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        try:
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
                img_cnt += 1
            im.save(fp=save_path)
            print(save_path + " 원본 다운 완료")
        except Exception as error:
            errorLogMaker(file_path, error)


def thumbnailConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        im.resize(imageCustom._thumbnail_size(im))
        try:
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
            print(save_path + " 썸네일 변환 완료")

        except Exception as error:
            errorLogMaker(file_path, error)


def previewConverter(file_path, save_path):
    file_idx = 1
    with Img(fp=file_path) as im:
        im.resize(imageCustom._preview_size(im))
        try:
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
            print(save_path + " 프리뷰 변환 완료")
        except Exception as error:
            errorLogMaker(file_path, error)


def cropImg(file_path, save_path):
    with Img(fp=file_path) as im:
        im.crop(box=(10, 10, 110, 110))
        im.save(fp=save_path)


if os.path.isdir(root_dir) == False:
    errorLogMaker(root_dir, "폴더가 존재하지 않습니다.")

else:
    for root, dirs, files in os.walk(root_dir):
        if len(files) > 0:
            for file_name in files:
                if (
                    os.path.splitext(file_name)[-1].lower() in possible_img_extension
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

    if img_cnt == 0:
        errorLogMaker(root_dir, "이미지 파일이 존재하지 않습니다.")
    else:
        print("모든 작업이 끝났습니다.")


# 수동 입력 시 사용
# os.system("pause")
