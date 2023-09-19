from imgpy import Img
import os
import configparser
from common import *
import sys
from PIL import Image, ImageSequence

# 이미지 파일
i_input = sys.argv[1].replace("\\", "/").strip('"')

# 입력된 프레임 수
c_frames = sys.argv[-1]

if not c_frames.isdigit():
    c_frames = 0
# 원본 이미지의 전체 프레임 수
i_frames = CommonDef.aniFrames(i_input)

# 파일 위치
i_root = os.path.dirname(i_input)

# ConfigParser 객체 생성 및 확인
config = configparser.ConfigParser()

possible_gif_decom = []

config.read(FileRoot.in_root, encoding="UTF-8")
for key in config["Ani_Image"].keys():
    possible_gif_decom.append(key)

# 로그 파일 여부 확인
log_dir = config["LogFile_Route"]["root"]
CommonDef.createDir(log_dir)


def setFrameNum(cfrm, ifrm):
    frm_arr = []
    if cfrm == 0:
        return False

    elif cfrm == 1:
        frm_arr = [0]

    else:
        sumfrm = 0
        f_intv = (ifrm - 1) / (cfrm - 1)
        while sumfrm < ifrm:
            frm_arr.append(round(sumfrm))
            sumfrm += f_intv

    return frm_arr


def aniDecompose(img, frmarr, cfrm):
    global log_msg

    # 해당 패스가 유효하지 않을 때
    if not os.path.isfile(img):
        log_msg = "유효하지 않은 패스"
        return False

    # 이미지가 해당 기능을 제공하지 못하는 확장자일 때
    if CommonDef.getFileExt(img).lower() not in possible_gif_decom:
        log_msg = "지원하지 않는 파일 확장자(" + CommonDef.getFileExt(img) + ")"
        return False

    # 프레임 수 체크
    if cfrm == 0:
        log_msg = f"프레임 수치 오류"
        return False

    cfrm = int(cfrm)

    if cfrm > i_frames:
        log_msg = f"원본 프레임 수({i_frames}) 초과"
        return False

    try:
        CommonDef.createDir(FileRoot.SubDir(i_root, CommonDef.getFileName(i_input)))
        DeleteCommon.All(f"{i_root}/{CommonDef.getFileName(i_input)}")
        frm_order = 0
        with Image.open(img) as im:
            for idx, frame in enumerate(ImageSequence.Iterator(im)):
                if idx in frmarr:
                    i_output = f"{i_root}/{CommonDef.getFileName(i_input)}/frames_{frm_order}.png"
                    frame.save(i_output, format="PNG")
                    frm_order += 1

            log_msg = f"이미지 파싱 완료(프레임 수: {c_frames})"
    except Exception as error_msg:
        log_msg = f"이미지 파싱 실패{str(error_msg)}"
        return False

    return True


target_frames = setFrameNum(int(c_frames), i_frames)

# 로그 파일 업데이트

if aniDecompose(i_input, target_frames, c_frames) == True:
    CommonDef.makeLogTxt(i_input.replace("\\", "/").strip('"'), log_msg, log_dir, True)
else:
    CommonDef.makeLogTxt(i_input.replace("\\", "/").strip('"'), log_msg, log_dir, False)
