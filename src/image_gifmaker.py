from PIL import Image
import sys
import os
from common import *
import configparser

imageRes = ProgramRes()

# sys.argv[1~-2] => 이미지 크기
# sys.argv[-1] => 각 이미지 프레임

# ConfigParser 객체 생성
config = configparser.ConfigParser()

config.read(FileRoot.in_root, encoding="UTF-8")

possible_img_gifmaker = list(config["Image_TypeI"].values())
rgba_convert_ext = list(config["RGBA_Exception"].values())

# 로그 파일 생성
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)

img_dura = sys.argv[-2]
suffix = sys.argv[-1]

img_dura = int(img_dura)

# 이미지 패스 배열
imgs_arr = sys.argv[1:-2]

# 이미지 프레임
from PIL import Image, ImageOps

def center_image_in_frame(image, frame_width, frame_height):
    image_width, image_height = image.size
    offset_x = (frame_width - image_width) // 2
    offset_y = (frame_height - image_height) // 2

    # 가상 프레임을 생성하고 이미지를 중앙에 삽입
    frame = Image.new('RGBA', (frame_width, frame_height), (255, 255, 255, 0))
    frame.paste(image, (offset_x, offset_y))

    return frame

def gifMaker(i_inputs):
    global log_msg, i_output
    new_path = suffix + ".gif"
    i_output = os.path.join(CommonDef.getFileRoot(i_inputs[0]), new_path)

    for idx, val in enumerate(i_inputs):
        if not os.path.isfile(val):
            log_msg = f"유효하지 않은 패스 포함({val})"
            return False

        if CommonDef.getFileExt(val).lower() not in possible_img_gifmaker:
            log_msg = f"지원하지 않는 파일 확장자 포함({CommonDef.getFileExt(val).lower()})"
            return False

    resized_images = [Image.open(path) for path in i_inputs]

    for idx, img in enumerate(resized_images):
        # 이미지를 중앙에 배치한 후, 프레임 크기에 맞게 리사이즈
        with Image.open(val) as im:
            if idx == 0:
                maxWidth = im.width
                maxHeight = im.height
            else:
                if im.width>maxWidth:
                    maxWidth = im.width
                if im.height>maxHeight:
                    maxHeight = im.height
        
        resized_images[idx] = center_image_in_frame(img, maxWidth, maxHeight).resize((maxWidth, maxHeight), Image.LANCZOS)

    try:
        resized_images[0].save(
            fp=i_output,
            save_all=True,
            append_images=resized_images[1:],
            loop=0,
            duration=img_dura,
            colors=256,
            disposal=2
        )

        file_size = os.path.getsize(i_output)
        imageRes.fileSize = file_size

        with Image.open(i_output) as im:
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi

        log_msg = "GIF 이미지 생성 완료"

    except Exception as error_msg:
        log_msg = "GIF 이미지 생성 실패 " + str(error_msg)
        return False

    # 작업이 끝났으면 이미지 객체를 닫음
    for img in resized_images:
        img.close()

    return True


if gifMaker(imgs_arr) == True:
    imageRes.res = CommonDef.makeLogTxt(i_output.replace("\\", "/").strip('"'), log_msg, log_dir, True)
else:
    imageRes.res = CommonDef.makeLogTxt(
        i_output.replace("\\", "/").strip('"'), log_msg, log_dir, False
    )

if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")