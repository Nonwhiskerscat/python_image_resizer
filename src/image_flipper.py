import os
import configparser
import sys
from imgpy import Img
from PIL import Image, ImageSequence
from common import *

imageRes = ProgramRes()
Image.MAX_IMAGE_PIXELS = None 

# 이미지 파일
i_input = sys.argv[1].replace("\\", "/").strip('"')

# 이미지 플립 idx
flip_idx = sys.argv[-2]  # 이미지 플립 idx
suffix = sys.argv[-1]

# ini 파일 읽어오기
config = configparser.ConfigParser()
config.read(FileRoot.in_root, encoding="UTF-8")

possible_img_flip = list(config["Image_TypeI"].values())
rgba_convert_ext = list(config["RGBA_Exception"].values())

# 로그 파일 생성 및 여부
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)


# 정적 이미지 플립 메서드
def flipImg(input, f_idx):
    # flip_idx가 1인 경우, 좌우대칭

    if f_idx == "1":
        f_img = input.transpose(Image.FLIP_LEFT_RIGHT)

    # flip_idx가 2인 경우, 상하대칭
    elif f_idx == "2":
        f_img = input.transpose(Image.FLIP_TOP_BOTTOM)

    # flip_idx가 3인 경우, 좌우 + 상하 대칭
    elif f_idx == "3":
        t_f_img = input.transpose(Image.FLIP_LEFT_RIGHT)
        f_img = t_f_img.transpose(Image.FLIP_TOP_BOTTOM)

    # 그 외, 좌우 대칭
    else:
        f_img = input.transpose(Image.FLIP_LEFT_RIGHT)

    # 뒤집힌 이미지 저장
    return f_img


# 동적 이미지 플립 매서드
def flipGif(input, output, f_idx):
    with Image.open(input) as im:
        idpi = CommonDef.getDPI(im)
        imageRes.iDpi = idpi
        frames = []

        # 프레임 추출 및 각 프레임 플립
        for frame in range(im.n_frames):
            im.seek(frame)
            flipped_frame = flipImg(im.copy(), f_idx)
            frames.append(flipped_frame)

        # 플립된 프레임을 새로운 GIF 파일로 저장
        frames[0].save(output, save_all=True, append_images=frames[1:], loop=0)
        file_size = os.path.getsize(output)
        imageRes.fileSize = file_size

def flipCommon(img, f_idx):
    global log_msg, i_output

    # 결과 이미지 패스 > 원본과 같은 폴더에서 파일 이름
    new_path = f"{suffix}{CommonDef.getFileExt(img)}"
    i_output = os.path.join(CommonDef.getFileRoot(img), new_path)


    # 입력된 패스가 유효하지 않을 때
    if not os.path.isfile(img):
        log_msg = "유효하지 않은 패스"
        return False

    # 해당 기능을 지원할 수 있는 확장자가 아닐 때
    if CommonDef.getFileExt(img).lower() not in possible_img_flip:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(img) + ")"
        return False

    try:
        # 이미지 형식이 Gif가 아닐 때
        if CommonDef.getFileExt(img).lower() != ".gif":
            with Image.open(img) as im:
                if im.mode == 'RGBA' and CommonDef.getFileExt(img).lower() in (item for item in rgba_convert_ext):
                    im = im.convert('RGB')
                flipped_img = flipImg(im, f_idx)
                flipped_img.save(fp=i_output)

        # 이미지 형식이 Gif일 때
        else:
            flipGif(img, i_output, f_idx)
            # t = 1

        with Image.open(i_output) as im:
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi

        file_size = os.path.getsize(i_output)
        imageRes.fileSize = file_size

        log_msg = "이미지 플립 완료"

    except Exception as error_msg:
        log_msg = f"이미지 플립 실패 {str(error_msg)}"
        return False

    return True


# 로그 파일 업데이트
if flipCommon(i_input, flip_idx) == True:
    imageRes.res = CommonDef.makeLogTxt(i_output.replace("\\", "/").strip('"'), log_msg, log_dir, True)
else:
    imageRes.res = CommonDef.makeLogTxt(
        i_output.replace("\\", "/").strip('"'), log_msg, log_dir, False
    )

if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")