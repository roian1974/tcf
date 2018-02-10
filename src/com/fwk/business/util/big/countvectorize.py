import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def cvtst() :
    print("==========================")
    basicvectorizer1 = CountVectorizer(min_df=1)
    content = ['How to format my hard disk', 'how disk format problems']
    X = basicvectorizer1.fit_transform(content)
    basicvectorizer1.get_feature_names()
    print(X.toarray().transpose())
    print("==========================")


def cvtst2():
    text = ['안녕 세상','사과 맛있다']
    cv = CountVectorizer()   # 일반적으로 공백으로 나눈다. 하지만 한글은 형태소 처리가 필요하다.
    tdm = cv.fit_transform(text)

    print(tdm)

    data= cv.get_feature_names()
    print(data)

def cvst3() :
    # https://datascienceschool.net/view-notebook/3e7aadbf88ed4f0d87a76f9ddc925d69/
    from sklearn.feature_extraction import DictVectorizer
    v = DictVectorizer(sparse=False)
    D = [{'A': 1, 'B': 2}, {'B': 3, 'C': 1}]
    X = v.fit_transform(D)
    print(X)
    a=v.get_feature_names()
    print(a)
    t=v.inverse_transform(X)
    print(t)

    from sklearn.feature_extraction.text import CountVectorizer
    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
        'The last document?',
    ]
    vect = CountVectorizer()
    vect.fit(corpus)
    aa=vect.vocabulary_
    print(aa)

    vect.transform(['This is the second document.']).toarray()
    vect.transform(['Something completely new.']).toarray()
    vect.transform(corpus).toarray()



cvst3()

