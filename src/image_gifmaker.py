from PIL import Image
import sys
import os
from common import *
import configparser

# sys.argv[1~-2] => 이미지 크기
# sys.argv[-1] => 각 이미지 프레임

# ConfigParser 객체 생성
config = configparser.ConfigParser()

possible_img_gifmaker = []

config.read(FileRoot.in_root, encoding="UTF-8")
for key in config["Image_TypeI"].keys():
    possible_img_gifmaker.append(key)

# 로그 파일 생성
log_dir = config["LogFile_Route"]["root"]
CommonDef.createDir(log_dir)


# 이미지 Duration
img_dura = sys.argv[-1]

# 이미지 Duration Default 값
if not img_dura.isdigit():
    img_dura = 500
else:
    img_dura = int(img_dura)

# 이미지 패스 배열
imgs_arr = sys.argv
del imgs_arr[0], imgs_arr[-1]

# 이미지 프레임

######################## 크기 기준(비율 무시) ########################

# # 첫 번째 이미지를 기준으로 크기를 가져옴
# base_image = Image.open(image_paths[0])
# base_width, base_height = base_image.size

# # 이미지들을 열어 리스트에 저장하면서 크기를 조정
# resized_images = [Image.open(path).resize((base_width, base_height)) for path in image_paths]

######################## 너비 기준(비주얼 무시) ########################


def gifMaker(i_inputs):
    global log_msg, i_output
    new_path = CommonDef.getFileName(i_inputs[0]) + "_gif.gif"
    i_output = os.path.join(CommonDef.getFileRoot(i_inputs[0]), new_path)

    for val in i_inputs:
        if not os.path.isfile(val):
            log_msg = f"유효하지 않은 패스 포함({val})"
            return False

        if CommonDef.getFileExt(val).lower() not in possible_img_gifmaker:
            log_msg = f"지원하지 않는 파일 확장자 포함({CommonDef.getFileExt(val).lower()})"
            return False

    first_img = Image.open(i_inputs[0])
    first_width, _ = first_img.size

    resized_images = [Image.open(path) for path in i_inputs]

    for i, img in enumerate(resized_images):
        width_percent = first_width / float(img.size[0])
        new_height = int((float(img.size[1]) * float(width_percent)))
        resized_images[i] = img.resize((first_width, new_height), Image.LANCZOS)

    try:
        resized_images[0].save(
            i_output,
            save_all=True,
            append_images=resized_images[1:],
            loop=0,
            duration=img_dura,
        )
        log_msg = "GIF 이미지 생성 완료"

    except Exception as error_msg:
        log_msg = "GIF 이미지 생성 실패 " + str(error_msg)
        return False

    # 작업이 끝났으면 이미지 객체를 닫음
    for img in resized_images:
        img.close()

    return True


if gifMaker(imgs_arr) == True:
    CommonDef.makeLogTxt(i_output.replace("\\", "/").strip('"'), log_msg, log_dir, True)
else:
    CommonDef.makeLogTxt(
        i_output.replace("\\", "/").strip('"'), log_msg, log_dir, False
    )
