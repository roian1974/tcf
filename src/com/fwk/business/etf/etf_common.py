import timeit
import logging,logging.handlers

import logging,logging.handlers
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil

def ETF():
    try:

        if include.ptype == "TCF" :
            comlogging.logger.info("트랜잭션을 완료시킨다.")
            if include.isError() == True :
                tpsutil.tprollback()
            else :
                tpsutil.tpcommit()

        comlogging.logger.info( "프로세스 종료시간을 설정한다")
        include.setIntervaletf()

        comlogging.logger.info( "인터벌은 " + include.getInterval())

        comlogging.logger.info( "로그를 저장합니다")
        ETF_logging()

    except Exception as err:
        comlogging.logger.error( 'ETF '+ str(err))
        include.setErr('ECOM003', 'ETF Error-' + str(err))
    else:
        comlogging.logger.info( 'ETF '+ '성공')
    finally:

        if include.isError() == True :
            return False
        else :
            return True


def ETF_logging() :
    comlogging.logger.info('filename=='+ include.getLogFile()+ '----'+ str(include.gcominfo))
    comutil.file_append(include.getLogFile(), str(include.gcominfo))
    return


