# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 프레임워크 전체에서 사용되는 주요 정보를 저장관리한다.
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------


import timeit
import logging,logging.handlers
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil

#-----------------------------------------------------------------------------------------------------------------------
gdb = [-1]
#-----------------------------------------------------------------------------------------------------------------------
tcfenv_fname = "C:\jDev\MyWorks\PycharmProjects\Roian\\env\\tcf.env.win"
tcfenv_fname_unix = "/home/u402/env/tcf.env.unix"
# tcfenv_fname_unix = "/home/bigdata/vcomenv/env/tcf.env.unix"
#-----------------------------------------------------------------------------------------------------------------------
output_dir="C:\\jDev\\MyWorks\\PycharmProjects\\Roian\log\\output"
unix_output_dir="/home/u402/log/output"
#-----------------------------------------------------------------------------------------------------------------------
ibatisini_fname='C:\jDev\MyWorks\PycharmProjects\Roian\ibatis\sql.ini'
comibatisini_fname='C:\jDev\MyWorks\PycharmProjects\Roian\ibatis\sql.ini'
#-----------------------------------------------------------------------------------------------------------------------
start_timeit = timeit.default_timer()
end_timeit = timeit.default_timer()
#-----------------------------------------------------------------------------------------------------------------------
FAIL = -1
SUCCESS = 0
#-----------------------------------------------------------------------------------------------------------------------
# 20180128 txbegin 관리
gtpbeginflag = 0
# 프로세스 수행 스타일을 결정한다.
# 기본은 TCF 타입이다.
ptype='TCF'

gcominfo = {
                'com_info' : {
                        'svcname':'',
                        'sysdate':'',
                        'intime':'',
                        'outtime':'',
                        'hostprog':'',
                        'logfile':'',
                        'interval':'' } ,
                'dbconn': [],
                "pid"   : '',
                "ostype" :'',
                'err_info' : {
                        'count'  : 0,
                        'err1cod':'',
                        'err1msg':'',
                        'err2cod':'',
                        'err2msg':'',
                        'err3cod':'',
                        'err3msg':'',
                        'err4cod': '',
                        'err4msg': '',
                        'err5cod': '',
                        'err5msg': '',
                        'err6cod':'',
                        'err6msg':'',
                        'err7cod': '',
                        'err7msg': '',
                        'finalcd': 'Z'
                },
                'sysargv' : [],
                'indata'  : [],
                'outdata'  : []
              }
gtcfenv = {
    'db_host' : '',
    'db_user' : '',
    'db_password' : '',
    'db_dbname' : '',
    'watson_user' : '',
    'watson_password' : '',
    'watson_version' : '',
    'ibatisini_fname' : '',
    'comibatisini_fname' : '',
    'output_dir' : '',
    'unix_output_dir' :''
}

def showCominfo() :
    comlogging.logger.info('#######################################################')
    comlogging.logger.info(gcominfo)
    comlogging.logger.info('#######################################################')

def getErrCnt() :
    return gcominfo['err_info']['count']

def setComInfoInit() :

    gcominfo['com_info']['svcname'] = ''
    gcominfo['com_info']['sysdate'] = ''
    gcominfo['com_info']['intime'] = ''
    gcominfo['com_info']['outtime'] = ''
    gcominfo['com_info']['logfile'] = ''
    gcominfo['com_info']['interval'] = ''
    gcominfo['dbconn'] = []
    gcominfo['pid'] = ''
    gcominfo['ostype'] = ''
    gcominfo['err_info']['count'] = 0
    gcominfo['err_info']['err1cod'] = ''
    gcominfo['err_info']['err2cod'] = ''
    gcominfo['err_info']['err3cod'] = ''
    gcominfo['err_info']['err4cod'] = ''
    gcominfo['err_info']['err5cod'] = ''
    gcominfo['err_info']['err6cod'] = ''
    gcominfo['err_info']['err7cod'] = ''
    gcominfo['err_info']['err1msg'] = ''
    gcominfo['err_info']['err2msg'] = ''
    gcominfo['err_info']['err3msg'] = ''
    gcominfo['err_info']['err4msg'] = ''
    gcominfo['err_info']['err5msg'] = ''
    gcominfo['err_info']['err6msg'] = ''
    gcominfo['err_info']['err7msg'] = ''
    gcominfo['err_info']['finalcd'] = 'Z'
    gcominfo['sysargv'] = []
    gcominfo['indata'] = []
    gcominfo['outdata'] = []

    setOSType()


def setIndata(indata) :
    gcominfo['indata'].append(indata)

def getIndata() :
    return gcominfo['indata']

def setOutdata(outdata) :
    gcominfo['outdata'].append(outdata)

def getOutdata() :
    return gcominfo['outdata']

def setErr(errcode,errmsg) :
    errcnt = getErrCnt()
    if errcnt < 7  :
        errcnt += 1
        meta_no = 'err%dcod' % errcnt
        meta_ms = 'err%dmsg' % errcnt
        gcominfo['err_info'][meta_no] = errcode
        gcominfo['err_info'][meta_ms] = errmsg
        gcominfo['err_info']['finalcd'] = errcode
        gcominfo['err_info']['count'] += 1
    else :
        comlogging.logger.error('현재 메시지 갯수[' + str(errcnt) + '] 더이상 추가할 수 없음')

def setServiceName(svcname) :
    gcominfo['com_info']['svcname'] = svcname

def setPid() :
    gcominfo['pid'] = comutil.getpid()

def setArgv(argv) :
    gcominfo['sysargv'] = argv

def getArgv() :
    return gcominfo['sysargv']

def setStartTime() :
    global start_timeit
    start_timeit = timeit.default_timer()

def setEndTime() :
    global end_timeit
    end_timeit = timeit.default_timer()

def setIntervaletf() :
    global end_timeit, start_timeit
    end_timeit = timeit.default_timer()
    gcominfo['com_info']['interval'] = ('%f' % (end_timeit - start_timeit))

def setHostProg(hostprog) :
    gcominfo['com_info']['hostprog'] = hostprog

def setSysDate() :
    gcominfo['com_info']['sysdate'] = comutil.getsysdate()

def getSysDate() :
    return gcominfo['com_info']['sysdate']

def setInSysTime() :
    gcominfo['com_info']['intime'] = comutil.getsystime()

def setOutSysTime() :
    gcominfo['com_info']['outtime'] = comutil.getsystime()

def setOSType() :
    gcominfo['ostype'] = comutil.getostype()

def getOSType() :
    return gcominfo['ostype']

def setInterval(val) :
    gcominfo['com_info']['interval'] = val

def getInterval() :
    return gcominfo['com_info']['interval']

def setLogFile(logfile) :
    gcominfo['com_info']['logfile'] = logfile

def getLogFile() :
    return gcominfo['com_info']['logfile']


def isError() :
    if gcominfo['err_info']['finalcd'][0] == 'E':
        return True
    elif gcominfo['err_info']['finalcd'][0] == 'Z':
        return False
    else:
        return False

def getHostProg() :
    return gcominfo['com_info']['hostprog']

def getServiceName() :
    return gcominfo['com_info']['svcname']

def getDBHost() :
    return gtcfenv['db_host']

def getDBuser() :
    return gtcfenv['db_user']

def getDBpasswd() :
    return gtcfenv['db_password']

def getDBname() :
    return gtcfenv['db_dbname']

def getWatsonUserName() :
    return gtcfenv['watson_user']

def getWatsonPasswd() :
    return gtcfenv['watson_password']

def getWatsonVersion():
    return gtcfenv['watson_version']
