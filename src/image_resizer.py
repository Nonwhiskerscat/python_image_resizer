import os
import math
import configparser
from PIL import Image, ImageSequence
import sys
from common import *

imageRes = ProgramRes()

# sys.argv[0] = file_name
# sys.argv[1~-1] = image_files

# 입력된 img 경로를 저장한 배열
i_arr = sys.argv[1:-3]

isizex = sys.argv[-3]
isizey = sys.argv[-2]
suffix = sys.argv[-1]

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
def resizeImg(img, size, orgpath):
    if img.mode == 'RGBA' and CommonDef.getFileExt(orgpath).lower() == '.jpeg':
        img = img.convert('RGB')
    img_resized = img.resize(size)
    return img_resized


# 동적 이미지 리사이즈 메서드
def resizeGif(input, output, size):
    with Image.open(input) as im:
        frames = []

        # 프레임 추출 및 각 프레임 회전
        for frame in range(im.n_frames):
            im.seek(frame)
            resized_frame = resizeImg(im.copy(), size, input)
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
        log_msg_i = f"유효하지 않은 패스 {i_input}"
        return False

    # 리사이징이 지원되지 않는 확장자인 경우
    elif CommonDef.getFileExt(i_input).lower() not in possible_img_resize:
        log_msg_i = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(i_input) + ")"
        return False

    else:
        return True


def freeResizer(i_input, width, height):
    log_msg_f = ""  # log_msg_f 초기화
    i_img = Image.open(i_input)
    if height == 0:
        height = (width / i_img.width) * i_img.height

    if width == 0:
        width = (height / i_img.height) * i_img.width

    free_path = f"{suffix}{CommonDef.getFileExt(i_input)}"
    free_output = os.path.join(CommonDef.getFileRoot(i_input), free_path)

    try:
        if CommonDef.getFileExt(i_input).lower() != ".gif":
            with Image.open(i_input) as im:
                resized_img = resizeImg(im, (int(width), int(height)), i_input)
                resized_img.save(fp=free_output)

        else:
            resizeGif(i_input, free_output, (int(width), int(height)))

        file_size = os.path.getsize(free_output)
        imageRes.fileSize = file_size
        with Image.open(free_output) as im:
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
        
        log_msg_f = f"이미지 리사이징 완료({width}, {int(height)})"

    except Exception as error_msg:
        log_msg_f = f"이미지 리사이징 실패 {str(error_msg)}"
        return False

    return True

def imgResizerCommon(i_input):
    log_msg_f = ""  # log_msg_f 초기화
    if isPath(i_input) == True:
        try:
            if freeResizer(i_input, int(isizex), int(isizey)):
                imageRes.res = CommonDef.makeLogTxt(i_input, log_msg_f, log_dir, True)
            else:
                imageRes.res = CommonDef.makeLogTxt(i_input, log_msg_f, log_dir, False)

        except Exception as e:
            log_msg_f = str(e)
            imageRes.res = CommonDef.makeLogTxt(i_input, log_msg_f, log_dir, False)

    else:
        imageRes.res = CommonDef.makeLogTxt(i_input, log_msg_i, log_dir, False)



try:
    for img in i_arr:
        try:
            imgResizerCommon(img.replace("\\", "/").strip('"'))
        except:
            imgResizerCommon(i_arr[0].replace("\\", "/").strip('"'))
    
except Exception as e:
        print(str)
        imageRes.res = CommonDef.makeLogTxt("", str(e), log_dir, False)


if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")

# os.system("pause")