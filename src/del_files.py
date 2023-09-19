import sys
import os
from common import *


def DelCommon(cat):
    # 0 sys.argv의 길이가 1일 때(아무 것도 입력되지 않았을 때)
    if len(cat) == 0:
        return False

    # 1 sys.argv의 길이가 2일 때
    elif len(cat) == 2:
        ## 단일 파일 및 폴더 삭제 시(입력 받은 값이 파일 패스일 때)
        try:
            DeleteCommon.One(cat[1])
            # print("1 삭제 성공")
            return True
        except Exception as e:
            # print("1 삭제 실패 " + str(e))
            return False

    else:
        # 2 sys_argv의 길이가 3일 때(폴더 명 + 확장자/키워드/*)
        if len(cat) == 3:
            ## 2.1 확장자 기준으로 파일 삭제 시(폴더 명 + *.확장자)
            if os.path.isdir(cat[1]):
                if cat[-1].startswith("*.") == True:
                    try:
                        DeleteCommon.CommonExt(cat[1], CommonDef.getFileExt(cat[-1]))
                        # print("2 삭제 성공")
                        return True
                    except Exception as e:
                        # print("2.1 삭제 실패 " + str(e))
                        return False

                ## 2.2 단일 폴더 내 파일 전부 삭제 시(폴더 명 + 키워드)
                # >> 폴더 내 자식 폴더는 삭제되지 않는다는 점에서 1번 경우와 차별점이 있음
                elif cat[-1] == "*":
                    try:
                        DeleteCommon.All(cat[1])
                        # print("2.2 삭제 성공")
                        return True
                    except Exception as e:
                        # print("2.2 삭제 실패 " + str(e))
                        return False

                ## 2.3 키워드 기준으로 파일 삭제 시(폴더 명 + 확장자 + 키워드)
                elif not (os.path.isfile(cat[-1]) or os.path.isdir(cat[-1])):
                    try:
                        DeleteCommon.CommonKey(cat[1], cat[-1])
                        # print("2.3 삭제 성공")
                        return True
                    except Exception as e:
                        # print("2.3 삭제 실패 " + str(e))
                        return False

        # 3 sys.argv의 길이가 3 이상일 때
        # 위 조건에서 Return 값을 반환하지 못한 요소에 대해서는 다음 조건 충족
        if len(cat) > 2:
            del cat[0]
            for val in cat:
                try:
                    DeleteCommon.One(val)
                    # print("3 삭제 성공")
                except Exception as e:
                    # print("3 삭제 실패 " + str(e))
                    t = 1
            return True


DelCommon(sys.argv)
