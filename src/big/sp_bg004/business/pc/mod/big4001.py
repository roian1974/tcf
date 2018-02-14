import time

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg004.business.dc import dc_bg005
from src.big.sp_bg004.transfer.big4000cdto import BIG4000CDTO

def BIG4001():
    rtn = True
    try:
        comlogging.logger.info( "BIG4001_start() start ")
        big4000cdto = BIG4001_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG4001_processing() start ")

            cdto = BIG4001_processing(big4000cdto)

        else :
            raise Exception('BIG4001_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG4001-'+ str(err))
        include.setErr('EBIG4001', 'BIG4001' + str(err))
    else:
        comlogging.logger.info( 'BIG4001-성공')
    finally:

        BIG4001_end(cdto)

        if include.isError() == False :
            return True
        else :
            return False

def BIG4001_start() :
    try:
        big4000cdto = include.gcominfo['sysargv'][3]

    except Exception as err:
        comlogging.logger.error( 'BIG4001_start-' + str(err))
        include.setErr('EBIG4001', 'BIG4001_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG4001_start-성공')
    finally:
        if include.isError() == False :
            return big4000cdto
        else :
            return False

def BIG4001_processing(big4000cdto) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        domain_function = big4000cdto.indata['domain_function']
        big4000cdto = dc_bg005.preAnalysis(big4000cdto)

        if big4000cdto  != True :
            if domain_function == "trainModel" :
                dc_bg005.trainModel(big4000cdto)
            elif domain_function == "testModel" :
                dc_bg005.trainModel(big4000cdto)


        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG4001_processing '+ str(err) )
        include.setErr('EBIG4001', 'BIG4001_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG4001_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG4001_end(cdto) :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG4001_end '+ str(err))
        include.setErr('EBIG4001', 'BIG4001_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG4001_end-성공')
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
