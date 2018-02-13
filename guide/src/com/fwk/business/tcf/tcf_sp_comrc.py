# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 트랜잭션 메인 관리 엔진
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------

import sys
import logging,logging.handlers

from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.dbms import comdbutil
from src.com.fwk.business.stf import stf_common
from src.com.fwk.business.etf import etf_common
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.tcf.action import spaction
from src.com.fwk.business.tcf.action import sjfaction
from src.com.fwk.business.tcf.action import ejfaction


def TCF_SP_comrc():

    include.showCominfo()

    comlogging.logger.info("TCF_SP_comrc 모듈시작")

    try:
        comlogging.logger.info( "=================== STF() 함수호출 ")
        comlogging.logger.info( "STF() start ")
        stf_common.STF()
        comlogging.logger.info( "STF() end ")

        if include.isError() == False :
            comlogging.logger.info( "STF() 함수호출성공 ")
            comlogging.logger.info( "===================AP [%s] main start " % (include.getServiceName()))

            spaction.action(include.getServiceName())

            comlogging.logger.info( "===================AP [%s] main end " % (include.getServiceName()))

            if include.isError() == False :
                comlogging.logger.info( "AP[%s] 함수호출성공" % (include.getServiceName()))
            else:
                comlogging.logger.error( "AP[%s] 함수호출실패" % (include.getServiceName()))
        else:
            comlogging.logger.error( "STF() 함수호출실패 ")

    except Exception as err:
        comlogging.logger.error( 'TCF_SP_comrc 에서 발생 :' + str(err))
        include.setErr('ECOM001', 'TCF Error-' + str(err))
    else:
        comlogging.logger.info( "SUS:F[" + 'TCF_SP_comrc' + ']함수 호출성공')
    finally:
        comlogging.logger.info( "=================== ETF() 함수호출 ")
        comlogging.logger.info( "ETF() start ")
        etf_common.ETF()
        comlogging.logger.info( "ETF() end ")

        include.showCominfo()
        if include.isError() == True :
            return False
        return True

def tpsvrinit(argv):


    # set head
    include.setComInfoInit()
    include.ptype = "TCF"

    # argv[0] = tcf_sp_commo.py -> Transaction Control Function
    # argv[1] = sp_commo -> Service Function
    # argv[2] = COM1000 -> Domain Function
    # argv[3] = [aaa,bbb,ccc]
    if len(argv) >= 2 :
        include.gcominfo['sysargv'] = argv
        hostservice = include.gcominfo['sysargv'][1] #sp_commo
        hostprog = include.gcominfo['sysargv'][2]   #COM1000
        include.setServiceName(hostservice)
        include.setHostProg(hostprog)
    else :
        print("\t==================================================")
        print("\tusage : python", argv[0], "HostService HostProg arg1 arg2 .....")
        print("\t------------------------------------------------")
        print("        python", argv[0], 'sp_commo COM1000 file_name')
        print("\t==================================================")
        exit(0)

    tpsutil.tpenv()

    include.setPid()
    include.setArgv(argv)
    include.setStartTime()

    comlogging.logger = logging.getLogger(__name__)
    comlogging.logger = logging.getLogger('root')
    comlogging.set_logger(comlogging.logger)

    comlogging.logger.info( "============================================= TCF_SP_comrc() s")
    comlogging.logger.info( 'DB connect 호출(dbconnect)')

    host = include.getDBHost()
    user = include.getDBuser()
    password = include.getDBpasswd()
    db = include.getDBname()

    rtn = comdbutil.dbinit(host, user, password, db)
    if rtn == -1:
        comlogging.logger.error( "▲ dbconnect() call failed")
        include.setErr('ECOM002', 'DB connect fail')
        return False
    else:
        comlogging.logger.info( "dbconnect() call success")
        include.gcominfo['dbconn'] = include.gdb
        include.gcominfo['dbconn'] = comdbutil.gdbmsSession

    username = include.getWatsonUserName()
    passwd = include.getWatsonPasswd()
    version = include.getWatsonVersion()

    rtn = tpsutil.tpsinit(username, passwd, version)
    if rtn == -1:
        comlogging.logger.error( "▲tpsinit() call failed")
        include.setErr('ECOM003', 'tpsinit() connect fail')
        return False
    else:
        comlogging.logger.info( "tpsinit() call success")

    if sjfaction.action(include.getServiceName()) == False :
        comlogging.logger.error("SJF module call failed")
        return False
    else :
        pass

    return True

def tpsvrdone():

    if ejfaction.action(include.getServiceName()) == False :
        comlogging.logger.error("EJF module call failed")
        return False
    else :
        pass

    comdbutil.dbclose()


def commandmain() :

    # sys.argv = ['C:/jDev/MyWorks/PycharmProjects/Roian/src/tcf_sp_commo.py', 'sp_commo', 'COM1001', 'test_group_1.xlsx']

    rtn = tpsvrinit(sys.argv)
    if rtn == False:
        tpsvrdone()
        exit(-1)
    else:
        TCF_SP_comrc()
    tpsvrdone()
    comlogging.logger.info( "============================================= TCF_SP_comrc() e")
    comlogging.logger.error("============================================= TCF_SP_comrc() e")

    include.showCominfo()


def main(argv):

    # argv=['tcf_sp_commo', 'sp_commo', 'COM1000', 'entity_group_1.xlsx']

    rtn = tpsvrinit(argv)
    if rtn == False:
        tpsvrdone()
        exit(-1)
    else:
        TCF_SP_comrc()
    tpsvrdone()
    comlogging.logger.info( "============================================= TCF_SP_comrc() e")

    include.showCominfo()

    return include.gcominfo

if __name__ == "__main__":
    # set logging
    commandmain()
    sys.exit(0)





