import os
import datetime as dt


class DateTime:
    now = dt.datetime.now()


class FileRoot:
    root = os.getcwd()
    root_dir = root.replace("\\", "/").strip('"')
    watermark_dir = root_dir + "/watermark"
    daily_dir = watermark_dir + "/daily"
    sports_dir = watermark_dir + "/sports"
    dotcom_dir = watermark_dir + "/dotcom"
    error_dir_1 = watermark_dir + "/error"

    resize_dir = root_dir + "/resize"
    origin_dir = resize_dir + "/original"
    thum_dir = resize_dir + "/thumbnail"
    prev_dir = resize_dir + "/preview"
    error_dir = resize_dir + "/error"
    errorY_dir = error_dir + "/" + str(DateTime.now.year)
    errorM_dir = errorY_dir + "/" + str(DateTime.now.month)
    errorD_dir = errorM_dir + "/" + str(DateTime.now.day)
    errorB_dir = errorD_dir + "/오전"
    errorA_dir = errorD_dir + "/오후"


class CommonDef:
    def createDir(path):
        t_isdir = os.path.isdir(path)
        if t_isdir == False:
            os.mkdir(path)

    def errorDateDir():
        CommonDef.createDir(FileRoot.error_dir)
        CommonDef.createDir(FileRoot.errorY_dir)
        CommonDef.createDir(FileRoot.errorM_dir)
        CommonDef.createDir(FileRoot.errorD_dir)

    def errorLogMaker(path, msg):
        CommonDef.errorDateDir()
        if DateTime.now.hour < 12:
            CommonDef.createDir(FileRoot.errorB_dir)
            tpath = FileRoot.errorB_dir + "/" + "오류로그.txt"
        else:
            CommonDef.createDir(FileRoot.errorA_dir)
            tpath = FileRoot.errorA_dir + "/" + "오류로그.txt"
        f = open(tpath, "a")
        f.write(str(DateTime.now) + ": " + path + " " + msg + "\n")
        f.close()
