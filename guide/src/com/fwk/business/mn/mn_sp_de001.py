import sys
import timeit

from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.dbms import comdbutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.stf import stf_common
from src.com.fwk.business.etf import etf_common
from src.ded.sp_de001.business.pc import sp_de001


def MN_SP_de001():
    # 시간표시
    lsSrvInTime = ''

    include.showCominfo()

    comutil.fprint(__file__, "MN_SP_de001 모듈시작")
    rtn = 0

    try:
        comutil.fprint(__file__, "=================== STF() 함수호출 ")
        comutil.fprint(__file__, "STF() start ")
        stf_common.STF()
        comutil.fprint(__file__, "STF() end ")

        if include.gcominfo['err_info']['finalcd'][0] != 'E':

            comutil.fprint(__file__, "STF() 함수호출성공 ")
            comutil.fprint(__file__,
                           "===================AP [%s] main start " % (include.gcominfo['com_info']['svcname']))
            rtn = sp_de001.SP_de001()
            comutil.fprint(__file__, "===================AP [%s] main end " % (include.gcominfo['com_info']['svcname']))

            if include.gcominfo['err_info']['finalcd'][0] != 'E':
                comutil.fprint(__file__, "AP[%s] 함수호출성공" % (include.gcominfo['com_info']['svcname']))
            else:
                comutil.fprint(__file__, "AP[%s] 함수호출실패" % (include.gcominfo['com_info']['svcname']))
        else:
            comutil.fprint(__file__, "STF() 함수호출실패 ")

    except Exception as err:
        print('▲▲▲ ERR',str(err))
        comutil.ferrprint(__file__, 'MN_SP_de001', str(err))
        include.setErr('ECOM001', 'MN Error-' + str(err))
    else:
        comutil.fprint(__file__, "SUS:F[" + 'MN_SP_de001' + ']함수 호출성공')
    finally:
        comutil.fprint(__file__, "=================== ETF() 함수호출 ")
        comutil.fprint(__file__, "ETF() start ")
        rtn = etf_common.ETF()
        comutil.fprint(__file__, "ETF() end ")

        if rtn == 0:
            comutil.fprint(__file__, "ETF() 함수호출성공")
        else:
            comutil.fprint(__file__, "ETF() 함수호출실패")

        include.showCominfo()

        return include.SUCCESS

#------------------------------------------
# python tcf_sp_de001.py DED101 filename

def tpsvrinit(argv):
    include.setComInfoInit()
    include.gcominfo['com_info']['svcname'] = 'sp_de001'
    include.gcominfo['pid'] = comutil.getpid()
    # include.gcominfo['sysargv'] = comutil.getsysargv()
    include.gcominfo['sysargv'] = argv
    include.start_timeit = timeit.default_timer()
    if len(sys.argv) >= 2 :
        include.gcominfo['com_info']['hostprog'] = include.gcominfo['sysargv'][1]
    else :
        print("\t==================================================")
        print("\tusage : python", sys.argv[0], "HOSTPROG XXXX....")
        print("\t------------------------------------------------")
        print("        python", sys.argv[0], 'DED1003.....')
        print("\t==================================================")
        exit(0)

    comutil.fprint(__file__, "============================================= MN_SP_de001() s")

    comutil.fprint(__file__, 'DB connect 호출(dbconnect)')

    tpsutil.tpenv()

    host = include.gtcfenv['db_host']
    user = include.gtcfenv['db_user']
    password = include.gtcfenv['db_password']
    db = include.gtcfenv['db_dbname']

    print('-----------------------------')
    print(host,user,password,db)
    print('-----------------------------')

    rtn = comdbutil.dbinit(host, user, password, db)
    print('rtn-',rtn)
    if rtn == -1:
        comutil.fprint(__file__, "▲ dbconnect() call failed")
        include.setErr('ECOM002', 'DB connect fail')
        return -1
    else:
        comutil.fprint(__file__, "dbconnect() call success")
        include.gcominfo['dbconn'] = include.gdb
        include.gcominfo['dbconn'] = comdbutil.gdbmsSession

    username = include.gtcfenv['watson_user']
    passwd = include.gtcfenv['watson_password']
    version = include.gtcfenv['watson_version']

    rtn = tpsutil.tpsinit(username, passwd, version)
    if rtn == -1:
        comutil.fprint(__file__, "▲tpsinit() call failed")
        include.setErr('ECOM003', 'tpsinit() connect fail')
        return -1
    else:
        comutil.fprint(__file__, "tpsinit() call success")

    return include.SUCCESS


def tpsvrdone():
    comdbutil.dbclose()

def commandmain() :
    # sys.argv = ['C:/jDev/MyWorks/PycharmProjects/Roian/src/mn_sp_de001.py', 'DED1003', 'arg2']
    rtn = tpsvrinit(sys.argv)
    if rtn == -1:
        tpsvrdone()
        exit(-1)
    else:
        MN_SP_de001()
    tpsvrdone()
    comutil.fprint(__file__, "============================================= MN_SP_de001() e")

    include.showCominfo()


def main(argv):
    argv=['C:/jDev/MyWorks/PycharmProjects/Roian/src/mn_sp_de001.py', 'DED1003', 'xxxxx']
    rtn = tpsvrinit(argv)
    if rtn == -1:
        tpsvrdone()
        exit(-1)
    else:
        MN_SP_de001()
    tpsvrdone()
    comutil.fprint(__file__, "============================================= MN_SP_de001() e")

    include.showCominfo()

if __name__ == "__main__":
    commandmain()
    exit(0)
