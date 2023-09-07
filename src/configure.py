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

# 세션 생성

config["Size_List"] = {"thumbnail": 200, "preview": 500}

config["Water_Type"] = {}
Water_Type = config["Water_Type"]
wat_img_arr = [
    ".jpg",
    ".jpeg",
    ".bmp",
    ".png",
    ".webp",
    ".bmp",
]

for w in wat_img_arr:
    Water_Type[w] = w

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
