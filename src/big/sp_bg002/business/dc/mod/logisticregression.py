import pandas as pd
import pickle
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include



# CountVectorizer는 단어의 개수를 세어서 단어-문서간의 행렬을 만들어 준다.
# 형태소란 의미가 있는 가장작은 말의단위 ... 드세요
# 데이타의 특징을 feature라한다.

def train(modelType, train, trainheadlines) :
    try:
        rtn = True
        comlogging.logger.info("    • Training 1 단계-클러스터링-CountVectorizer:단어의 빈도수를 조사하기위한 fitting작업을 한다.")

        basicvectorizer = CountVectorizer(ngram_range=(1,1))
        basictrain = basicvectorizer.fit_transform(trainheadlines)
        print(basictrain.shape)

        comlogging.logger.info("    • Training 2 단계-로지스틱회귀분석 모델 적용")
        basicmodel = LogisticRegression()
        basicmodel = basicmodel.fit(basictrain, train["Label"])     # train["Label"] 데이타는 일자별로 전날 주가에 대해 기의 헤더라인을 읽고 강제로 1이면 긍정, 0 이면 부정인 값을 넣어준데이타를 말한다.

        comlogging.logger.info("    • Training 3 단계-로지스틱회귀분석 모델를 파일로 저장")
        moutfile="C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "mod.logistic." + comutil.getsysdate()
        voutfile = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "vec.logistic." + comutil.getsysdate()
        with open(moutfile, 'wb') as f:
            pickle.dump(basicmodel, f)

        with open(voutfile, 'wb') as f:
            pickle.dump(basicvectorizer, f)

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return True
        else :
            return False

def test(modelType, train, trainheadlines) :
    try:
        rtn = True

        comlogging.logger.info("    • Training 3 단계-테스트데이터를 적용해 본다.")

        moutfile="C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "mod.logistic." + comutil.getsysdate()
        voutfile = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\\" + "vec.logistic." + comutil.getsysdate()

        with open(moutfile, 'rb') as f:
            testmodel = pickle.load( f )

        with open(voutfile, 'rb') as f:
            testvector = pickle.load( f )

        testvectorizer = testvector
        basictest = testvectorizer.transform(trainheadlines)
        predictions = testmodel.predict(basictest)

        out = pd.crosstab(train["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])
        comlogging.logger.info( "\n===========================\n" + str(out) )
        out = pd.crosstab(train["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])

        total = out[0][0] + out[0][1] + out[1][0] + out[1][1]
        accuracy =  ( out[0][0]+ out[1][1] ) / total
        comlogging.logger.info("accuracy:" + str(accuracy))

        # include.setOutdata(out)

        basicwords = testvectorizer.get_feature_names()
        basiccoeffs = testmodel.coef_.tolist()[0]
        coeffdf = pd.DataFrame({'Word': basicwords, 'Coefficient': basiccoeffs})
        coeffdf = coeffdf.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
        out = coeffdf.head(10)
        comlogging.logger.info("\n===========================\n" +str(out))
        out = coeffdf.tail(10)
        comlogging.logger.info("\n===========================\n" + str(out))

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'execute' + str(err))
    else:
        comlogging.logger.info( 'execute-성공-')
    finally:
        if rtn == True :
            return out
        else :
            return False

