# from common import add_func, FileRoot

from wand.image import Image
import os
from imgpy import Img
import math


global img_cnt
img_cnt = False

root = os.getcwd()
root_dir = root.replace("\\", "/").strip('"')
watermark_dir = root_dir + "/watermark"
daily_dir = watermark_dir + "/daily"
sports_dir = watermark_dir + "/sports"
dotcom_dir = watermark_dir + "/dotcom"
error_dir = watermark_dir + "/error"


w_mark1 = Image(filename="./watermark_logo/sports.png")
w_mark2 = Image(filename="./watermark_logo/daily.png")
w_mark3 = Image(filename="./watermark_logo/dotcom.png")

img1 = Image(filename="rabbit.jpg")
img2 = Image(filename="cat-66980.jpg")
img3 = Image(filename="animal-1844835.jpg")


# 워터마크 리사이즈 필요 시 주석 풀고 사용
def wWidth(width):
    return math.ceil(width * 0.15)


def wHeight(wwidth, n):
    if n == 1:
        w_ratio = w_mark1.size[0] / w_mark1.size[1]
    if n == 2:
        w_ratio = w_mark2.size[0] / w_mark2.size[1]
    if n == 3:
        w_ratio = w_mark3.size[0] / w_mark3.size[1]
    return math.ceil(wwidth / w_ratio)


w_mark1.resize(wWidth(img1.size[0]), wHeight(wWidth(img1.size[0]), 1))
x1 = img1.size[0] - math.ceil(1.1 * w_mark1.size[0])
y1 = img1.size[1] - w_mark1.size[1] - math.ceil(0.1 * w_mark1.size[0])
img1.watermark(image=w_mark1, transparency=0.3, left=x1, top=y1)
img1.save(filename="nwater1.jpg")

w_mark2.resize(wWidth(img2.size[0]), wHeight(wWidth(img2.size[0]), 2))
x2 = img2.size[0] - math.ceil(1.1 * w_mark2.size[0])
y2 = img2.size[1] - w_mark2.size[1] - math.ceil(0.1 * w_mark2.size[0])
img2.watermark(image=w_mark2, transparency=0.3, left=x2, top=y2)
img2.save(filename="nwater2.jpg")

w_mark3.resize(wWidth(img3.size[0]), wHeight(wWidth(img3.size[0]), 3))
x3 = img3.size[0] - math.ceil(1.1 * w_mark3.size[0])
y3 = img3.size[1] - w_mark3.size[1] - math.ceil(0.1 * w_mark3.size[0])
img3.watermark(image=w_mark3, transparency=0.3, left=x3, top=y3)
img3.save(filename="nwater3.jpg")


def waterMarkImg(cat):
    if cat == 1:  # 동아일보 워터 마크
        return "watermark_daily.png"
    elif cat == 4:  # 스포츠 동아 워터 마크
        return "watermark_sports.png"
    elif cat == 5:  # 동아닷컴 워터 마크
        return "watermark_dotcom.png"
