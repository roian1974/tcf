
from sklearn import svm, metrics
import urllib.request as req
import gzip, os, os.path
import struct
import glob, os.path, re, json
from src.big.sp_bg001.transfer import bg1000cdto, big1000cdto
from src.big.sp_bg001.business.dc.mod import catchLANG_preprocessing
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging


def preAnalysis(big1000cdto) :

    try:
        file = big1000cdto.indata['file']
        # 데이터 읽어 들이기--- (※1)
        mr = pd.read_csv(file, header=None)

        # 데이터 내부의 기호를 숫자로 변환하기--- (※2)
        label = []
        data = []
        attr_list = []
        for row_index, row in mr.iterrows():
            label.append(row.ix[0])
            row_data = []
            for v in row.ix[1:]:
                row_data.append(ord(v))
            data.append(row_data)

        # 학습 전용과 테스트 전용 데이터로 나누기 --- (※3)
        data_train, data_test, label_train, label_test = train_test_split(data, label)

        big1000cdto.ddto['data_train'] = data_train
        big1000cdto.ddto['label_train'] = label_train
        big1000cdto.ddto['data_test'] = data_test
        big1000cdto.ddto['label_test'] = label_test

    except Exception as err:
        comlogging.logger.error('preAnalysis 에러 ' + str(err))
        include.setErr('EBIG1004', 'preAnalysis,' + str(err))
    else:
        comlogging.logger.info('preAnalysis-성공')
    finally:
        if include.isError() == False:
            return big1000cdto
        else:
            return False


def trainModel(big1000cdto) :

    try:
        data_train = big1000cdto.ddto['data_train']
        label_train = big1000cdto.ddto['label_train']
        data_test = big1000cdto.ddto['data_test']
        label_test = big1000cdto.ddto['label_test']

        print(big1000cdto.indata['model_type'])
        # 데이터 학습시키기 --- (※4)
        clf = ''
        if big1000cdto.indata['model_type'] == "Randomforest":
            clf = RandomForestClassifier()
        elif big1000cdto.indata['model_type'] == "svc":
            clf = svm.SVC()
        elif big1000cdto.indata['model_type'] == "AdaBoostClassifier":
            clf = AdaBoostClassifier()
        elif big1000cdto.indata['model_type'] == "MLPClassifier":
            clf = MLPClassifier()

        clf.fit(data_train, label_train)

        # 데이터 예측하기 --- (※5)
        predict = clf.predict(data_test)

        # 결과 테스트하기 --- (※6)
        ac_score = metrics.accuracy_score(label_test, predict)
        cl_report = metrics.classification_report(label_test, predict)

        print("정답률 =", ac_score)
        print("리포트 =\n", cl_report)

        big1000cdto.outdata['accuracy'] = ac_score
        big1000cdto.outdata['report'] = cl_report

    except Exception as err:
        comlogging.logger.error('trainModel 에러 ' + str(err))
        include.setErr('EBIG1004', 'trainModel,' + str(err))
    else:
        comlogging.logger.info('trainModel-성공')
    finally:
        if include.isError() == False:
            return big1000cdto
        else:
            return False


# XOR 예측모델 테스트
def xorPredit(bg1000cdto):
    clf = svm.SVC()
    clf.fit(bg1000cdto.indata, bg1000cdto.labels)
    results = clf.predict(bg1000cdto.examples)
    score = metrics.accuracy_score(bg1000cdto.examples_labels, results)
    print(results)
    print('정확도:', score)


# 붓꽃판별 테스트
def flowerPredit(bg1000cdto):
    clf = svm.SVC()

    clf.fit(bg1000cdto.indata, bg1000cdto.labels)
    results = clf.predict(bg1000cdto.examples)
    # score = metrics.accuracy_score(bg1000cdto.examples_labels, results)
    print("붓꽃의품종은 ",results)
    # print('정확도:', score)

#
def flowerPredit2(bg1000cdto):

    clf = svm.SVC()

    clf.fit(bg1000cdto.train_data, bg1000cdto.train_label)

    results = clf.predict(bg1000cdto.test_data)
    score = metrics.accuracy_score(bg1000cdto.test_label,results)

    print("붓꽃의품종은 ",results)
    print('정확도:', score)

# todo : 손글씨 다운로드 후 압축해제
def miniDownload(bg1000cdto) :
    savepath = "./mnist"
    baseurl = "http://yann.lecun.com/exdb/mnist"
    files = [
        "train-images-idx3-ubyte.gz",
        "train-labels-idx1-ubyte.gz",
        "t10k-images-idx3-ubyte.gz",
        "t10k-labels-idx1-ubyte.gz"]
    # 다운로드
    if not os.path.exists(savepath): os.mkdir(savepath)
    for f in files:
        url = baseurl + "/" + f
        loc = savepath + "/" + f
        print("download:", url)
        if not os.path.exists(loc):
            req.urlretrieve(url, loc)
    # GZip 압축 해제
    for f in files:
        gz_file = savepath + "/" + f
        raw_file = savepath + "/" + f.replace(".gz", "")
        print("gzip:", f)
        with gzip.open(gz_file, "rb") as fp:
            body = fp.read()
            with open(raw_file, "wb") as w:
                w.write(body)
    print("ok")

