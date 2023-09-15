from PIL import Image
import sys

# sys.argv[1~-2] => 이미지 크기
# sys.argv[-1] => 각 이미지 프레임

# 이미지 패스 모음
img_dura = sys.argv[-1]
imgs_arr = sys.argv
del imgs_arr[0], imgs_arr[-1]

# 이미지 프레임


######################## 크기 기준(비율 무시) ########################

# # 첫 번째 이미지를 기준으로 크기를 가져옴
# base_image = Image.open(image_paths[0])
# base_width, base_height = base_image.size

# # 이미지들을 열어 리스트에 저장하면서 크기를 조정
# resized_images = [Image.open(path).resize((base_width, base_height)) for path in image_paths]

######################## 너비 기준(비주얼 무시) ########################

# 첫 번째 이미지 기준 너비 설정
first_img = Image.open(imgs_arr[0])
first_width, _ = first_img.size
print(imgs_arr, img_dura)
# 이미지 오픈 및 리사이징
resized_images = [Image.open(path) for path in imgs_arr]
for i, img in enumerate(resized_images):
    width_percent = first_width / float(img.size[0])
    new_height = int((float(img.size[1]) * float(width_percent)))
    resized_images[i] = img.resize((first_width, new_height), Image.LANCZOS)


# 경로 설정
i_output = "output.gif"

# 첫 번째 이미지를 기준으로 GIF를 만듦
resized_images[0].save(
    i_output,
    save_all=True,
    append_images=resized_images[1:],
    loop=0,
    duration=int(img_dura),
)

# 작업이 끝났으면 이미지 객체를 닫음
for img in resized_images:
    img.close()
