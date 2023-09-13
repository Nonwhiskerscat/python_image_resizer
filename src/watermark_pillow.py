from PIL import Image, ImageSequence
import math
from common import *
import configparser

w_mark_route = "./watermark_logo/sports.png"

# f_rt, w_rt = input("파일 경로, 워터마크 idx").split()

# if w_rt == 1:
#     w_mark_route = "./watermark_logo/daily.png"
# elif w_rt == 4:
#     w_mark_route = "./watermark_logo/sports.png"
# elif w_rt == 5:
#     w_mark_route = "./watermark_logo/dotcom.png"
# else:
#     w_mark_route = "./watermark_logo/daily.png"


def wWidth(width):
    return math.ceil(width * 0.15)


def wHeight(wmark, wwidth):
    w_ratio = wmark.width / wmark.height
    return math.ceil(wwidth / w_ratio)


# 사용 예시


def watermarkForGif(
    input_gif_path,
    watermark_image_path,
    output_gif_path,
    transparency,
):
    # GIF 열기
    original_gif = Image.open(input_gif_path)
    watermark = Image.open(watermark_image_path)
    # 결과 GIF 프레임들
    watermarked_frames = []

    for frame in ImageSequence.Iterator(original_gif):
        # 각 프레임에 워터마크 추가
        original_frame = frame.convert("RGBA")
        frame = original_frame.copy()

        # 이전 프레임의 시간 간격 유지
        if hasattr(frame.info, "duration"):
            frame.info["duration"] = original_gif.info["duration"]

        # 워터마크 크기 조정
        watermark_resized = watermark.resize(
            (wWidth(frame.width), wHeight(watermark, wWidth(frame.width)))
        )

        # 알파 채널 생성
        alpha = watermark_resized.getchannel("A")
        alpha = alpha.point(lambda p: p * transparency / 255)
        watermark_resized.putalpha(alpha)

        position_x = frame.width - math.ceil(1.1 * watermark_resized.width)
        position_y = (
            frame.height
            - watermark_resized.height
            - math.ceil(0.1 * watermark_resized.width)
        )

        # 워터마크 위치 설정
        transparent = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        transparent.paste(watermark_resized, (position_x, position_y))

        watermarked_frame = Image.alpha_composite(frame, transparent)
        watermarked_frames.append(watermarked_frame)

    # 새로운 GIF 만들기
    watermarked_gif = Image.new("RGBA", original_gif.size)
    watermarked_gif.save(
        output_gif_path,
        save_all=True,
        format="gif",
        append_images=watermarked_frames[1:],
        optimize=True,
        loop=0xFF,
    )

    # 프레임별 저장
    # for index, frame in enumerate(watermarked_frames):
    #     save_files = f"frame_{index}.png"
    #     frame.save(save_files, format="PNG")


# 함수 호출 (input_gif_path에 원본 GIF 경로, output_gif_path에 결과 GIF 경로, watermark_image_path에 워터마크 이미지 경로)
# watermarkForGif("input.gif", "watermark.png", "output.gif", 196)


def watermarkForImg(input_image_path, output_image_path, watermark_image_path, opacity):
    original_image = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")

    # 워터마크 크기 조정
    watermark_resized = watermark.resize(
        (wWidth(original_image.width), wHeight(watermark, wWidth(original_image.width)))
    )

    # 알파 채널 생성
    alpha = watermark_resized.getchannel("A")
    alpha = alpha.point(lambda p: p * opacity / 255)
    watermark_resized.putalpha(alpha)

    position_x = original_image.width - math.ceil(1.1 * watermark_resized.width)
    position_y = (
        original_image.height
        - watermark_resized.height
        - math.ceil(0.1 * watermark_resized.width)
    )

    transparent = Image.new(
        "RGBA", (original_image.width, original_image.height), (0, 0, 0, 0)
    )
    transparent.paste(original_image, (0, 0))
    transparent.paste(watermark_resized, (position_x, position_y), watermark_resized)

    transparent.save(output_image_path, "PNG")


# 자동화
possible_img_watermark = []

# ConfigParser 객체 생성
config = configparser.ConfigParser()

config.read("image_custom.ini", encoding="UTF-8")
for key in config["Water_Type"].keys():
    possible_img_watermark.append(key)
# 사용 예시
# watermarkForImg("input.jpg", "output.jpg", "watermark.png", 196)

if os.path.isdir(FileRoot.root_dir) == False:
    CommonDef.errorLogMaker(FileRoot.root_dir, "폴더가 존재하지 않습니다.", FileRoot.watermark_dir)
else:
    for root, dirs, files in os.walk(FileRoot.root_dir):
        if len(files) > 0:
            for file_name in files:
                if (
                    os.path.splitext(file_name)[-1].lower() in possible_img_watermark
                    and root == FileRoot.root_dir
                ):
                    CommonDef.createDir(FileRoot.watermark_dir)
                    img_path = root + "/" + file_name
                    watermarkForImg(
                        img_path,
                        FileRoot.watermark_dir + "/" + file_name,
                        w_mark_route,
                        225,
                    )
                elif (
                    os.path.splitext(file_name)[-1].lower() == ".gif"
                    and root == FileRoot.root_dir
                ):
                    CommonDef.createDir(FileRoot.watermark_dir)
                    img_path = root + "/" + file_name
                    watermarkForGif(
                        img_path,
                        w_mark_route,
                        FileRoot.watermark_dir + "/" + file_name,
                        225,
                    )

                elif root == FileRoot.root_dir:
                    CommonDef.createDir(FileRoot.watermark_dir)
                    CommonDef.errorLogMaker(
                        file_name, "지원하지 않는 파일 확장자입니다.", FileRoot.watermark_dir
                    )

print("모든 작업이 끝났습니다.")
