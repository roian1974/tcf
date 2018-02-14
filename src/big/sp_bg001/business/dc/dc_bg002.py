import pandas as pd
import numpy as np
from src.com.fwk.business.util.logging import comlogging
from gensim.models import word2vec
import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn import svm, metrics
import matplotlib.pyplot as plt
import seaborn as sns
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam
from keras.utils import np_utils


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


def kerasTest(cdto) :

    # MNIST 데이터 읽어 들이기 --- (※1)
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # 데이터를 float32 자료형으로 변환하고 정규화하기 --- (※2)
    X_train = X_train.reshape(60000, 784).astype('float32')
    X_test = X_test.reshape(10000, 784).astype('float')
    X_train /= 255
    X_test /= 255
    # 레이블 데이터를 0-9까지의 카테고리를 나타내는 배열로 변환하기 --- (※2a)
    y_train = np_utils.to_categorical(y_train, 10)
    y_test = np_utils.to_categorical(y_test, 10)

    # 모델 구조 정의하기 --- (※3)
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    # 모델 구축하기 --- (※4)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(),
        metrics=['accuracy'])


    # 데이터 훈련하기 --- (※5)
    hist = model.fit(X_train, y_train)


    # 테스트 데이터로 평가하기 --- (※6)
    score = model.evaluate(X_test, y_test, verbose=1)
    print('loss=', score[0])
    print('accuracy=', score[1])

    cdto.outdata['loss'] = score[0]
    cdto.outdata['accuracy'] = score[1]

    return cdto


def kerasBMI(cdto) :
    """
    TODO : 모듈을 읽어 들인다
    TODO : 데이터를 가공한다.
    TODO : 모델을 만든다
    TODO : 학습을 시킨다
    TODO : 예측을 한뒤 정답률을 구한다.
    :param cdto:
    :return: cdto
    """

    # TODO : 모듈을 읽어 들인다.
    from keras.models import Sequential
    from keras.layers.core import Dense, Dropout, Activation
    from keras.callbacks import EarlyStopping
    import pandas as pd, numpy as np

    # TODO :
    """
    데이터는 
    [
        [<키>/200,<몸무게>/100], # 이값들은 0.0 ~ 1.0 사이어야 되므로 정규화를 해야된다. 정규화를 하는 방법은 키는 200으로 몸무게는 100으로 나눈다
        [<키>/200,<몸무게>/100],
        [<키>/200,<몸무게>/100]
    ]
    레이블은
    [
        'thin',  -> 변환 [ 1, 0, 0 ]
        'normal',-> 변환 [ 0, 1, 0 ]
        'fat'    -> 변환 [ 0, 0, 1 ]
        ]
    """
    # BMI 데이터를 읽어 들이고 정규화하기 --- (※1)
    csv = pd.read_csv("./keras/bmi.csv")

    # 몸무게와 키 데이터를 가지고와서 정규화작업을 실시한다.
    csv["weight"] /= 100
    csv["height"] /= 200

    # csv에서 weight, height을 가지고 와서 이것 matrix로 변환하는 작업을 실시한다.
    X = csv[["weight", "height"]].as_matrix()  # --- (※1a)

    # 레이블
    bmi_class = {
        "thin": [1, 0, 0],
        "normal": [0, 1, 0],
        "fat": [0, 0, 1]
    }
    # 여기서 x는 입력값으로 표시하고 이때는 레이블을 y로 나타낸다.
    # 빈공간을 20000개 만들고 리스트가 3개 들어갈 수 있는 자리를 만든다.
    y = np.empty((20000, 3))
    """
    이 의미는
    [
        [0,0,0],
        [0,0,0],
        ...
        [0,0,0]
    ] 이런 형태로 데이타가 20000개 생성된다.
    """

    # csv에 있는 레이블을 튜플형태로 추출한다.
    for i, v in enumerate(csv["label"]):
        y[i] = bmi_class[v]
    print(y[0:3])
    """
    [[0. 0. 1.]
    [0. 0. 1.]
    [0. 1. 0.]]
    이런 형태의 데이타가 나오고 이것을 레이블로 이용한다.
    """

    # 이제 만들어진 데이터를 가지고와서 학습전용데이터와 테스트전용 데이타를 만든다.
    # 훈련 전용 데이터와 테스트 전용 데이터로 나누기 --- (※2)
    # X는 1부터 15000번째까지
    X_train, y_train = X[1:15001], y[1:15001]
    X_test, y_test = X[15001:20001], y[15001:20001]

    # 모델 구조 정의하기 --- (※3)
    model = Sequential()
    # 모델의 레이어를 만드는 작업을 한다.
    model.add(Dense(512, input_shape=(2,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.1))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    # 모델 구축하기 --- (※4)
    model.compile(
        loss='categorical_crossentropy',
        optimizer="rmsprop",
        metrics=['accuracy'])

    # 데이터 훈련하기 --- (※5)
    hist = model.fit(
        X_train, y_train,
        batch_size=100,
        nb_epoch=20,
        validation_split=0.1,
        callbacks=[EarlyStopping(monitor='val_loss', patience=2)],
        verbose=1)

    # 테스트 데이터로 평가하기 --- (※6)
    # score는 정답율을 의미한다.
    score = model.evaluate(X_test, y_test)
    print('loss=', score[0])
    print('accuracy=', score[1])

    cdto.outdata['loss'] = score[0]
    cdto.outdata['accuracy'] = score[1]

    return cdto


