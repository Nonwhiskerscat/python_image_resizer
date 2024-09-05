import os
import configparser
import sys
from PIL import Image, ImageSequence
from common import *

imageRes = ProgramRes()


# 이미지 파일
i_input = sys.argv[1].replace("\\", "/").strip('"')

# 이미지 회전 각도
i_rotate = sys.argv[-2]  # 이미지 회전 각도
suffix = sys.argv[-1]

# ini 파일 읽어오기
config = configparser.ConfigParser()

possible_img_rotate = []

config.read(FileRoot.in_root, encoding="UTF-8")
possible_img_rotate = list(config["Image_TypeI"].values())
rgba_convert_ext = list(config["RGBA_Exception"].values())

# 로그 파일 생성 및 여부
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)


# 정적 이미지 로테이트 메서드
def rotateImg(img, angle):
    img_rotated = img.rotate(-1*float(angle), expand=True)
    return img_rotated


# 동적 이미지 로테이트 메서드
def rotateGif(input, output, angle):
    with Image.open(input) as im:
        frames = []

        # 프레임 추출 및 각 프레임 회전
        for frame in range(im.n_frames):
            im.seek(frame)
            rotated_frame = rotateImg(im.copy(), angle)
            frames.append(rotated_frame)

        # 회전된 프레임을 새로운 GIF 파일로 저장
        frames[0].save(output, save_all=True, append_images=frames[1:], loop=0)
        file_size = os.path.getsize(output)
        imageRes.fileSize = file_size


# 이미지 로테이트 종합 함수
def rotateCommon(img, rot):
    global log_msg, i_output

    # 결과 이미지 패스 > 원본과 같은 폴더에서 파일 이름_rot로테이트 앵글
    new_path = f"{suffix}{CommonDef.getFileExt(img)}"
    i_output = os.path.join(CommonDef.getFileRoot(img), new_path)

    # 입력된 패스가 유효하지 않을 때
    if not os.path.isfile(img):
        log_msg = "유효하지 않은 패스"
        return False

    # 해당 기능을 지원할 수 있는 확장자가 아닐 때
    if CommonDef.getFileExt(img).lower() not in possible_img_rotate:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(img) + ")"
        return False

    # 회전 값이 int형 혹은 float형이 아닐 때
    if not CommonDef.isDigit(rot):
        log_msg = f"회전값 수치 오류({rot})"
        return False

    try:
        # 이미지 형식이 Gif가 아닐 때
        if CommonDef.getFileExt(img).lower() != ".gif":
            with Image.open(img) as im:
                if im.mode == 'RGBA' and CommonDef.getFileExt(img).lower() in (item for item in rgba_convert_ext):
                    im = im.convert('RGB')
                rotated_image = rotateImg(im, rot)
                rotated_image.save(fp=i_output)
        # 이미지 형식이 Gif일 때
        else:
            rotateGif(img, i_output, rot)

        with Image.open(i_output) as im:
            imageRes.sizeX = im.width
            imageRes.sizeY = im.height
            idpi = CommonDef.getDPI(im)
            imageRes.iDpi = idpi

        file_size = os.path.getsize(i_output)
        imageRes.fileSize = file_size

        log_msg = "이미지 로테이트 완료"

    # 이미지 로테이트 실패 시, 에러 메시지 발생
    except Exception as error_msg:
        log_msg = f"이미지 로테이트 실패 {str(error_msg)}"
        return False

    return True


# 로그 파일 업데이트
if rotateCommon(i_input, i_rotate) == True:
    imageRes.res = CommonDef.makeLogTxt(i_output.replace("\\", "/").strip('"'), log_msg, log_dir, True)
else:
    imageRes.res = CommonDef.makeLogTxt(
        i_output.replace("\\", "/").strip('"'), log_msg, log_dir, False
    )

if(imageRes.res[0] == True):
    print(f"SUCCESS|{imageRes.sizeX}|{imageRes.sizeY}|{int(imageRes.iDpi)}|{int(imageRes.fileSize)}")
else:
    print(f"FAILED|{imageRes.res[1]}")