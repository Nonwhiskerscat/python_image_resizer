import os
import math
import configparser
from PIL import Image
import sys
from common import *

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


# 정적 이미지 로테이트 메서드
def resizeImg(img, size):
    img_resized = img.resize(size)
    return img_resized


# 동적 이미지 로테이트 메서드
def resizeGif(input, output, size):
    with Image.open(input) as im:
        frames = []

        # 프레임 추출 및 각 프레임 회전
        for frame in range(im.n_frames):
            im.seek(frame)
            resized_frame = resizeImg(im.copy(), size)
            frames.append(resized_frame)

        # 회전된 프레임을 새로운 GIF 파일로 저장
        frames[0].save(output, save_all=True, append_images=frames[1:], loop=0)


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
        if CommonDef.getFileExt(i_input).lower() != ".gif":
            with Image.open(i_input) as im:
                resized_img = resizeImg(im, imageCustom._thumbnail_size(im))
                resized_img.save(fp=thm_output)

        else:
            gif_img = Image.open(i_input)
            resizeGif(i_input, thm_output, imageCustom._thumbnail_size(gif_img))
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
        if CommonDef.getFileExt(i_input).lower() != ".gif":
            with Image.open(i_input) as im:
                resized_img = resizeImg(im, imageCustom._preview_size(im))
                resized_img.save(fp=pre_output)

        else:
            gif_img = Image.open(i_input)
            resizeGif(i_input, pre_output, imageCustom._preview_size(gif_img))

        log_msg_p = "프리뷰 변환 완료"
    except Exception as error_msg:
        log_msg_p = "프리뷰 변환 실패 " + str(error_msg)
        return False

    return True


def freeResizer(i_input, width, height):
    global log_msg_f
    i_img = Image.open(i_input)
    if not height:
        height = (width / i_img.width) * i_img.height

    free_path = f"{CommonDef.getFileName(i_input)}f_{width}_{int(height)}{CommonDef.getFileExt(i_input)}"
    free_output = os.path.join(CommonDef.getFileRoot(i_input), free_path)

    try:
        if CommonDef.getFileExt(i_input).lower() != ".gif":
            with Image.open(i_input) as im:
                resized_img = resizeImg(im, (int(width), int(height)))
                resized_img.save(fp=free_output)

        else:
            resizeGif(i_input, free_output, imageCustom._preview_size(i_img))

        log_msg_f = f"이미지 리사이징 완료({width}, {int(height)})"

    except Exception as error_msg:
        log_msg_f = f"이미지 리사이징 실패 {str(error_msg)}"
        return False

    return True


def imgResizerCommon(i_input):
    if isPath(i_input) == True:
        if i_arr[-2].isdigit() and i_arr[-1].isdigit():
            if freeResizer(i_input, int(i_arr[-2]), int(i_arr[-1])):
                CommonDef.makeLogTxt(i_input, log_msg_f, log_dir, True)
            else:
                CommonDef.makeLogTxt(i_input, log_msg_f, log_dir, False)

        elif i_arr[-1].isdigit():
            if freeResizer(i_input, int(i_arr[-1]), None):
                CommonDef.makeLogTxt(i_input, log_msg_f, log_dir, True)
            else:
                CommonDef.makeLogTxt(i_input, log_msg_f, log_dir, False)

        else:
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


if CommonDef.isDigit(i_arr[-2]) and CommonDef.isDigit(i_arr[-1]):
    for img in i_arr[0:-2]:
        imgResizerCommon(img.replace("\\", "/").strip('"'))

elif CommonDef.isDigit(i_arr[-1]):
    for img in i_arr[0:-1]:
        imgResizerCommon(img.replace("\\", "/").strip('"'))

else:
    for img in i_arr:
        imgResizerCommon(img.replace("\\", "/").strip('"'))
