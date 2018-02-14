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
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg002.business.dc import dc_bg002


# • Pandas - 데이터 가공
# • CounterVectorizer - NLP
# • LogisticRegression - 예측모델을 학습하고 테스트

# python tcf_sp_bg01.py sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv LogisR [NaiveEyes,RF,SVMGusian,SVMLinear] 20150101

def BIG2001():
    rtn = True
    try:
        comlogging.logger.info( "BIG2001_start() start ")
        # ------------------------------------------------------------------------------------------------------------
        # 전처리된 입력파일에 대한 로딩작업을 진행한다.
        # ------------------------------------------------------------------------------------------------------------
        filename,modelType, baseDate, ftype = BIG2001_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG2001_processing() start ")

            #--------------------------------------------------------------------------------------------------------
            # 훈련데이타 와 데이타 데이터를 준비하는 과정을 거친다.
            #   > 데이타를 소문자로 치환하는 작업을 처리한다.
            #   > 문장을 읽어서 단어별로 리스트를 작성하고 단어별 빈도수를 작업한다.
            # --------------------------------------------------------------------------------------------------------
            tdata = BIG2001_processing(filename, modelType, baseDate, ftype)

        else :
            raise Exception('BIG2001_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG2001-'+ str(err))
        include.setErr('EBIG2001', 'BIG2001' + str(err))
    else:
        comlogging.logger.info( 'BIG2001-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG2001_end(tdata)

        if include.isError() == False :
            return True
        else :
            return False

#----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
#----------------------------------------------------------------------------------------------------------------------
def BIG2001_start() :
    try:

        # sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\쌍용건설_dataset.csv LogisR 20050628 KO
        comlogging.logger.info("STEP-01: 전처리된 데이타를 입력한다")
        comlogging.logger.info("   >> IN: C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv")
        infile = include.gcominfo['sysargv'][3]
        # infile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv'
        modelType = include.gcominfo['sysargv'][4]
        baseDate = include.gcominfo['sysargv'][5]
        if len( include.gcominfo['sysargv'] ) == 7 :
            ftype = include.gcominfo['sysargv'][6]
        else :
            ftype = 'EN'

    except Exception as err:
        comlogging.logger.error( 'BIG2001_start-' + str(err))
        include.setErr('EBIG2001', 'BIG2001_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG2001_start-성공')
    finally:
        if include.isError() == False :
            return infile, modelType, baseDate, ftype
        else :
            return False

def BIG2001_processing(infile,modelType,baseDate,ftype) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        comlogging.logger.info('• 1. 훈련데이타와 테스트 데이터를 준비한다.')
        train, headlines = dc_bg002.preAnalysis(infile,baseDate,"<",ftype) # < 20150101
        if headlines  != True :
            comlogging.logger.info('• 2. 모델 훈련과 모델을 생성한다.')
            dc_bg002.trainModel(modelType, train, headlines)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG2001_processing '+ str(err) )
        include.setErr('EBIG2001', 'BIG2001_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG2001_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG2001_end(tdata) :
    try:
        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        outfile = include.gcominfo['sysargv'][4]
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"
        comutil.file_append( outfile, str(tdata) )


    except Exception as err:
        comlogging.logger.error( 'BIG2001_end '+ str(err))
        include.setErr('EBIG2001', 'BIG2001_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG2001_end-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False

#-----------------------------------------------------------------------------------------------------------------------

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())
