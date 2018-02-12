# INPUT - Combined_News_DJIA.csv
# OUTPUT - TEXT Preprocessing
#           - 형태소 분리(왓슨의 경우는 senmentic role통해) 및 조사제거 -> 불용어 처리(filter):도메인과 관련없는 단어제거 ->
#           - 절차
#              train.iloc :
#               대문자를 소문자로 변경하는 plain text 화 시킨다.
#
#               단어별 빈도수를 작성한다.
#
#   BASIC MODEL TRAINING AND TESTING : 모델(로직스틱회귀분석모델)을 위한 학습 데이타 준비
#    -

import time
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil


# • Pandas - 데이터 가공
# • CounterVectorizer - NLP
# • LogisticRegression - 예측모델을 학습하고 테스트


def BIG1003():
    rtn = True
    try:
        comlogging.logger.info("BIG1003_start() start ")
        # ------------------------------------------------------------------------------------------------------------
        # 전처리된 입력파일에 대한 로딩작업을 진행한다.
        # ------------------------------------------------------------------------------------------------------------
        data = BIG1003_start()

        if include.isError() == False:

            comlogging.logger.info("BIG1003_processing() start ")

            # --------------------------------------------------------------------------------------------------------
            # 훈련데이타 와 데이타 데이터를 준비하는 과정을 거친다.
            #   > 데이타를 소문자로 치환하는 작업을 처리한다.
            #   > 문장을 읽어서 단어별로 리스트를 작성하고 단어별 빈도수를 작업한다.
            # --------------------------------------------------------------------------------------------------------
            tdata = BIG1003_processing(data)

        else:
            raise Exception('BIG1003_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error('BIG1003-' + str(err))
        include.setErr('EBIG1003', 'BIG1003' + str(err))
    else:
        comlogging.logger.info('BIG1003-성공')
    finally:

        # ------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG1003_end(tdata)

        if include.isError() == False:
            return True
        else:
            return False


# ----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
# ----------------------------------------------------------------------------------------------------------------------
def BIG1003_start():
    try:
        comlogging.logger.info("STEP-01: 전처리된 데이타를 입력한다")
        comlogging.logger.info("   >> IN: C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Combined_News_DJIA.csv")
        infile = include.gcominfo['sysargv'][3]
        infile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Combined_News_DJIA.csv'
        outfile = infile + ".out"
        data = pd.read_csv(infile)
        print("==========data head========")
        print(data.head())
    except Exception as err:
        comlogging.logger.error('BIG1003_start-' + str(err))
        include.setErr('EBIG1003', 'BIG1003_start,' + str(err))
    else:
        comlogging.logger.info('BIG1003_start-성공')
    finally:
        if include.isError() == False:
            return data
        else:
            return False


def BIG1003_processing(data):
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))
        comlogging.logger.info('• Basic Model Training and Testing..')
        comlogging.logger.info("    Training 1 단계-???")

        train = data[data['Date'] < '2015-01-01']
        test = data[data['Date'] > '2014-12-31']

        trainheadlines = []
        for row in range(0, len(train.index)):
            trainheadlines.append(' '.join(str(x) for x in train.iloc[row, 2:27]))
        comlogging.logger.info(trainheadlines)

        comlogging.logger.info("    Training 2 단계-CountVectorizer")
        basicvectorizer = CountVectorizer()
        basictrain = basicvectorizer.fit_transform(trainheadlines)
        print(basictrain.shape)

        comlogging.logger.info("    Training 3 단계-로지스틱회귀분석 모델 적용")
        basicmodel = LogisticRegression()
        basicmodel = basicmodel.fit(basictrain, train["Label"])

        comlogging.logger.info("    Training 4 단계-???")
        testheadlines = []
        for row in range(0, len(test.index)):
            testheadlines.append(' '.join(str(x) for x in test.iloc[row, 2:27]))
        basictest = basicvectorizer.transform(testheadlines)

        predictions = basicmodel.predict(basictest)

        out = pd.crosstab(test["Label"], predictions, rownames=["Actual"], colnames=["Predicted"])
        print(out)

        comlogging.logger.info("    Training 5 단계-???")
        # coefficient

        basicwords = basicvectorizer.get_feature_names()
        basiccoeffs = basicmodel.coef_.tolist()[0]
        coeffdf = pd.DataFrame({'Word': basicwords,
                                'Coefficient': basiccoeffs})
        coeffdf = coeffdf.sort_values(['Coefficient', 'Word'], ascending=[0, 1])
        out = coeffdf.head(10)
        print(out)

        out = coeffdf.tail(10)
        print(out)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error('BIG1003_processing ' + str(err))
        include.setErr('EBIG1003', 'BIG1003_processing,' + str(err))
    else:
        comlogging.logger.info('BIG1003_processing-성공')
    finally:
        if include.isError() == False:
            return True
        else:
            return False


def BIG1003_end(tdata):
    try:
        # ------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        outfile = include.gcominfo['sysargv'][4]
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"
        comutil.file_append(outfile, str(tdata))


    except Exception as err:
        comlogging.logger.error('BIG1003_end ' + str(err))
        include.setErr('EBIG1003', 'BIG1003_end,' + str(err))
    else:
        comlogging.logger.info('BIG1003_end-성공')
    finally:

        if include.isError() == False:
            return True
        else:
            return False


# -----------------------------------------------------------------------------------------------------------------------

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday, t3.tm_hour, t3.tm_min, t3.tm_sec)


def getIntTime():
    return time.mktime(time.localtime())
