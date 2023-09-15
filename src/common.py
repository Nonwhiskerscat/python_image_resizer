import os
import datetime as dt

# 파일 이동 시 수정 필수!!!!!!!!!!!!!!!!!!!!


class DateTime:
    now = dt.datetime.now()


class FileRoot:
    program_dirname = (
        os.path.abspath("./Desktop/wps_image_converter").replace("\\", "/").strip('"')
    )
    in_root = program_dirname + "/Program/image_custom.ini"
    in_root = os.path.abspath(in_root)

    def LogDir(parent, idx):
        logY_dir = parent + "/" + str(DateTime.now.year)
        logM_dir = logY_dir + "/" + str(DateTime.now.month).zfill(2)
        logD_dir = (
            logM_dir
            + "/"
            + str(DateTime.now.month).zfill(2)
            + str(DateTime.now.day).zfill(2)
        )

        if idx == 1:
            return logY_dir
        elif idx == 2:
            return logM_dir
        elif idx == 3:
            return logD_dir

    def RootDir(cwd):
        return cwd.replace("\\", "/").strip('"')

    def SubDir(cwd, type):
        watermark_dir = FileRoot.RootDir(cwd) + "/watermark"

        if type == "watermark":
            return watermark_dir


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
        CommonDef.createDir(FileRoot.LogDir(parent, 3))

    # 로그 txt 생성 메서드
    def makeLogTxt(path, msg, parent, bool):
        CommonDef.makeLogDir(parent)
        if bool == True:
            tpath = FileRoot.LogDir(parent, 3) + "/" + "clear.txt"
        else:
            tpath = FileRoot.LogDir(parent, 3) + "/" + "error.txt"
        f = open(tpath, "a")
        f.write(str(DateTime.now) + " > " + path + " " + msg + "\n")
        f.close()

    # 파일 주소 추출
    def getFileRoot(i_path):
        return os.path.dirname(i_path)

    # 파일 확장자 추출
    def getFileExt(i_path):
        _, extension = os.path.splitext(i_path)
        return extension

    # 파일 이름 추출
    def getFileName(i_path):
        base_name = os.path.basename(i_path)
        file_name, _ = os.path.splitext(base_name)
        return file_name
