import time

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg004.business.dc import dc_bg004
from src.big.sp_bg004.transfer.big4000cdto import BIG4000CDTO



def BIG4000():
    rtn = True
    try:
        comlogging.logger.info( "BIG4000_start() start ")
        big4000cdto = BIG4000_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG4000_processing() start ")

            cdto = BIG4000_processing(big4000cdto)

        else :
            raise Exception('BIG4000_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG4000-'+ str(err))
        include.setErr('EBIG4000', 'BIG4000' + str(err))
    else:
        comlogging.logger.info( 'BIG4000-성공')
    finally:

        BIG4000_end(cdto)

        if include.isError() == False :
            return True
        else :
            return False

def BIG4000_start() :
    try:
        big4000cdto = include.gcominfo['sysargv'][3]

    except Exception as err:
        comlogging.logger.error( 'BIG4000_start-' + str(err))
        include.setErr('EBIG4000', 'BIG4000_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG4000_start-성공')
    finally:
        if include.isError() == False :
            return big4000cdto
        else :
            return False

def BIG4000_processing(big4000cdto) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))
        domain_function = big4000cdto.indata['domain_function']
        big4000cdto = dc_bg004.preAnalysis(big4000cdto)
        if big4000cdto  != True :
            if domain_function == "analysisFeature" :
                dc_bg004.analysisFeature(big4000cdto)
            elif domain_function == "trainModel" :
                dc_bg004.trainModel(big4000cdto)


        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG4000_processing '+ str(err) )
        include.setErr('EBIG4000', 'BIG4000_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG4000_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG4000_end(tdata) :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'BIG4000_end '+ str(err))
        include.setErr('EBIG4000', 'BIG4000_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG4000_end-성공')
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
