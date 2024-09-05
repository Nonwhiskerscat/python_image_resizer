from imgpy import Img
import os
import configparser
from common import *
import sys
from PIL import Image

imageRes = ProgramRes()

i_path = sys.argv[1].replace("\\", "/").strip('"')  # img path
x_start = sys.argv[-5]  # X 시작 좌표
y_start = sys.argv[-4]  # Y 시작 좌표
x_end = sys.argv[-3]  # X 끝 좌표
y_end = sys.argv[-2]  # Y 끝 좌표
suffix = sys.argv[-1] # 파일 이름


# ConfigParser 객체 생성
config = configparser.ConfigParser()

possible_img_crop = []

config.read(FileRoot.in_root, encoding="UTF-8")
possible_img_crop = list(config["Image_TypeI"].values())

# 로그 파일 생성
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)


def cropImg(i_input, x1, y1, x2, y2):
    global log_msg, crop_output
    crop_path = f"{suffix}{CommonDef.getFileExt(i_input)}"
    crop_output = os.path.join(CommonDef.getFileRoot(i_input), crop_path)

    # 해당 패스가 유효하지 않을 때
    if not os.path.isfile(i_input):
        log_msg = "유효하지 않은 패스"
        return False

    # 이미지가 해당 기능을 제공하지 못하는 확장자일 때
    if CommonDef.getFileExt(i_input).lower() not in possible_img_crop:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(i_input) + ")"
        return False

    # 이미지 좌표의 값이 숫자 형식이 아닐 때
    if not all(CommonDef.isDigit(val) for val in (x1, y1, x2, y2)):
        log_msg = f"Crop 파라미터 형식 오류({x1},{y1}_{x2},{y2})"
        return False

    # 좌표 값 모두 int형으로 변환
    x1, x2, y1, y2 = map(int, (x1, x2, y1, y2))

    # 시작 좌표 값이 끝 좌표값을 오버할 때
    if x2 < x1 or y2 < y1:
        log_msg = f"Crop 파라미터 배치 오류({x1},{y1}_{x2},{y2})"
        return False

    # 이미지 사이즈 구하기

    i_obj = Image.open(i_input)
    i_width, i_height = i_obj.size
    imageRes.sizeX, imageRes.sizeY = i_obj.size

    # 좌표 값이 0보다 작거나 이미지의 높이와 너비 값을 오버할 때, 그리고 각 좌표 간의 차이가 이미지의 너비 및 높이의 값을 오버할 때
    def check_range(val, i_limit):
        return max(0, min(val, i_limit))

    x1 = check_range(x1, i_width)
    x2 = check_range(x2, i_width)

    y1 = check_range(y1, i_height)
    y2 = check_range(y2, i_height)

    if x2 - x1 > i_width:
        x1, x2 = 0, i_width

    if y2 - y1 > i_height:
        y1, y2 = 0, i_height

    try:
        with Img(fp=i_input) as im:
            im.crop(box=(x1, y1, x2, y2))
            im.save(fp=crop_output)

        with Img(fp=crop_output) as im:
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi

        cropped_file_size = os.path.getsize(crop_output)
        imageRes.fileSize = cropped_file_size

        log_msg = f"Cropping 완료({x1},{y1}_{x2},{y2})"
        return True
    except Exception as error_msg:
        print(i_input)
        log_msg = "이미지 Cropping 실패 " + str(error_msg)
        return False


if cropImg(i_path, x_start, y_start, x_end, y_end) == True:
    imageRes.res = CommonDef.makeLogTxt(i_path, log_msg, log_dir, True)

else:
    imageRes.res = CommonDef.makeLogTxt(i_path, log_msg, log_dir, False)

if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")