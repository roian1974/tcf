import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg003.business.dc import dc_bg003

def BIG3002():
    rtn = True
    try:
        comlogging.logger.info( "BIG3002_start() start ")
        # ------------------------------------------------------------------------------------------------------------
        # 전처리된 입력파일에 대한 로딩작업을 진행한다.
        # ------------------------------------------------------------------------------------------------------------
        data = BIG3002_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG3002_processing() start ")

            tdata = BIG3002_processing(data)

        else :
            raise Exception('BIG3002_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG3002-'+ str(err))
        include.setErr('EBIG3002', 'BIG3002' + str(err))
    else:
        comlogging.logger.info( 'BIG3002-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG3002_end(tdata)

        if include.isError() == False :
            return True
        else :
            return False

#----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
#----------------------------------------------------------------------------------------------------------------------
def BIG3002_start() :
    try:

        dc_bg003.전처리()

    except Exception as err:
        comlogging.logger.error( 'BIG3002_start-' + str(err))
        include.setErr('EBIG3002', 'BIG3002_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG3002_start-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG3002_processing(data) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        dc_bg003.전처리()

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG3002_processing '+ str(err) )
        include.setErr('EBIG3002', 'BIG3002_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG3002_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG3002_end(tdata) :
    try:
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"


    except Exception as err:
        comlogging.logger.error( 'BIG3002_end '+ str(err))
        include.setErr('EBIG3002', 'BIG3002_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG3002_end-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())
