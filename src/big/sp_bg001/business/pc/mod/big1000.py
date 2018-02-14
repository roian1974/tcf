import time
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg001.business.dc import dc_bg001

def BIG1000():
    rtn = True
    try:
        comlogging.logger.info("BIG1000_start() start ")
        cdto = BIG1000_start()

        if include.isError() == False:
            comlogging.logger.info("BIG1000_processing() start ")
            cdto = BIG1000_processing(cdto)
        else:
            raise Exception('BIG1000_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error('BIG1000-' + str(err))
        include.setErr('EBIG1000', 'BIG1000' + str(err))
    else:
        comlogging.logger.info('BIG1000-성공')
    finally:

        BIG1000_end(cdto)

        if include.isError() == False:
            return True
        else:
            return False


def BIG1000_start():
    try:
        big1000cdto = include.gcominfo['sysargv'][3]
    except Exception as err:
        comlogging.logger.error('BIG1000_start-' + str(err))
        include.setErr('EBIG1000', 'BIG1000_start,' + str(err))
    else:
        comlogging.logger.info('BIG1000_start-성공')
    finally:
        if include.isError() == False:
            return big1000cdto
        else:
            return False


def BIG1000_processing(cdto):
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        cdto = dc_bg001.preAnalysis_XOR(cdto)
        if cdto  != True :
            cdto = dc_bg001.trainModel_XOR(cdto)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error('BIG1000_processing ' + str(err))
        include.setErr('EBIG1000', 'BIG1000_processing,' + str(err))
    else:
        comlogging.logger.info('BIG1000_processing-성공')
    finally:
        if include.isError() == False:
            return cdto
        else:
            return False


def BIG1000_end(cdto):
    try:
        include.gcominfo['outdata'].append(cdto)

    except Exception as err:
        comlogging.logger.error('BIG1000_end ' + str(err))
        include.setErr('EBIG1000', 'BIG1000_end,' + str(err))
    else:
        comlogging.logger.info('BIG1000_end-성공')
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
