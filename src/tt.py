import subprocess

# 프레임 수를 정의합니다 (예: 10개)
num_frames = 10

# 프레임 파일들을 리스트에 추가합니다
frames = ["frame{:02d}.png".format(i) for i in range(1, num_frames + 1)]
watermark_image = "watermark.png"

# ImageMagick 명령어를 생성합니다
command = f'magick {" ".join(frames)} {watermark_image} -resize 100x100 -gravity southeast -composite output.gif'

# 명령어를 실행합니다
subprocess.run(command, shell=True)
