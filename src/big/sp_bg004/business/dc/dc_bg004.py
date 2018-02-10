import pandas as pd
import time
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.info import include
from src.big.sp_bg004.business.dc.dao import queryDAO
from src.big.sp_bg004.business.dc.mod import logisticregression, naviebayes, randomforest, svmgausian, svmlinear
#-----------------------------------------------------------------------------------------------------------------------
# 개요 : 기사의 헤더라인과 주가상승레이블을 가지고 주가를 예츨하는 모델링 작업이다
# 기사내용
#       =============================================================
#       일자      label 기사헤더라인1, 기사헤더라인2, 기사헤어라인3 ....
#       =============================================================
#       20180101    0   A 'hindrance to operations': extracts from the leaked reports .....
#-----------------------------------------------------------------------------------------------------------------------
def preAnalysis(filename,baseDate,my,ftype) :
    try:
        rtn = True

        # CSV 파일을 읽는다.
        comlogging.logger.info('• 1. Saving CSV File.')
        if ftype == "KO" :
            data = pd.read_csv(filename, engine = "python")
        else:
            data = pd.read_csv(filename, encoding = "ISO-8859-1")
        # print(data.head(1))

        # 테스트 데이타와 훈련데이타를 나누어 준다
        # train = data[data['Date'] < '20150101']
        # test = data[data['Date'] > '20141231']
        if my == "<" :
            print("<",baseDate)
            train = data[data['Date'] < baseDate ]
        elif my == ">" :
            print(">", baseDate)
            train = data[data['Date'] > baseDate]

        # print('---',train)

        # 쓸데없는 문자를 없앤다
        # * @ # $ % ^ & * ( ) _- + 등의 문자를 삭제한다.  문자는 A-Z a-z까지만 허용한다.
        comlogging.logger.info('• 2. Removing punctuations.')
        slicedData = train.iloc[:, 2:3] # tail.iloc[ 행, 열]
        # slicedData.replace(to_replace="[^a-zA-Z]", value=" ", regex=True, inplace=True)

        comlogging.logger.info('• 3. Renaming column names for ease of access')
        list1 = [i for i in range(1)]  # 1 개의 리스트를 생성한다.
        new_Index = [str(i) for i in list1]

        # slicedData.columns - sliceData[:,2:27] 이므로 2컬럼부터 26컬럼까지의 정보이다.
        slicedData.columns = new_Index
        # print( slicedData.head(5) )

        comlogging.logger.info('• 4. Convertng headlines to lower case')
        for index in new_Index:
            slicedData[index] = slicedData[index].str.lower()
        # slicedData.head(1)

        headlines = []
        for row in range(0, len(slicedData.index)):
            headlines.append(' '.join(str(x) for x in slicedData.iloc[row, 0:25]))

        # 결과데이타는 일자별로의 헤어라인을 특수문자등을 없애고 소문자화 해서 가지고 오는 것이 preAnaly 분석과정이다.
        # cnt=0
        # for rd in headlines :
        #     cnt+=1
        #     print(cnt,rd)

    except Exception as err:
        comlogging.logger.error('▲preAnalysis()-ERR:'+ str(err))
        include.setErr('EBIG005', 'preAnalysis 분석에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲preAnalysis()-성공:')
    finally:
        if rtn == True :
            return train, headlines
        else :
            return False


def trainModel(modelType, train, headlines) :
    try:
        rtn = True
        if modelType == "LogisR" :
            logisticregression.train(modelType, train, headlines)
        elif modelType == "NaiveEyes" :
            naviebayes.train(modelType, train, headlines)
        elif modelType == "RF":
            randomforest.train(modelType, train, headlines)
        elif modelType == "SVMGusian":
            svmgausian.train(modelType, train, headlines)
        elif modelType == "SVMLinear":
            svmlinear.train(modelType, train, headlines)
        else :
            pass

    except Exception as err:
        comlogging.logger.error('▲exeModel()-ERR:'+ str(err))
        include.setErr('EBIG005', 'exeModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲exeModel()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False

def testModel(modelType, train, headlines) :
    try:
        rtn = True
        if modelType == "LogisR" :
            logisticregression.test(modelType, train, headlines)
        elif modelType == "NaiveEyes" :
            naviebayes.test(modelType, train, headlines)
        elif modelType == "RF":
            randomforest.test(modelType, train, headlines)
        elif modelType == "SVMGusian":
            svmgausian.test(modelType, train, headlines)
        elif modelType == "SVMLinear":
            svmlinear.test(modelType, train, headlines)
        else :
            pass

    except Exception as err:
        comlogging.logger.error('▲exeModel()-ERR:'+ str(err))
        include.setErr('EBIG005', 'exeModel 수행 에러' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲exeModel()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False


def queryDocument(sql_id, parameter) :
    try:
        rtn = True
        rows = queryDAO.queryDocument(sql_id, parameter)
        if rows == False:
            comlogging.logger.error(sql_id + 'fetch error')
        else:
            if len(rows) == 0:
                rtn = 1403
                raise Exception('Data Not Found')
    except Exception as err:
        comlogging.logger.error('▲queryDocument()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲queryDocument()-성공:')
    finally:
        if rtn == True :
            return rows
        elif rtn == 1403 or rtn == False :
            return rtn
        else :
            return False

def upsertDocument(sql_id, parameter,tup) :
    try:
        rtn = True
        if queryDAO.upsertDocument(sql_id, parameter, tup) == True:
            print('insert insert_doc_sentiment_01- doc_sentiment success')
        else:
            rtn = False
            raise Exception('upsertDocument error')
    except Exception as err:
        comlogging.logger.error('▲queryDocument()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲queryDocument()-성공:')
    finally:
        return rtn
