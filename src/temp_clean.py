import os
import configparser
import sys
from datetime import datetime, timedelta
import glob
from common import *

root = sys.argv[1] if len(sys.argv) > 1 else '0'
ext = sys.argv[2] if len(sys.argv) > 2 else '0'
time = sys.argv[3] if len(sys.argv) > 3 else '0'

now = datetime.now()

# 로그 파일 생성
log_dir = FileRoot.log_root
CommonDef.createDir(log_dir)

# ini 파일 읽어오기
config = configparser.ConfigParser()
config.read(FileRoot.fn_root, encoding="UTF-8")

# 시간 값이 0으로 들어오면 일주일 전 다음날 0시
if time == '0':
    one_week_ago = now - timedelta(weeks=1)
    next_day_midnight = (one_week_ago + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time = next_day_midnight.strftime('%Y%m%d%H%M%S')

if root == '0':
    root = config["Forder_Path"]["temp"]

image_extensions = []
for key in config["Image_TypeI"].keys():
    image_extensions.append(key)
    image_extensions.append(key.upper())

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

formattime = datetime.strptime(time, '%Y%m%d%H%M%S')
formattime = formattime.strftime('%Y년 %m월 %d일 %H시 %M분 %S초'.encode('unicode-escape').decode()).encode().decode('unicode-escape')

CommonDef.makeLogTxt("클린 시작 ··· ", f"조건 『파일 루트: {root}, 파일 확장자: {ext if ext != '0' else '전체'}, 삭제 조건: {formattime} 이전 파일 모두 삭제』", log_dir, 'clean')

try:
    del_count = 0
    for file in files:
        try:
            mtime = os.path.getmtime(file)
            mtime = datetime.fromtimestamp(mtime)
            mtime = mtime.strftime('%Y%m%d%H%M%S')
            if os.path.isfile(file):
                if(int(mtime) < int(time)):
                    os.remove(file)
                    CommonDef.makeLogTxt(file, " 삭제 완료", log_dir, 'clean')
                    del_count += 1

        except OSError as e:
            CommonDef.makeLogTxt(file, " 삭제 실패", log_dir, 'cleanError')

    CommonDef.makeLogTxt("클린 완료 ··· ", f"총 {del_count}개의 파일이 삭제되었습니다.", log_dir, 'clean')

    print(f"SUCCESS|{del_count}")

except Exception as error:
    CommonDef.makeLogTxt("클린 실패 ··· ", error, log_dir, 'cleanError')
    print(f"FAILED|{error}")


# exe 파일 배포 시
# pyinstaller --noconsole -F  ./src/temp_clean.py 입력