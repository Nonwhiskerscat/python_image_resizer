from imgpy import Img
from datetime import date
import os 
import math

#날짜별 파일분류
today = date.today()
today_dir = today.strftime("%Y%m%d")

# 디렉토리
root = input("폴더 경로를 입력하세요: ")
# root_dir = 'C:/Users/김서용/Desktop/이미지리사이즈 샘플/WPS 화상 버그/5. 사진빨갛게나옴(리사이즈는 됨)'
root_dir = root.replace('\\', '/').strip('"')

bighead_dir = root_dir + '/bighead'
origin_dir = bighead_dir + '/original'
thum_dir = bighead_dir + '/thumnail'
prev_dir = bighead_dir + '/preview'

is_bighead_dir = os.path.isdir(bighead_dir)
is_origin_dir = os.path.isdir(origin_dir)
is_thum_dir = os.path.isdir(thum_dir)
is_prev_dir = os.path.isdir(prev_dir)

if(is_bighead_dir == False):
    os.mkdir(bighead_dir)

if(is_origin_dir == False):
    os.mkdir(origin_dir)

if(is_thum_dir == False):
    os.mkdir(thum_dir)

if(is_prev_dir == False):
    os.mkdir(prev_dir)

class imageCustom: 
    thumnail_width = 200
    preview_width = 500

    def _thumnail_height(cat):
        return math.ceil((imageCustom.thumnail_width/cat.width) * cat.height)
    
    def _preview_height(cat):
        return math.ceil((imageCustom.preview_width/cat.width) * cat.height)
    
    def _thumnail_size(cat): 
        return (imageCustom.thumnail_width, imageCustom._thumnail_height(cat))
    
    def _preview_size(cat):
        return (imageCustom.preview_width, imageCustom._preview_height(cat))

def originConverter(file_path, save_path): 
    with Img(fp=file_path) as im:
        im.save(fp=save_path)
        print(file_name + ' 원본 다운 완료')


def thumnailConverter(file_path, save_path): 
    with Img(fp=file_path) as im:
        im.resize(imageCustom._thumnail_size(im))
        im.save(fp=save_path)
        print(file_name + ' 썸네일 변환 완료')

def previewConverter(file_path, save_path): 
    with Img(fp=file_path) as im:
        im.resize(imageCustom._preview_size(im))
        im.save(fp=save_path)
        print(file_name + ' 프리뷰 변환 완료')

img_path_list = []
possible_img_extension = ['.jpg', '.jpeg', '.JPG', '.bmp', '.png', '.webp', '.gif'] 
for (root, dirs, files) in os.walk(root_dir):
    if len(files) > 0:
        for file_name in files:
            if os.path.splitext(file_name)[1] in possible_img_extension and root==root_dir:
                img_path = root + '/' + file_name 
                img_path = img_path.replace('\\', '/')
                img_path_list.append(img_path)
                originConverter(img_path, origin_dir + '/' + file_name)
                thumnailConverter(img_path, thum_dir + '/' + file_name)
                previewConverter(img_path, prev_dir + '/' + file_name)

# Crop image
def cropImg(file_path, save_path):
    with Img(fp=file_path) as im:
        im.crop(box=(10, 10, 110, 110))
        im.save(fp=save_path)