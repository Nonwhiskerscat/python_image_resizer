from PIL import Image

# 이미지 파일 경로
image_paths = [
    "image1.jpg",
    "image2.jpg",
    "image4.jpg",
    "image5.jpg",
    "image6.jpg",
    # 필요한 만큼 추가
]

# 첫 번째 이미지 기준 너비 설정
first_img = Image.open(image_paths[0])
first_width, _ = first_img.size

# 이미지 오픈 및 리사이징
resized_images = [Image.open(path) for path in image_paths]
for i, img in enumerate(resized_images):
    width_percent = first_width / float(img.size[0])
    new_height = int((float(img.size[1]) * float(width_percent)))
    resized_images[i] = img.resize((first_width, new_height), Image.LANCZOS)

# 경로 설정
i_output = "output.gif"

# 각 이미지의 표시 시간 (밀리초)
duration = 1000

# 첫 번째 이미지를 기준으로 GIF를 만듦
resized_images[0].save(
    i_output,
    save_all=True,
    append_images=resized_images[1:],
    loop=0,
    duration=duration,
)

# 작업이 끝났으면 이미지 객체를 닫음
for img in resized_images:
    img.close()
