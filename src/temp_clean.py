import os
import configparser
import sys
from datetime import datetime, timedelta
import glob
from common import *

root = sys.argv[1] if len(sys.argv) > 1 else '0'
ext = sys.argv[2] if len(sys.argv) > 2 else '0'
time = sys.argv[3] if len(sys.argv) > 3 else '0'
filter = sys.argv[4] if len(sys.argv) > 4 else '' # 필터는 0을 입력될 수 있으니까 기본값을 공백처리

now = datetime.now()

# 로그 파일 생성
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)

# ini 파일 읽어오기
config = configparser.ConfigParser()
config.read(FileRoot.fn_root, encoding="UTF-8")

# 이미지 확장자 정리
image_extensions = []
image_extensions = [value.upper() for value in config["Image_TypeI"].values()]

# 시간 설정
if time == '0':
    if "time" in config["Custom_Setting"]:
        cDate = config["Custom_Setting"]["time"]
        setTime = now - timedelta(days=int(cDate))
    else:
        setTime = now - timedelta(days=2)
    time = setTime.strftime('%Y%m%d%H%M%S')

# 최상위 디렉토리 패스 설정
if root == '0':
    if "root" in config["Custom_Setting"]:
        root = config["Custom_Setting"]["root"]
    else:
        root = config["Forder_Path"]["temp"]

# 확장자 설정
if ext == '0':
    if "ext" in config["Custom_Setting"]:
        ext = config["Custom_Setting"]["ext"]

if ext == '0':
    files = glob.glob(f'{root}/**/*', recursive=True)
elif ext == 'img': # 확장자가 img인 경우
    patterns = [f'{root}/**/*.{img_ext}' for img_ext in image_extensions]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))
else:
    patterns = [f'{root}/**/*.{ext}', f'{root}/**/*.{ext.upper()}']
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))

# 필터 설정
if filter == '':
    if "filter" in config["Custom_Setting"]:
        filter = config["Custom_Setting"]["filter"]
    else:
        filter = ''

formattime = datetime.strptime(time, '%Y%m%d%H%M%S')
formattime = formattime.strftime('%Y년 %m월 %d일 %H시 %M분 %S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')

CommonDef.makeLogTxt("클린 시작 ··· ", f"조건 『파일 루트: {root}, 파일 확장자: {ext if ext != '0' else '전체'}, 삭제 조건: {formattime} 이전 파일 모두 삭제, 필터: {filter if filter != '' else '없음'}』", log_dir, 'clean')

try:
    del_count = 0
    for file in files:
        try:
            if os.path.isfile(file):
                mtime = os.path.getmtime(file)
                mtime = datetime.fromtimestamp(mtime)
                mtime = mtime.strftime('%Y%m%d%H%M%S')
                if int(mtime) < int(time):
                    if filter not in os.path.basename(file) or filter == '':
                        os.remove(file)
                        CommonDef.makeLogTxt(file, " 삭제 완료", log_dir, 'clean')
                        del_count += 1
        except FileNotFoundError:
            CommonDef.makeLogTxt(file, " 파일이 존재하지 않음", log_dir, 'cleanError')
        except OSError as e:
            CommonDef.makeLogTxt(file, f" 삭제 실패: {str(e)}", log_dir, 'cleanError')

    CommonDef.makeLogTxt("클린 완료 ··· ", f"총 {del_count}개의 파일이 삭제되었습니다.", log_dir, 'clean')

    print(f"SUCCESS|{del_count}")

except Exception as error:
    CommonDef.makeLogTxt("클린 실패 ··· ", f"오류 발생: {str(error)}", log_dir, 'cleanError')
    print(f"FAILED|{error}")
