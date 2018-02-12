import pandas as pd
import numpy as np
from src.com.fwk.business.util.logging import comlogging
from gensim.models import word2vec
import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter

import matplotlib.pyplot as plt
import seaborn as sns

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

    word_dictionary {
        "몇" : 1
        "번" : 2
        "을" : 3
        "쓰러지다" : 4
        "무너지다" : 5
        "다시" : 6
        "일어나다" : 7
     }
    # 몇은 2번 반복, ,..
    data
    [2, 2, 2, 1, 1, 1]

    이렇게 해서 벡터화 시킨다.

    이런 벡터화 된 정보를 모델에 활용되는데

    예를들어보면

    model.fit(X_train, Y_train)
    이 모델의 fit 메소드의 파라미터로 사용된다는 것이다.
    여기서
    X_train은 단어의 출현도를
    Y_train은 카테고리를 입력한다.






