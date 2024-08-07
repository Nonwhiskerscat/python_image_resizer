# 일부 라이브러리 불러오기
import configparser
from common import *

#
# 여기서부터 이미지 전용 ini 생성 
# 


# ConfigParser 객체 생성
config = configparser.ConfigParser()

# 이미지 확장자
## Image_TypeI은 대부분 프로그램에서 사용
config["Image_TypeI"] = {}
Image_TypeI = config["Image_TypeI"]

pos_img_arr_1 = [
    ".jpg",
    ".jpeg",
    ".bmp",
    ".png",
    ".webp",
    ".gif",
]

# pos_img_arr 값을 Image_TypeI에 저장
for ftype in pos_img_arr_1:
    Image_TypeI[ftype] = ftype


# 움짤 전용 확장자
## Image_TypeI은 대부분 프로그램에서 사용
config["Ani_Image"] = {}
Ani_Image = config["Ani_Image"]

if not "Ani_Image" in config:
    print("config['Ani_Image'] not exist")

pos_img_arr_2 = [".gif", ".webp"]

for ftype in pos_img_arr_2:
    Ani_Image[ftype] = ftype

# 이미지 리사이징 사이즈
config["Size_List"] = {"thumbnail": 200, "preview": 500}


# 워터마크 이미지 지원 idx
config["Water_Idx"] = {}
Water_Idx = config["Water_Idx"]
wat_idx_arr = ["1", "4", "5"]

for w in wat_idx_arr:
    Water_Idx[w] = w

# 워터마크 이미지 위치
config["Water_Route"] = {
    1: FileRoot.program_dirname + "/Program/Watermark/daily.png",  # 동아일보ss
    4: FileRoot.program_dirname + "/Program/Watermark/sports.png",  # 스포츠동아
    5: FileRoot.program_dirname + "/Program/Watermark/dotcom.png",  # 동아닷컴ss
}

# 이미지 비율 워터마크 크기
config["Water_Ratio"] = {1: 0.15, 4: 0.15, 5: 0.15}
config["Water_Opacity"] = {1: 0.9, 4: 0.9, 5: 0.9}
# 1: 동아일보, 4: 스포츠동아, 5: 동아닷컴

# 로그 및 에러로그 파일 위치

# config.ini 파일 생성
with open("image_custom.ini", "wt", encoding="UTF-8") as conf_file:
    config.write(conf_file)

#
# 여기서부터 파일 전용 ini 생성 
# 

# ConfigParser 객체 생성
fconfig = configparser.ConfigParser()
# 워터마크 이미지 위치
fconfig["Forder_Path"] = {
    "TEMP": "\\\\10.70.8.191\dr_nas\WPS_Root\TEMP",
    "LOG": FileRoot.program_dirname + "/Log"
}

fconfig["Image_TypeI"] = {}
Image_TypeI = fconfig["Image_TypeI"]

pos_img_arr_1 = [
    "jpg",
    "jpeg",
    "bmp",
    "png",
    "webp",
    "gif",
]





config["LogFile_Route"] = {"root": FileRoot.program_dirname + "/Log"}

# config.ini 파일 생성
with open("file_custom.ini", "wt", encoding="UTF-8") as fconf_file:
    fconfig.write(fconf_file)
    
# # 이후 딕셔너리와 동일하게 처리 가능
# for item in config['File_info'].items():
#     print(item)

# for option in config['File_info'].keys():
#     print(option)

# for value in config['File_info'].values():
#     print(value)
