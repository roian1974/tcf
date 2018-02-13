
from sklearn import svm, metrics
import urllib.request as req
import gzip, os, os.path
import struct
import glob, os.path, re, json
from src.big.sp_bg001.transfer import bg1000cdto
from src.big.sp_bg001.business.dc.mod import catchLANG_preprocessing


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

    # 훈련시키기기
    clf = svm.SVC()
    clf.fit(train_data, train_label)
    results = clf.predict(test_data)

    score = metrics.accuracy_score(test_label,results)

    report = metrics.classification_report(test_label,results)

    print("--- report ---")
    print("정확도 ",score)
    print(report)



