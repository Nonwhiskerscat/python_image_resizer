# 일부 라이브러리 불러오기
import os
import sys
import datetime as dt
import shutil
import ctypes
import configparser
from PIL import Image, ExifTags

config = configparser.ConfigParser()

class ProgramRes:
    pass


# 날짜 관련 객체 > DateTime
class DateTime:
    now = dt.datetime.now()


# 파일 경로 관련 객체 > FileRoot
class FileRoot:
    program_dirname = os.path.abspath(sys.argv[0])
    # custom.ini 파일의 경로
    in_root = os.path.join(os.path.dirname(program_dirname), "image_custom.ini")
    log_root = os.path.join(os.path.dirname(os.path.dirname(program_dirname)), "Log")
    water_root = os.path.join(os.path.dirname(program_dirname), "Watermark")

    ### ini 파일 위치는 exe 프로그램과 같은 경로에 위치해야 한다. 그렇지 않으면 프로그램 자체가 돌아가지 않는다. ###

    # 로그 폴더 경로
    def LogDir(parent, idx):
        logY_dir = parent + "/" + str(DateTime.now.year)  # Year 폴더 위치(yyyy)
        logM_dir = logY_dir + "/" + str(DateTime.now.month).zfill(2)  # Month 폴더 위치(mm)
        logD_dir = logM_dir + "/" + str(DateTime.now.day).zfill(2)  # Day 폴더 위치(mmdd)

        # 메서드 호출 시
        if idx == 1:  # idx가 1이면
            return logY_dir  # Year 폴더 생성
        elif idx == 2:  # idx가 2면
            return logM_dir  # Month 폴더 생성
        elif idx == 3:  # idx가 3이면
            return logD_dir  # Day 폴더 생성

    # Root 폴더 cwd 생성 메서드
    def RootDir(cwd):
        return cwd.replace("\\", "/").strip('"')

    # Root 폴더 cwd 아래 이름이 type인 SubDir 생성 메서드
    def SubDir(cwd, type):
        sub_dir = f"{FileRoot.RootDir(cwd)}/{type}"
        return sub_dir


# 공용으로 사용하는 메서드 저장용 객체
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

        return bool, msg

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

    # dpi 값 추출
    def getDPI(image, default_dpi=72) :
        # 이미지의 메타데이터 가져오기
        try:
            dpi_infoX, dpi_InfoY = image.info["dpi"]
            return dpi_infoX

        except (AttributeError, KeyError, TypeError):
            pass

        return default_dpi # 이미지의 DPI 정보가 메타데이터에 포함되어 있지 않는 경우 72를 리턴한다.(디폴트 값이 72이기 때문)
    
    # 새로운 DPI 정보 수정
    # def modifyDpi(image_path, new_dpi):
    #     with Image.open(image_path) as img:
    #         img.info['dpi'] = new_dpi
    #         img.save(image_path)

    
    # isdit 커스텀 메서드
    ## 기존의 isdigit()가 음수 혹은 float를 False 처리해버리기 때문에 어쩔 수 없이 만든 메서드...
    def isDigit(str):
        try:
            cat = float(str)
            return True
        except ValueError:
            return False

    # Gif 이미지의 프레임 개수를 리턴하는 메서드
    def aniFrames(img):
        with Image.open(img) as im:
            return im.n_frames

    # 에러 메시지를 생성하는 메서드
    def Errormsg(handle, msg, title, type):
        ctypes.windll.user32.MessageBoxW(handle, msg, title, type)


# 폴더 및 파일 삭제 관련 메서드를 저장한 객체
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


# e_log_msg = f"{CommonDef.getFileName(FileRoot.in_root)} 파일이 누락되어 있습니다."

# if not os.path.isdir(FileRoot.in_root):
#     CommonDef.Errormsg(0, e_log_msg, "에러 발생", 16)
