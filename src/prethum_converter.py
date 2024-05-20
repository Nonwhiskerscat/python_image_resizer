import os
import math
import configparser
from PIL import Image, ImageSequence
import sys
from common import *

imageRes = ProgramRes()

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
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)


# 정적 이미지 리사이즈 메서드
def resizeImg(img, size):
    img_resized = img.resize(size)
    return img_resized


# 동적 이미지 리사이즈 메서드
def resizeGif(input, output, size):
    with Image.open(input) as im:
        frames = []

        # 프레임 추출 및 각 프레임 리사이징
        for frame in range(im.n_frames):
            im.seek(frame)
            resized_frame = resizeImg(im.copy(), size)
            frames.append(resized_frame)

        # 리사이징된 프레임을 새로운 GIF 파일로 저장
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
        log_msg_i = f"유효하지 않은 패스 {i_input}"
        return False

    # 리사이징이 지원되지 않는 확장자인 경우
    elif CommonDef.getFileExt(i_input).lower() not in possible_img_resize:
        log_msg_i = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(i_input) + ")"
        return False

    else:
        return True


def resize_image(image, output_path, custom_width, size_function):
    new_size = size_function(image)
    return resizeImg(image, new_size)

def save_image(image, output_path):
    image.save(fp=output_path)


def process_image(i_input, custom_width, size_function, type):
    global log_msg_t, log_msg_p

    path_suffix = ""

    if type == "thm":
        path_suffix = "t"
    elif type == "pre":
        path_suffix = "p"

    output_path = os.path.join(
        CommonDef.getFileRoot(i_input),
        CommonDef.getFileName(i_input) + path_suffix + CommonDef.getFileExt(i_input),
    )

    try:
        ext = CommonDef.getFileExt(i_input).lower()
        with Image.open(i_input) as im:
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi

            if imageRes.sizeX <= custom_width:

                if ext == ".gif":
                    # 프레임 추출 및 각 프레임 리사이징
                    frames = []
                    
                    for frame in range(im.n_frames):
                        im.seek(frame)
                        ifrm = im.copy()
                        frames.append(ifrm)

                    frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)

                else:
                    save_image(im, output_path)

            else:
                if ext == ".gif":
                    frames = [
                        resize_image(frame, output_path, custom_width, size_function)
                        for frame in ImageSequence.Iterator(im)
                    ]
                    new_im = frames[0].copy()
                    new_im.save(output_path, save_all=True, append_images=frames[1:])
                else:
                    resized_img = resize_image(im, output_path, custom_width, size_function)
                    save_image(resized_img, output_path)

        if type == "thm":
            log_msg_t = "썸네일 변환 완료"
        elif type == "pre" :
            log_msg_p = "프리뷰 변환 완료"
        else:
            return False
    except Exception as error_msg:
        if type == "thm":
            log_msg_t = "썸네일 변환 실패 " + str(error_msg)
        elif type == "pre" :
            log_msg_p = "프리뷰 변환 실패 " + str(error_msg)
        return False

    return True


def thumbnailResizer(i_input):
    return process_image(
        i_input, imageCustom.thumbnail_width, imageCustom._thumbnail_size, "thm"
    )

def previewResizer(i_input):
    return process_image(
        i_input, imageCustom.preview_width, imageCustom._preview_size, "pre"
    )

# 반복 최소화
def changeCommon(cat):
    if thumbnailResizer(cat):
        imageRes.res = CommonDef.makeLogTxt(cat, log_msg_t, log_dir, True)
    else:
        imageRes.res = CommonDef.makeLogTxt(cat, log_msg_t, log_dir, False)

    if previewResizer(cat):
        imageRes.res = CommonDef.makeLogTxt(cat, log_msg_p, log_dir, True)
    else:
        imageRes.res = CommonDef.makeLogTxt(cat, log_msg_p, log_dir, False)


def imgResizerCommon(i_input):
    if isPath(i_input) == True:
        changeCommon(i_input)

    else:
        imageRes.res = CommonDef.makeLogTxt(i_input, log_msg_i, log_dir, False)


try:
    for img in i_arr:
        imgResizerCommon(img.replace("\\", "/").strip('"'))
except:
    imgResizerCommon(i_arr[0].replace("\\", "/").strip('"'))

if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}")
else:
    print(f"FAILED|{imageRes.res[1]}")
