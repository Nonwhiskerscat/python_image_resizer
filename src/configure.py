import configparser
import datetime as dt
import os

# ConfigParser 객체 생성
config = configparser.ConfigParser()
config["Resize_Type"] = {}
Resize_Type = config["Resize_Type"]

if not "Resize_Type" in config:
    print("config['Resize_Type'] not exist")

pos_img_arr = [
    ".jpg",
    ".jpeg",
    ".bmp",
    ".png",
    ".webp",
    ".gif",
    ".bmp",
]

for ftype in pos_img_arr:
    Resize_Type[ftype] = ftype

# 이미지 리사이징 사이즈
config["Size_List"] = {"thumbnail": 200, "preview": 500}


# 워터마크 이미지 지원 idx
config["Water_Idx"] = {}
Water_Idx = config["Water_Idx"]
wat_idx_arr = ["1", "4", "5"]

for w in wat_idx_arr:
    Water_Idx[w] = w

# 워터마크 이미지 지원 확장자
config["Water_Type"] = {}
Water_Type = config["Water_Type"]
wat_img_arr = [
    ".jpg",
    ".jpeg",
    ".bmp",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
]

for w in wat_img_arr:
    Water_Type[w] = w

# 워터마크 이미지 위치
config["Water_Route"] = {
    1: os.getcwd().replace("\\", "/").strip('"')
    + "/watermark_logo/daily.png",  # 동아일보ss
    4: os.getcwd().replace("\\", "/").strip('"')
    + "/watermark_logo/sports.png",  # 스포츠동아
    5: os.getcwd().replace("\\", "/").strip('"')
    + "/watermark_logo/dotcom.png",  # 동아닷컴ss
}

# 이미지 비율 워터마크 크기
config["Water_Ratio"] = {1: 0.15, 4: 0.15, 5: 0.15}
config["Water_Opacity"] = {1: 0.9, 4: 0.9, 5: 0.9}
# 1: 동아일보, 4: 스포츠동아, 5: 동아닷컴

# 로그 및 에러로그 파일 위치
config["LogFile_Route"] = {
    "root": "C:/Users/김서용/Desktop/wps_image_converter/Log",
}

# config.ini 파일 생성
with open("image_custom.ini", "wt", encoding="UTF-8") as conf_file:
    config.write(conf_file)

# config.ini 파일 읽기
config.read("image_custom.ini", encoding="UTF-8")

# Section 정보 가져오기
sections = config.sections()


# # 이후 딕셔너리와 동일하게 처리 가능
# for item in config['File_info'].items():
#     print(item)

# for option in config['File_info'].keys():
#     print(option)

# for value in config['File_info'].values():
#     print(value)
