from imgpy import Img
import datetime as dt
import os
import math
import configparser
from common import *
import sys

# sys.argv[0] = file_name
# sys.argv[1~-1] = image_files

# 입력된 img 경로를 저장한 배열
i_arr = sys.argv
del i_arr[0]

# ConfigParser 객체 생성
config = configparser.ConfigParser()


# 자동화
possible_img_resize = []

config.read(FileRoot.in_root, encoding="UTF-8")
for key in config["Image_TypeI"].keys():
    possible_img_resize.append(key)

# 로그 파일 생성
log_dir = config["LogFile_Route"]["root"]
CommonDef.createDir(log_dir)


# 사이즈 조절 클래스
class imageCustom:
    # 썸네일 사이즈 정의
    thumbnail_width = int(config["Size_List"]["thumbnail"])

    def _thumbnail_height(cat):
        return math.ceil((imageCustom.thumbnail_width / cat.width) * cat.height)

    # 프리뷰 사이즈 정의
    preview_width = int(config["Size_List"]["preview"])

    def _preview_height(cat):
        return math.ceil((imageCustom.preview_width / cat.width) * cat.height)

    # 썸네일 사이즈 종합
    def _thumbnail_size(cat):
        return (imageCustom.thumbnail_width, imageCustom._thumbnail_height(cat))

    # 프리뷰 사이즈 종합
    def _preview_size(cat):
        return (imageCustom.preview_width, imageCustom._preview_height(cat))


def isPath(i_input):
    global log_msg_i
    # 파일이 누락된 경우
    if not os.path.isfile(i_input):
        log_msg_i = "유효하지 않은 패스"
        return False

    # 리사이징이 지원되지 않는 확장자인 경우
    elif CommonDef.getFileExt(i_input).lower() not in possible_img_resize:
        log_msg_i = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(i_input) + ")"
        return False

    else:
        return True


def thumbnailResizer(i_input):
    global log_msg_t
    thm_path = CommonDef.getFileName(i_input) + "t" + CommonDef.getFileExt(i_input)
    thm_output = os.path.join(CommonDef.getFileRoot(i_input), thm_path)

    try:
        with Img(fp=i_input) as im:
            im.resize(imageCustom._thumbnail_size(im))
            im.save(fp=thm_output)
            log_msg_t = "썸네일 변환 완료"
    except Exception as error_msg:
        log_msg_t = "썸네일 변환 실패 " + str(error_msg)
        return False

    return True


def previewResizer(i_input):
    global log_msg_p
    pre_path = CommonDef.getFileName(i_input) + "p" + CommonDef.getFileExt(i_input)
    pre_output = os.path.join(CommonDef.getFileRoot(i_input), pre_path)

    try:
        with Img(fp=i_input) as im:
            im.resize(imageCustom._preview_size(im))
            im.save(fp=pre_output)
            log_msg_p = "프리뷰 변환 완료"
    except Exception as error_msg:
        log_msg_p = "프리뷰 변환 실패 " + str(error_msg)
        return False

    return True


def imgResizerCommon(i_input):
    if isPath(i_input) == True:
        if thumbnailResizer(i_input) == True:
            CommonDef.makeLogTxt(i_input, log_msg_t, log_dir, True)
        else:
            CommonDef.makeLogTxt(i_input, log_msg_t, log_dir, False)

        if previewResizer(i_input) == True:
            CommonDef.makeLogTxt(i_input, log_msg_p, log_dir, True)
        else:
            CommonDef.makeLogTxt(i_input, log_msg_p, log_dir, False)
    else:
        CommonDef.makeLogTxt(i_input, log_msg_i, log_dir, False)


for img in i_arr:
    imgResizerCommon(img.replace("\\", "/").strip('"'))
