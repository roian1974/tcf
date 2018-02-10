import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg800.business.dc import dc_bg801
from src.big.sp_bg800.transfer import big8001cdto



# • Pandas - 데이터 가공
# • CounterVectorizer - NLP
# • LogisticRegression - 예측모델을 학습하고 테스트

# python tcf_sp_bg001.py sp_bg800 BIG8001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv LogisR [NaiveEyes,RF,SVMGusian,SVMLinear] 20150101 KO

def BIG8001():
    rtn = True
    try:
        comlogging.logger.info( "BIG8001_start() start ")
        _big8001cdto = BIG8001_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG8001_processing() start ")

            tdata = BIG8001_processing(_big8001cdto)

        else :
            raise Exception('BIG8001_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG8001-'+ str(err))
        include.setErr('EBIG8001', 'BIG8001' + str(err))
    else:
        comlogging.logger.info( 'BIG8001-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG8001_end(tdata)

        if include.isError() == False :
            return True
        else :
            return False

#----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
#----------------------------------------------------------------------------------------------------------------------
def BIG8001_start() :
    try:
        _big8001cdto = include.gcominfo['sysargv'][3]

    except Exception as err:
        comlogging.logger.error( 'BIG8001_start-' + str(err))
        include.setErr('EBIG8001', 'BIG8001_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG8001_start-성공')
    finally:
        if include.isError() == False :
            return _big8001cdto
        else :
            return False

def BIG8001_processing(pbig8001cdto) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        pbig8001cdto = dc_bg801.preAnalysis(pbig8001cdto)
        if pbig8001cdto  != True :
            dc_bg801.analysisFeature(pbig8001cdto)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG8001_processing '+ str(err) )
        include.setErr('EBIG8001', 'BIG8001_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG8001_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG8001_end(tdata) :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG8001_end '+ str(err))
        include.setErr('EBIG8001', 'BIG8001_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG8001_end-성공')
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
