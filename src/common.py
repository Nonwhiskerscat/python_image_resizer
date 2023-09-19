import os
import datetime as dt
import shutil
from PIL import Image

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
        sub_dir = f"{FileRoot.RootDir(cwd)}/{type}"
        return sub_dir


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
            tpath = FileRoot.LogDir(parent, 3) + "/" + "failed.txt"
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

    # isdit 커스텀 함수
    ## 기존의 isdigit()가 음수 혹은 float를 False 처리해버리기 때문에 어쩔 수 없이 만든 함수...
    def isDigit(str):
        try:
            cat = float(str)
            return True
        except ValueError:
            return False

    # Gif 이미지의 프레임 개수를 리턴하는 함수
    def aniFrames(img):
        with Image.open(img) as im:
            return im.n_frames


class DeleteCommon:
    # 특정 파일 및 폴더 삭제(단일)
    def One(f_path):
        try:
            if os.path.isfile(f_path):
                os.unlink(f_path)
            elif os.path.isdir(f_path):
                shutil.rmtree(f_path)
        except Exception as e:
            print(f"파일 삭제 오류: {e}")

    # 특정 파일 삭제(배열 혹은 sys.argv)
    def Multi(f_paths):
        for files in f_paths:
            try:
                os.unlink(files)
            except Exception as e:
                print(f"파일 삭제 오류: {e}")

    # 폴더 내 모든 파일 삭제
    def All(fo_path):
        for files in os.listdir(fo_path):
            file_path = os.path.join(fo_path, files)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"파일 삭제 오류: {e}")

    # 폴더 내 특정 파일 삭제(확장자 기준)
    def CommonExt(fo_path, ext):
        # 폴더 내의 파일 목록 가져오기
        for files in os.listdir(fo_path):
            # 특정 확장자를 가진 파일인지 확인
            try:
                if files.endswith(ext):
                    file_path = os.path.join(fo_path, files)
                    # 파일 삭제
                    os.unlink(file_path)
            except Exception as e:
                print(f"파일 삭제 오류: {e}")

    # 폴더 내 특정 파일 삭제(파일명 기준)
    def CommonKey(fo_path, keyword):
        # 폴더 내의 파일 목록 가져오기
        for files in os.listdir(fo_path):
            # 특정 문자열을 포함하는 파일인지 확인
            try:
                if keyword in CommonDef.getFileName(files):
                    file_path = os.path.join(fo_path, files)
                    # 파일 삭제
                    os.unlink(file_path)
            except Exception as e:
                print(f"파일 삭제 오류: {e}")
