from PIL import Image, ImageSequence
import math
from common import *
import configparser
import sys

imageRes = ProgramRes()
Image.MAX_IMAGE_PIXELS = None 
# 자동화
possible_img_idx = []
possible_img_watermark = []

# ConfigParser 객체C:\Users\김서용\Desktop\gif_water 4 생성
config = configparser.ConfigParser()
i_path = FileRoot.RootDir(sys.argv[1])
i_root = os.path.dirname(i_path)

w_idx = str(sys.argv[-2])
suffix = str(sys.argv[-1])

# image 워터마크 파일 생성

config.read(FileRoot.in_root, encoding="UTF-8")

possible_img_watermark = list(config["Image_TypeI"].values())
possible_img_idx = list(config["Water_Idx"].values())
rgba_convert_ext = list(config["RGBA_Exception"].values())

# 사용 예시
# watermarkForImg("input.jpg", "output.jpg", "watermark.png", 196)

# idx 값에 따른 워터마크 이미지 경로
if w_idx not in possible_img_idx:
    w_idx = "1"

w_path = config["Water_Image"][w_idx]

w_ent_path = os.path.join(FileRoot.water_root, w_path)

# 로그 파일 생성
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)


# 워터 마크 너비
def wWidth(width):
    return math.ceil(width * float(config["Water_Ratio"][w_idx]))


# 워터 마크 높이
def wHeight(wmark, wwidth):
    w_ratio = wmark.width / wmark.height
    return math.ceil(wwidth / w_ratio)


def watermarkForImg(i_input, w_image, w_opacity):
    global log_msg
    global i_output

    new_path = f"{suffix}{CommonDef.getFileExt(i_input)}"
    i_output = os.path.join(CommonDef.getFileRoot(i_input), new_path)


    if not os.path.isfile(i_input):
        log_msg = "유효하지 않은 패스"
        return False

    if CommonDef.getFileExt(i_input).lower() not in possible_img_watermark:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(i_input) + ")"
        return False

    original_image = Image.open(i_input).convert("RGB")
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
        try:
            transparent.save(fp=i_output)

        except:
            transparent = transparent.convert("RGB")
            transparent.save(fp=i_output)

        log_msg = "워터마크 이미지 제작 완료"
        file_size = os.path.getsize(i_output)

        with Image.open(i_output) as im:
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height

        imageRes.fileSize = file_size
        return True
    except Exception as error_msg:
        log_msg = "에러 발생" + str(error_msg)
        return False

w_opacity = float(config["Water_Opacity"][w_idx])

if watermarkForImg(i_path, w_ent_path, w_opacity) == True:
    imageRes.res = CommonDef.makeLogTxt(i_output, log_msg, log_dir, True)
else:
    imageRes.res = CommonDef.makeLogTxt(i_output, log_msg, log_dir, False)


if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")