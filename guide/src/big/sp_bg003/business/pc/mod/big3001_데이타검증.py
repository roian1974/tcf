import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg003.business.dc import dc_bg003

def BIG3001():
    rtn = True
    try:
        comlogging.logger.info( "BIG3001_start() start ")
        # ------------------------------------------------------------------------------------------------------------
        # 전처리된 입력파일에 대한 로딩작업을 진행한다.
        # ------------------------------------------------------------------------------------------------------------
        data = BIG3001_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG3001_processing() start ")

            tdata = BIG3001_processing(data)

        else :
            raise Exception('BIG3001_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG3001-'+ str(err))
        include.setErr('EBIG3001', 'BIG3001' + str(err))
    else:
        comlogging.logger.info( 'BIG3001-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG3001_end(tdata)

        if include.isError() == False :
            return True
        else :
            return False

#----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
#----------------------------------------------------------------------------------------------------------------------
def BIG3001_start() :
    try:
        comlogging.logger.info("STEP-01: 전처리된 데이타를 입력한다")
        comlogging.logger.info("   >> IN: C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv")
        infile = include.gcominfo['sysargv'][3]
        infile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv'
        outfile = infile + ".out"
        data = pd.read_csv(infile, encoding = "ISO-8859-1")
        print(data.head(1))
    except Exception as err:
        comlogging.logger.error( 'BIG3001_start-' + str(err))
        include.setErr('EBIG3001', 'BIG3001_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG3001_start-성공')
    finally:
        if include.isError() == False :
            return data
        else :
            return False

def BIG3001_processing(data) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))
        dc_bg003.데이터검증()
        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG3001_processing '+ str(err) )
        include.setErr('EBIG3001', 'BIG3001_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG3001_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG3001_end(tdata) :
    try:
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"


    except Exception as err:
        comlogging.logger.error( 'BIG3001_end '+ str(err))
        include.setErr('EBIG3001', 'BIG3001_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG3001_end-성공')
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
