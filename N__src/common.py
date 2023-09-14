import os
import datetime as dt


class DateTime:
    now = dt.datetime.now()


class FileRoot:
    def ErrorDir(parent, idx):
        error_dir = parent + "/error"
        errorY_dir = error_dir + "/" + str(DateTime.now.year)
        errorM_dir = errorY_dir + "/" + str(DateTime.now.month)
        errorD_dir = errorM_dir + "/" + str(DateTime.now.day)
        errorB_dir = errorD_dir + "/오전"
        errorA_dir = errorD_dir + "/오후"

        if idx == 1:
            return error_dir
        elif idx == 2:
            return errorY_dir
        elif idx == 3:
            return errorM_dir
        elif idx == 4:
            return errorD_dir
        elif idx == 5:
            return errorB_dir
        elif idx == 6:
            return errorA_dir

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
    def createDir(path):
        t_isdir = os.path.isdir(path)
        if t_isdir == False:
            os.mkdir(path)

    def errorDateDir(parent):
        CommonDef.createDir(FileRoot.ErrorDir(parent, 1))
        CommonDef.createDir(FileRoot.ErrorDir(parent, 2))
        CommonDef.createDir(FileRoot.ErrorDir(parent, 3))
        CommonDef.createDir(FileRoot.ErrorDir(parent, 4))

    def errorLogMaker(path, msg, parent):
        CommonDef.errorDateDir(parent)
        if DateTime.now.hour < 12:
            CommonDef.createDir(FileRoot.ErrorDir(parent, 5))
            tpath = FileRoot.ErrorDir(parent, 5) + "/" + "오류로그.txt"
        else:
            CommonDef.createDir(FileRoot.ErrorDir(parent, 6))
            tpath = FileRoot.ErrorDir(parent, 6) + "/" + "오류로그.txt"
        f = open(tpath, "a")
        f.write(str(DateTime.now) + ": " + path + " " + msg + "\n")
        f.close()
