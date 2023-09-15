from PIL import Image, ImageSequence
import math
from common import *
import configparser
import sys

# 자동화
possible_img_idx = []
possible_img_watermark = []

# ConfigParser 객체C:\Users\김서용\Desktop\gif_water 4 생성
config = configparser.ConfigParser()
i_path = FileRoot.RootDir(sys.argv[1])
i_root = os.path.dirname(i_path)
w_idx = str(sys.argv[-1])

# image 워터마크 파일 생성

config.read(FileRoot.in_root, encoding="UTF-8")
for key in config["Water_Type"].keys():
    possible_img_watermark.append(key)
for key in config["Water_Idx"].keys():
    possible_img_idx.append(key)
# 사용 예시
# watermarkForImg("input.jpg", "output.jpg", "watermark.png", 196)

# idx 값에 따른 워터마크 이미지 경로
if w_idx not in possible_img_idx:
    w_idx = "1"

w_path = config["Water_Route"][w_idx]

# 로그 파일 생성
log_dir = config["LogFile_Route"]["root"]
CommonDef.createDir(log_dir)


# 워터 마크 너비
def wWidth(width):
    return math.ceil(width * float(config["Water_Ratio"][w_idx]))


# 워터 마크 높이
def wHeight(wmark, wwidth):
    w_ratio = wmark.width / wmark.height
    return math.ceil(wwidth / w_ratio)


# 워터 마크 이미지 생성 메서드
def watermarkForImg(i_input, w_image, w_opacity):
    global log_msg
    global i_output

    i_output = i_root + "/watermark/" + os.path.basename(i_input)

    if not os.path.isfile(i_input):
        log_msg = "이미지 파일 누락"
        return False

    if CommonDef.getFileExt(i_input).lower() not in possible_img_watermark:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(i_input) + ")"
        return False

    CommonDef.createDir(FileRoot.SubDir(i_root, "watermark"))
    original_image = Image.open(i_input).convert("RGBA")
    watermark = Image.open(w_image).convert("RGBA")

    # 워터마크 크기 조정
    w_resized = watermark.resize(
        (wWidth(original_image.width), wHeight(watermark, wWidth(original_image.width)))
    )

    # 알파 채널 생성
    alpha = w_resized.getchannel("A")
    alpha = alpha.point(lambda p: int(p * w_opacity))
    w_resized.putalpha(alpha)

    position_x = original_image.width - math.ceil(1.1 * w_resized.width)
    position_y = (
        original_image.height - w_resized.height - math.ceil(0.1 * w_resized.width)
    )

    transparent = Image.new(
        "RGBA", (original_image.width, original_image.height), (0, 0, 0, 0)
    )

    # 가상 이미지에 원본 사진 레이어 추가
    transparent.paste(original_image, (0, 0))

    # 가상 이미지에 워터 마크 레이어 추가
    transparent.paste(w_resized, (position_x, position_y), w_resized)

    # 가상 이미지 저장
    try:
        transparent.save(i_output, "PNG")
        log_msg = "워터마크 이미지 제작 완료"
        return True
    except Exception as error_msg:
        log_msg = "에러 발생" + str(error_msg)
        return False


w_opacity = float(config["Water_Opacity"][w_idx])

# watermarkForImg(i_path, w_path, w_opacity)


if watermarkForImg(i_path, w_path, w_opacity) == True:
    CommonDef.makeLogTxt(i_output, log_msg, log_dir, True)
else:
    CommonDef.makeLogTxt(i_output, log_msg, log_dir, False)
