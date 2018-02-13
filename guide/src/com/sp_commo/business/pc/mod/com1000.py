import time
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.sp_commo.business.dc import dc_commo



def COM1000():
    rtn = True
    try:
        comlogging.logger.info( "COM1000_start() start ")
        if COM1000_start() == True :
            comlogging.logger.info( "COM1000_processing() start ")
            COM1000_processing()
        else :
            raise Exception('COM1000_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'COM1000-'+ str(err))
        include.setErr('ECOM1000', 'COM1000' + str(err))
    else:
        comlogging.logger.info( 'COM1000-성공')
    finally:
        COM1000_end()

        if include.isError() == False :
            return True
        else :
            return False

def COM1000_start() :
    try:
        pass

    except Exception as err:
        comlogging.logger.error( 'COM1000_start-' + str(err))
        include.setErr('ECOM1000', 'COM1000_start,' + str(err))
    else:
        comlogging.logger.info( 'COM1000_start-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def COM1000_processing() :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))
        parameter = []
        rows = dc_commo.queryDocument("select_document_01", parameter)
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
        comlogging.logger.error( 'COM1000_processing '+ str(err) )
        include.setErr('ECOM1000', 'COM1000_processing,' + str(err))
    else:
        comlogging.logger.info( 'COM1000_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def COM1000_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'COM1000_end '+ str(err))
        include.setErr('ECOM1000', 'COM1000_end,' + str(err))
    else:
        comlogging.logger.info( 'COM1000_end-성공')
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
