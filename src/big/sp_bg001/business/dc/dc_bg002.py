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


def word2vecTest() :

    fp = codecs.open('2BEXXX01.txt','r', encoding='utf-8')
    soup = BeautifulSoup(fp, "html.parser")
    body = soup.select_one("text body")
    text = body.getText()

    print(text)
    twitter = Twitter()
    lines = text.split("\r\n")
    results = []
    for line in lines :
        r = []
        malist = twitter.pos(line, norm=True, stem=True)
        for( word, pumsa ) in malist :
            if not pumsa in  ['Josa','Eomi',"Punctuation"] :
                r.append(word)
        results.append( (" ".join(r)).strip())

    output = ( " ".join(results)).strip()
    print(output)
    with open("togi.wakati","w",encoding="utf-8") as fp:
        fp.write(output)

    data = word2vec.LineSentence("togi.wakati")
    model = word2vec.Word2Vec(data,size=200, window=10, hs=1, min_count=2, sg=1)
    model.save("togi.model")


def word2vecModelTest() :

    model = word2vec.Word2Vec.load("togi.model")
    model.most_similar(positive=['땅']) # 땅과 가장 유사한 단어


def 형태소분석() :
    print("---")
    twitter = Twitter()
    print("---1")
    print(twitter.morphs(u'단독입찰보다 복수입찰의 경우'))
    print(twitter.nouns(u'유일하게 항공기 체계 종합개발 경험을 갖고 있는 KAI는'))
    print(twitter.phrases(u'날카로운 분석과 신뢰감 있는 진행으로'))
    print(twitter.pos(u'이것도 되나욬ㅋㅋ'))
    print(twitter.pos(u'이것도 되나욬ㅋㅋ', norm=True))
    print(twitter.pos(u'이것도 되나욬ㅋㅋ', norm=True, stem=True))

def 워드디셔너리() :
    string = '몇|번|을|쓰러지다|몇|번|을|무너지다|다시|일어나다'

    # todo : 이 문자을 벡터로 어떻게 표현할까
    # 먼저 워드디셔너리를 만든다.

    # word_dictionary {
    #     "몇" : 1
    #     "번" : 2
    #     "을" : 3
    #     "쓰러지다" : 4
    #     "무너지다" : 5
    #     "다시" : 6
    #     "일어나다" : 7
    #  }
    # 몇은 2번 반복, ,..
    # data
    # [2, 2, 2, 1, 1, 1]
    #
    # 이렇게 해서 벡터화 시킨다.
    #
    # 이런 벡터화 된 정보를 모델에 활용되는데
    #
    # 예를들어보면
    #
    # model.fit(X_train, Y_train)
    # 이 모델의 fit 메소드의 파라미터로 사용된다는 것이다.
    # 여기서
    # X_train은 단어의 출현도를
    # Y_train은 카테고리를 입력한다.






