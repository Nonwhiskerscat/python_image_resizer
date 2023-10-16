# 일부 라이브러리 불러오기
import os
import configparser
import sys
from PIL import Image, ImageSequence

# 공용 파일 불러오기
from common import *

# 이미지 파일
i_input = sys.argv[1].replace("\\", "/").strip('"')

# 입력된 프레임 수
c_frames = sys.argv[-1]

# 원본 이미지의 전체 프레임 수
i_frames = CommonDef.aniFrames(i_input)

# c_frame 값(입력 받은 int값)에 따른 프레임 수 조절
## *을 입력받을 경우, 이미지의 전체 프레임 수를 따르고
if c_frames == "*":
    c_frames = i_frames

## 입력받은 값이 자연수가 아닌 경우 0을 부여받는다.
elif not c_frames.isdigit():
    c_frames = 0

# 파일 위치
i_root = os.path.dirname(i_input)

# ConfigParser 객체 생성 및 확인
config = configparser.ConfigParser()

# 해당 프로그램을 사용할 수 있는 확장자 배열 선언
possible_gif_decom = []

# image_costom.ini 파일 호출
config.read(FileRoot.in_root, encoding="UTF-8")

# possible_gif_decom에 확장자 append
for key in config["Ani_Image"].keys():
    possible_gif_decom.append(key)

# 로그 파일 주소 가져오기
log_dir = config["LogFile_Route"]["root"]
# 로그 파일 여부 확인 및 생성
CommonDef.createDir(log_dir)


# 애니메이션 이미지에서 추출할 프레임 위치를 저장하는 함수
def setFrameNum(cfrm, ifrm):
    frm_arr = []  # 배열 선언
    if cfrm == 0:  # cfrm이 0일 때(입력 받은 프레임 수가 *이 아닐 때, 자연수 형식이 아닐 때)
        return False  # False 리턴(배열에 아무 것도 저장 X)

    elif cfrm == 1:  # cfrm이 1일 때(입력 받은 프레임 수가 1일 때)
        frm_arr = [0]  # 배열에 첫 번째 프레임 수 저장

    else:  # 그 외(입력 받은 프레임 수가 자연수거나 *일 때)
        sumfrm = 0  # 저장 할 프레임 수(초기값 0)
        f_intv = (ifrm - 1) / (cfrm - 1)  # 등차수열에 따른 프레임 간격 변수
        while sumfrm < ifrm:  # sumfrm의 수가 전체 프레임 수를 넘어갈 때까지 반복
            frm_arr.append(round(sumfrm))  # 저장된 프레임 수의 반올림한 값을 프레임 배열에 저장
            sumfrm += f_intv  # 프레임 값 업데이트

    return frm_arr  # 프레임 배열 리턴


# 메인 함수
def aniDecompose(img, frmarr, cfrm):
    global log_msg

    # 해당 패스가 유효하지 않을 때
    if not os.path.isfile(img):
        log_msg = "유효하지 않은 패스"
        return False

    # 이미지가 해당 기능을 제공하지 못하는 확장자일 때
    if CommonDef.getFileExt(img).lower() not in possible_gif_decom:
        log_msg = f"지원하지 않는 파일 확장자({CommonDef.getFileExt(img)})"
        return False

    # 프레임 수 체크
    if cfrm == 0:
        log_msg = f"프레임 수치 오류"
        return False

    # 프레임 수 int 형식화(기존에는 같은 숫자여도 str 형식으로 저장되어 있음)
    cfrm = int(cfrm)

    # 입력 받은 프레임 수가 원본 이미지의 프레임 수를 초과할 경우 오류 발생
    if cfrm > i_frames:
        log_msg = f"원본 프레임 수({i_frames}) 초과"
        return False

    try:
        # 이미지와 같은 경로에 이미지 이름으로 된 폴더 생성
        CommonDef.createDir(FileRoot.SubDir(i_root, CommonDef.getFileName(i_input)))
        # 이미지 폴더 내 모든 파일 삭제(동일한 이미지에 해당 프로그램을 재구동 할 시, 이미지 오버랩 현상 발생을 해결)
        DeleteCommon.All(f"{i_root}/{CommonDef.getFileName(i_input)}")

        # 파일 이름 구분자인 frm_order 선언
        frm_order = 0

        with Image.open(img) as im:
            # 프레임 분리 작업
            for idx, frame in enumerate(ImageSequence.Iterator(im)):
                # idx 값이 프레임 배열의 값에 포함될 경우
                if idx in frmarr:
                    # 해당 프레임 이미지 저장(파일 형식_png)
                    i_output = f"{i_root}/{CommonDef.getFileName(i_input)}/frames_{frm_order}.png"
                    frame.save(i_output, format="PNG")
                    frm_order += 1

            log_msg = f"이미지 파싱 완료(프레임 수: {c_frames})"
    except Exception as error_msg:
        # 이미지 파싱 도중 문제 발생 시 오류 발생
        log_msg = f"이미지 파싱 실패{str(error_msg)}"
        return False

    return True


# 타겟 프레임 변수 선언(프레임 배열 값 리턴)
target_frames = setFrameNum(int(c_frames), i_frames)

# 로그 파일 업데이트

# aniDecompose 값 실행
## 해당 메서드 값이 True일 경우 clear.txt에 로그 기록
if aniDecompose(i_input, target_frames, c_frames):
    CommonDef.makeLogTxt(i_input.replace("\\", "/").strip('"'), log_msg, log_dir, True)

## 해당 메서드 값이 False일 경우 failed.txt에 로그 기록
else:
    CommonDef.makeLogTxt(i_input.replace("\\", "/").strip('"'), log_msg, log_dir, False)
