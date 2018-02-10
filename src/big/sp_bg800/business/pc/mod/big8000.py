import time
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg800.business.dc import dc_bg801


# 전처리 단계


def BIG8000():
    rtn = True
    try:
        comlogging.logger.info( "BIG8000_start() start ")
        if BIG8000_start() == True :
            comlogging.logger.info( "BIG8000_processing() start ")
            BIG8000_processing()
        else :
            raise Exception('BIG8000_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'BIG8000-'+ str(err))
        include.setErr('EBIG8000', 'BIG8000' + str(err))
    else:
        comlogging.logger.info( 'BIG8000-성공')
    finally:
        BIG8000_end()

        if include.isError() == False :
            return True
        else :
            return False

def BIG8000_start() :
    try:


        pass

    except Exception as err:
        comlogging.logger.error( 'BIG8000_start-' + str(err))
        include.setErr('EBIG8000', 'BIG8000_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG8000_start-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG8000_processing() :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))
        parameter = []
        rows = dc_bg801.queryDocument("select_document_01", parameter)
        outdata = []
        if rows == False or rows == 1403:
            comlogging.logger.error('select_document_01')
            outdata.append(['data not found'])
        else:
            comlogging.logger.info('(' + str(rows) +  ')')
            outdata.append(rows)
            if len(rows) == 0:
                comlogging.logger.info('data not found')

        include.setOutdata(outdata)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG8000_processing '+ str(err) )
        include.setErr('EBIG8000', 'BIG8000_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG8000_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG8000_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG8000_end '+ str(err))
        include.setErr('EBIG8000', 'BIG8000_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG8000_end-성공')
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
