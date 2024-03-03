import os
import configparser
import sys
from PIL import Image, ImageSequence
from common import *

imageRes = ProgramRes()


# 이미지 파일
i_input = sys.argv[1].replace("\\", "/").strip('"')

suffix = sys.argv[-1]

# ini 파일 읽어오기
config = configparser.ConfigParser()

possible_img_grayscale = []

config.read(FileRoot.in_root, encoding="UTF-8")
for key in config["Image_TypeI"].keys():
    possible_img_grayscale.append(key)

# 로그 파일 생성 및 여부
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)


# 정적 이미지 그레이스케일 매서드
def grayScale(img):
    img_gray = img.convert("L")
    return img_gray


# 동적 이미지 그레이스케일 매서드
def rotateGif(input, output):
    with Image.open(input) as im:
        frames = []

        # 프레임 추출 및 각 프레임 흑백화
        for frame in range(im.n_frames):
            im.seek(frame)
            rotated_frame = grayScale(im.copy())
            frames.append(rotated_frame)

        # 회전된 프레임을 새로운 GIF 파일로 저장
        frames[0].save(output, save_all=True, append_images=frames[1:], loop=0)
        file_size = os.path.getsize(output)
        imageRes.fileSize = file_size


# 이미지 그레이스케일 종합 함수
def grayCommon(img):
    global log_msg, i_output

    # 결과 이미지 패스 > 원본과 같은 폴더에서 파일 이름_rot로테이트 앵글
    new_path = f"{suffix}{CommonDef.getFileExt(img)}"
    i_output = os.path.join(CommonDef.getFileRoot(img), new_path)

    # 입력된 패스가 유효하지 않을 때
    if not os.path.isfile(img):
        log_msg = "유효하지 않은 패스"
        return False

    # 해당 기능을 지원할 수 있는 확장자가 아닐 때
    if CommonDef.getFileExt(img).lower() not in possible_img_grayscale:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(img) + ")"
        return False

    try:
        # 이미지 형식이 Gif가 아닐 때
        if CommonDef.getFileExt(img).lower() != ".gif":
            with Image.open(img) as im:
                grayed_image = grayScale(im)
                grayed_image.save(fp=i_output)
        # 이미지 형식이 Gif일 때
        else:
            rotateGif(img, i_output)

        with Image.open(i_output) as im:
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi

        file_size = os.path.getsize(i_output)
        imageRes.fileSize = file_size

        log_msg = "이미지 흑백화 완료"

    # 이미지 로테이트 실패 시, 에러 메시지 발생
    except Exception as error_msg:
        log_msg = f"이미지 흑백화 실패 {str(error_msg)}"
        return False

    return True


# 로그 파일 업데이트
if grayCommon(i_input) == True:
    imageRes.res = CommonDef.makeLogTxt(i_output.replace("\\", "/").strip('"'), log_msg, log_dir, True)
else:
    imageRes.res = CommonDef.makeLogTxt(
        i_output.replace("\\", "/").strip('"'), log_msg, log_dir, False
    )

if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")