def handTypeModel(bg1000cdto):

    clf = svm.SVC()

    clf.fit(bg1000cdto.train_data, bg1000cdto.train_label)

    results = clf.predict(bg1000cdto.test_data)
    score = metrics.accuracy_score(bg1000cdto.test_label,results)

    # print("붓꽃의품종은 ",results)
    print('정확도:', score)


def toCSV(bg1000cdto) :

    name = bg1000cdto.file_name
    maxdata = bg1000cdto.maxdata
    # 레이블 파일과 이미지 파일 열기
    lbl_f = open("./mnist/" + name + "-labels-idx1-ubyte", "rb")
    img_f = open("./mnist/" + name + "-images-idx3-ubyte", "rb")
    csv_f = open("./mnist/" + name + ".csv", "w", encoding="utf-8")
    # 헤더 정보 읽기 --- (※1)
    mag, lbl_count = struct.unpack(">II", lbl_f.read(8))
    mag, img_count = struct.unpack(">II", img_f.read(8))
    rows, cols = struct.unpack(">II", img_f.read(8))
    pixels = rows * cols
    # 이미지 데이터를 읽고 CSV로 저장하기 --- (※2)
    res = []
    for idx in range(lbl_count):
        if idx > maxdata: break
        label = struct.unpack("B", lbl_f.read(1))[0]
        bdata = img_f.read(pixels)
        sdata = list(map(lambda n: str(n), bdata))
        csv_f.write(str(label) + ",")
        csv_f.write(",".join(sdata) + "\r\n")
        # 잘 저장됐는지 이미지 파일로 저장해서 테스트하기 -- (※3)
        if idx < 10:
            s = "P2 28 28 255\n"
            s += " ".join(sdata)
            iname = "./mnist/{0}-{1}-{2}.pgm".format(name, idx, label)
            with open(iname, "w", encoding="utf-8") as f:
                f.write(s)
    csv_f.close()
    lbl_f.close()
    img_f.close()

# 언어 이해
def catchLANG(bg1000cdto) :

    # 전처리
    train_data, train_label, test_data, test_label = catchLANG_preprocessing.preprocessing(bg1000cdto)

    # print(train_data,train_label)

    # 그래프 보여기주
    graph_dict = {}
    for i in range(0, len(train_label)):
        label = train_label[i]
        data = train_data[i]
        if not ( label in graph_dict ) :
            graph_dict[label] = data
    asclist = [ [chr(n) for n in range(97, 97+26)]]
    df = pd.DataFrame(graph_dict, index=asclist)

    #그래프 그리기
    plt.style.use('ggplot')
    df.plot(kind='bar', subplots=True, ylim=(0,0.15))
    plt.savefig("lang-plot.png")

    # 훈련시키기기

    clf =''
    if bg1000cdto.model_type == "Randomforest" :
        clf = RandomForestClassifier()
    elif bg1000cdto.model_type == "svc" :
        clf = svm.SVC()
    elif bg1000cdto.model_type == "AdaBoostClassifier" :
        clf = AdaBoostClassifier()
    elif big1000cdto.model_type == "MLPClassifier":
        clf = MLPClassifier()



    clf.fit(train_data, train_label)
    results = clf.predict(test_data)

    score = metrics.accuracy_score(test_label,results)

    report = metrics.classification_report(test_label,results)

    print("--- report ---")
    print("정확도 ",score)
    print(report)


def mushroomModel() :
    # 데이터 읽어 들이기--- (※1)
    mr = pd.read_csv("mushroom.csv", header=None)
    # 데이터 내부의 기호를 숫자로 변환하기--- (※2)
    label = []
    data = []
    attr_list = []
    for row_index, row in mr.iterrows():
        label.append(row.ix[0])
        row_data = []
        for v in row.ix[1:]:
            row_data.append(ord(v))
        data.append(row_data)
    # 학습 전용과 테스트 전용 데이터로 나누기 --- (※3)
    data_train, data_test, label_train, label_test = \
        train_test_split(data, label)
    # 데이터 학습시키기 --- (※4)
    clf = RandomForestClassifier()
    clf.fit(data_train, label_train)
    # 데이터 예측하기 --- (※5)
    predict = clf.predict(data_test)
    # 결과 테스트하기 --- (※6)
    ac_score = metrics.accuracy_score(label_test, predict)
    cl_report = metrics.classification_report(label_test, predict)
    print("정답률 =", ac_score)
    print("리포트 =\n", cl_report)



