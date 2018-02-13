import time
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg001.business.dc import dc_bg001
from src.big.sp_bg001.transfer import bg1000cdto
from sklearn import svm, metrics


def BIG1000():
    rtn = True
    try:
        comlogging.logger.info( "BIG1000_start() start ")
        bg1000cdto = BIG1000_start()
        if bg1000cdto != False :
            comlogging.logger.info( "BIG1000_processing() start ")
            BIG1000_processing(bg1000cdto)
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
        bg1000cdto = include.gcominfo['sysargv'][3]
    except Exception as err:
        comlogging.logger.error( 'BIG1000_start-' + str(err))
        include.setErr('EBIG1000', 'BIG1000_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG1000_start-성공')
    finally:
        if include.isError() == False :
            return bg1000cdto
        else :
            return False

def BIG1000_processing(bg1000cdto) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        if bg1000cdto.domain_function == "xorPredict" :
            dc_bg001.xorPredit(bg1000cdto)
        elif bg1000cdto.domain_function == "flowerPredit" :
            dc_bg001.flowerPredit(bg1000cdto)
        elif bg1000cdto.domain_function == "handTypeModel" :
            dc_bg001.handTypeModel(bg1000cdto)
        elif bg1000cdto.domain_function == "miniDownload":
            dc_bg001.miniDownload(bg1000cdto)
        elif bg1000cdto.domain_function == "toCSV":
            dc_bg001.toCSV(bg1000cdto)
        elif bg1000cdto.domain_function == "catchLANG":
            dc_bg001.catchLANG(bg1000cdto)

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
