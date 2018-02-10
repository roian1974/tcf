# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 트랜잭션 시작전 주요하게 작업해야 될 사전에 수행한다.
#            - 트랜잭션을 시작
#            _ 주요정보 관리 및 저장
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------

import timeit
import logging,logging.handlers
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.tpm import tpsutil



def STF():

    try:
        comlogging.logger.info( "set sysdate")
        include.setSysDate()

        comlogging.logger.info("set sysintime")
        include.setInSysTime()
        include.setOutSysTime()

        comlogging.logger.info("set os type")
        include.setOSType()

        comlogging.logger.info("set start int time")
        include.setStartTime()
        include.setEndTime()

        comlogging.logger.info("set indata-" + str(len(include.gcominfo['sysargv'])))
        if len(include.gcominfo['sysargv']) > 3 :
            i=3
            while True :
                include.setIndata(include.gcominfo['sysargv'][i])
                i = i+1
                if i+1 > len( include.gcominfo['sysargv']) :
                    break

        comlogging.logger.info( "서비스로그파일을 정한다.")
        if include.getOSType() == 'Windows' :
            logfile = "{0}\\{1}.log.{2}".format(include.output_dir,
                                                include.getServiceName(),
                                                include.getSysDate() )
        else :
            logfile = "{0}/{1}.log.{2}".format(include.unix_output_dir,
                                                   include.getServiceName(),
                                                   include.getSysDate())

        comlogging.logger.info( "set interval 0")
        include.setInterval(0)

        comlogging.logger.info("set logfile-" + logfile)
        include.setLogFile(logfile)

        if include.ptype == "TCF":
            rtn = tpsutil.tpbegin()
            if rtn == False:
                print('tpbegin fail')
                raise Exception('tpbegin() call 에러')

    except Exception as err:
        comlogging.logger.error( 'STF '+ str(err))
        include.setErr('ECOM002', 'STF Error-' + str(err))
    else:
        comlogging.logger.info( 'STF함수 '+ '성공')
    finally:

        if include.isError() == True :
            return False
        else :
            return True


