from PIL import Image, ImageSequence
import math
from common import *
import configparser
import sys

imageRes = ProgramRes()

# 자동화
possible_img_idx = []
possible_ani_watermark = []

# ConfigParser 객체C:\Users\김서용\Desktop\gif_water 4 생성
config = configparser.ConfigParser()
i_path = FileRoot.RootDir(sys.argv[1])
i_root = os.path.dirname(i_path)

w_idx = str(sys.argv[-2])
suffix = str(sys.argv[-1])

# image 워터마크 파일 생성

config.read(FileRoot.in_root, encoding="UTF-8")
possible_ani_watermark = list(config["Ani_Image"].values())
possible_img_idx = list(config["Water_Idx"].values())

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


def watermarkForGif(i_input, w_image, w_opacity):
    global log_msg
    global i_output

    original_gif = Image.open(i_input)


    new_path = f"{suffix}{CommonDef.getFileExt(i_input)}"
    i_output = os.path.join(CommonDef.getFileRoot(i_input), new_path)

    if not os.path.isfile(i_input):
        log_msg = "유효하지 않은 패스"
        return False

    if CommonDef.getFileExt(i_input).lower() not in possible_ani_watermark:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(i_input) + ")"
        return False


    frames = []
    for frame in ImageSequence.Iterator(original_gif):
        frame = frame.convert("RGBA")
        watermark = Image.open(w_image).convert("RGBA")

        w_resized = watermark.resize(
            (wWidth(frame.width), wHeight(watermark, wWidth(frame.width))),
            resample=Image.NEAREST  # 보간 알고리즘 설정
        )

        alpha = w_resized.getchannel("A")
        alpha = alpha.point(lambda p: int(p * w_opacity))
        w_resized.putalpha(alpha)

        position_x = frame.width - math.ceil(1.1 * w_resized.width)
        position_y = (
            frame.height - w_resized.height - math.ceil(0.1 * w_resized.width)
        )

        transparent = Image.new(
            "RGBA", (frame.width, frame.height), (0, 0, 0, 0)
        )

        transparent.paste(frame, (0, 0))
        transparent.paste(w_resized, (position_x, position_y), w_resized)

        frames.append(transparent)

    # 새로운 GIF 이미지 생성
    try:
        frames[0].save(fp=i_output, save_all=True, append_images=frames[1:], loop=0, optimize=True, duration=original_gif.info['duration'], disposal=2, colors=256)
        log_msg = "워터마크 GIF 이미지 제작 완료"
        file_size = os.path.getsize(i_output)
        imageRes.fileSize = file_size
        with Image.open(i_output) as im:
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi
        return True
    except Exception as error_msg:
        log_msg = "에러 발생: " + str(error_msg)
        return False

w_opacity = float(config["Water_Opacity"][w_idx])

if watermarkForGif(i_path, w_ent_path, w_opacity) == True:
    imageRes.res = CommonDef.makeLogTxt(i_output, log_msg, log_dir, True)
else:
    imageRes.res = CommonDef.makeLogTxt(i_output, log_msg, log_dir, False)

if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")