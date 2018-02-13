import time
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg900.business.dc import dc_bg900


def BIG9002():
    rtn = True
    try:
        comlogging.logger.info( "BIG9002_start() start ")
        if BIG9002_start() == True :
            comlogging.logger.info( "BIG9002_processing() start ")
            BIG9002_processing()
        else :
            raise Exception('BIG9002_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'BIG9002-'+ str(err))
        include.setErr('EBIG9002', 'BIG9002' + str(err))
    else:
        comlogging.logger.info( 'BIG9002-성공')
    finally:
        BIG9002_end()

        if include.isError() == False :
            return True
        else :
            return False

def BIG9002_start() :
    try:
        pass

    except Exception as err:
        comlogging.logger.error( 'BIG9002_start-' + str(err))
        include.setErr('EBIG9002', 'BIG9002_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG9002_start-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG9002_processing() :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        dc_bg900.이벤트후보군데이터추출()

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG9002_processing '+ str(err) )
        include.setErr('EBIG9002', 'BIG9002_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG9002_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG9002_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG9002_end '+ str(err))
        include.setErr('EBIG9002', 'BIG9002_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG9002_end-성공')
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
