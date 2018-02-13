from src.big.sp_bg001.transfer import bg1000cdto
from sklearn import svm, metrics
import urllib.request as req
import gzip, os, os.path
import struct
import glob, os.path, re, json


def preprocessing(bg1000cdto) :

    path = bg1000cdto.train_file_path
    train_data, train_label = loadfiles(path)

    path = bg1000cdto.test_file_path
    test_data, test_label = loadfiles(path)

    return train_data, train_label, test_data, test_label


def loadfiles(path) :
    files = glob.glob(path)
    train_data = []
    train_label = []

    for file_name in files:
        # 레이블 구하기
        basename = os.path.basename(file_name)
        lang = basename.split("-")[0]
        # 텍스트 추출하기
        with open(file_name, "r", encoding='utf-8') as f:
            text = f.read()
        text = text.lower()
        # 알파벳 출현빈도 구하기
        code_a = ord("a")
        code_z = ord("z")
        count = [0 for n in range(0, 26)]
        for character in text:
            code_current = ord(character)
            if code_a <= code_current <= code_z:
                # print(code_current, code_a, code_current - code_a)
                count[code_current - code_a] += 1
        # 표현은 0과 1로해야 되므로 정규화를 진행한다.
        total = sum(count)
        # count를 map으로 변환한다.
        count = list(map(lambda n: n / total, count))
        train_data.append(count)
        train_label.append(lang)

    return train_data, train_label


def test(n):
    return 10

