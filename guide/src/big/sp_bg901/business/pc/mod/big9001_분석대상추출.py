import time
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg900.business.dc import dc_bg900

def BIG9001():
    rtn = True
    try:
        comlogging.logger.info( "BIG9001_start() start ")
        if BIG9001_start() == True :
            comlogging.logger.info( "BIG9001_processing() start ")
            BIG9001_processing()
        else :
            raise Exception('BIG9001_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'BIG9001-'+ str(err))
        include.setErr('EBIG9001', 'BIG9001' + str(err))
    else:
        comlogging.logger.info( 'BIG9001-성공')
    finally:
        BIG9001_end()

        if include.isError() == False :
            return True
        else :
            return False

def BIG9001_start() :
    try:

        pass

    except Exception as err:
        comlogging.logger.error( 'BIG9001_start-' + str(err))
        include.setErr('EBIG9001', 'BIG9001_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG9001_start-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG9001_processing() :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        dc_bg900.분석대상추출()

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG9001_processing '+ str(err) )
        include.setErr('EBIG9001', 'BIG9001_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG9001_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG9001_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG9001_end '+ str(err))
        include.setErr('EBIG9001', 'BIG9001_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG9001_end-성공')
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
