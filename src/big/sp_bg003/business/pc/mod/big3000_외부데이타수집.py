import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg003.business.dc import dc_bg003

def BIG3000():
    rtn = True
    try:
        comlogging.logger.info( "BIG3000_start() start ")
        data = BIG3000_start()

        if include.isError() == False:
            comlogging.logger.info( "BIG3000_processing() start ")
            tdata = BIG3000_processing(data)
        else :
            raise Exception('BIG3000_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG3000-'+ str(err))
        include.setErr('EBIG3000', 'BIG3000' + str(err))
    else:
        comlogging.logger.info( 'BIG3000-성공')
    finally:
        BIG3000_end(tdata)
        if include.isError() == False :
            return True
        else :
            return False

def BIG3000_start() :
    try:
        data = []

        dc_bg003.외부데이터수집()

        pass
    except Exception as err:
        comlogging.logger.error( 'BIG3000_start-' + str(err))
        include.setErr('EBIG3000', 'BIG3000_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG3000_start-성공')
    finally:
        if include.isError() == False :
            return data
        else :
            return False

def BIG3000_processing(data) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        dc_bg003.외부데이터수집()

    except Exception as err:
        comlogging.logger.error( 'BIG3000_processing '+ str(err) )
        include.setErr('EBIG3000', 'BIG3000_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG3000_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG3000_end(tdata) :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG3000_end '+ str(err))
        include.setErr('EBIG3000', 'BIG3000_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG3000_end-성공')
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
