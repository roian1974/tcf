import time
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.sp_commo.business.dc import dc_commo

# document 테이블을 읽어서 영문번역

def COM1005():
    rtn = True
    try:
        comlogging.logger.info( "COM1005_start() start ")
        if COM1005_start() == True :
            comlogging.logger.info( "COM1005_processing() start ")
            COM1005_processing()
        else :
            raise Exception('COM1005_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'COM1005-'+ str(err))
        include.setErr('ECOM1005', 'COM1005' + str(err))
    else:
        comlogging.logger.info( 'COM1005-성공')
    finally:
        COM1005_end()

        if include.isError() == False :
            return True
        else :
            return False

def COM1005_start() :
    try:
        pass

    except Exception as err:
        comlogging.logger.error( 'COM1005_start-' + str(err))
        include.setErr('ECOM1005', 'COM1005_start,' + str(err))
    else:
        comlogging.logger.info( 'COM1005_start-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def COM1005_processing() :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))
        while True :
            parameter = ['20180118']
            rows = dc_commo.queryDocument("select_document_05", parameter)
            outdata = []
            if rows == False or rows == 1403:
                comlogging.logger.error('select_document_05')
                break
            else:
                comlogging.logger.info('(' + str(rows) +  ')')
                if len(rows) == 0:
                    comlogging.logger.info('data not found')
                    break
                print(rows)
        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'COM1005_processing '+ str(err) )
        include.setErr('ECOM1005', 'COM1005_processing,' + str(err))
    else:
        comlogging.logger.info( 'COM1005_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def COM1005_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'COM1005_end '+ str(err))
        include.setErr('ECOM1005', 'COM1005_end,' + str(err))
    else:
        comlogging.logger.info( 'COM1005_end-성공')
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
