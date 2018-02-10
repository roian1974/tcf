import time
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg001.business.dc import dc_bg001


# 전처리 단계


def BIG1000():
    rtn = True
    try:
        comlogging.logger.info( "BIG1000_start() start ")
        if BIG1000_start() == True :
            comlogging.logger.info( "BIG1000_processing() start ")
            BIG1000_processing()
        else :
            raise Exception('BIG1000_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'BIG1000-'+ str(err))
        include.setErr('EBIG1000', 'BIG1000' + str(err))
    else:
        comlogging.logger.info( 'BIG1000-성공')
    finally:
        BIG1000_end()

        if include.isError() == False :
            return True
        else :
            return False

def BIG1000_start() :
    try:
        pass

    except Exception as err:
        comlogging.logger.error( 'BIG1000_start-' + str(err))
        include.setErr('EBIG1000', 'BIG1000_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG1000_start-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG1000_processing() :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))
        dc_bg001.measurePCA()
        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG1000_processing '+ str(err) )
        include.setErr('EBIG1000', 'BIG1000_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG1000_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG1000_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG1000_end '+ str(err))
        include.setErr('EBIG1000', 'BIG1000_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG1000_end-성공')
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
