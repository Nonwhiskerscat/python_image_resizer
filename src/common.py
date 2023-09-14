import os
import datetime as dt


class DateTime:
    now = dt.datetime.now()


class FileRoot:
    # 파일 이동 시 수정 필수!!!!!!!!!!!!!!!!!!!!
    in_root = "C:/Users/김서용/Desktop/wps_image_converter/Program/image_custom.ini"

    def LogDir(parent, idx):
        logY_dir = parent + "/" + str(DateTime.now.year)
        logD_dir = (
            logY_dir
            + "/"
            + str(DateTime.now.month).zfill(2)
            + str(DateTime.now.day).zfill(2)
        )

        if idx == 1:
            return logY_dir
        elif idx == 2:
            return logD_dir

    def RootDir(cwd):
        return cwd.replace("\\", "/").strip('"')

    def SubDir(cwd, type):
        watermark_dir = FileRoot.RootDir(cwd) + "/watermark"

        resize_dir = FileRoot.RootDir(cwd) + "/resize"
        origin_dir = resize_dir + "/original"
        thum_dir = resize_dir + "/thumbnail"
        prev_dir = resize_dir + "/preview"

        if type == "watermark":
            return watermark_dir
        elif type == "resize":
            return resize_dir
        elif type == "origin":
            return origin_dir
        elif type == "thumbnail":
            return thum_dir
        elif type == "preview":
            return prev_dir


class CommonDef:
    # 폴더 생성 메서드
    def createDir(path):
        t_isdir = os.path.isdir(path)
        if t_isdir == False:
            os.mkdir(path)

    # 로그 폴더 생성 메서드
    def makeLogDir(parent):
        CommonDef.createDir(FileRoot.LogDir(parent, 1))
        CommonDef.createDir(FileRoot.LogDir(parent, 2))

    # 로그 txt 생성 메서드
    def makeLogTxt(path, msg, parent, bool):
        CommonDef.makeLogDir(parent)
        if bool == True:
            tpath = FileRoot.LogDir(parent, 2) + "/" + "clear.txt"
        else:
            tpath = FileRoot.LogDir(parent, 2) + "/" + "error.txt"
        f = open(tpath, "a")
        f.write(str(DateTime.now) + " > " + path + " " + msg + "\n")
        f.close()

    # 파일 확장자 추출
    def getFileExt(cat):
        _, extension = os.path.splitext(cat)
        return extension
