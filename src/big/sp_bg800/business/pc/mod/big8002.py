import time
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg800.business.dc import dc_bg802
from src.big.sp_bg800.transfer import big8001cdto

def BIG8002():
    rtn = True
    try:
        comlogging.logger.info( "BIG8002_start() start ")
        _big8001cdto = BIG8002_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG8002_processing() start ")

            tdata = BIG8002_processing(_big8001cdto)

        else :
            raise Exception('BIG8002_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG8002-'+ str(err))
        include.setErr('EBIG8002', 'BIG8002' + str(err))
    else:
        comlogging.logger.info( 'BIG8002-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG8002_end(tdata)

        if include.isError() == False :
            return True
        else :
            return False

def BIG8002_start() :
    try:
        _big8001cdto = include.gcominfo['sysargv'][3]

    except Exception as err:
        comlogging.logger.error( 'BIG8002_start-' + str(err))
        include.setErr('EBIG8002', 'BIG8002_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG8002_start-성공')
    finally:
        if include.isError() == False :
            return _big8001cdto
        else :
            return False

def BIG8002_processing(pbig8001cdto) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        pbig8001cdto = dc_bg802.preAnalysis(pbig8001cdto)
        if pbig8001cdto  != True :
            dc_bg802.trainModel(pbig8001cdto)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG8002_processing '+ str(err) )
        include.setErr('EBIG8002', 'BIG8002_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG8002_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG8002_end(tdata) :
    try:

        pass

    except Exception as err:
        comlogging.logger.error( 'BIG8002_end '+ str(err))
        include.setErr('EBIG8002', 'BIG8002_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG8002_end-성공')
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
