# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 프레임워크 전체에서 사용되는 주요 정보를 저장관리한다.
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------
import timeit
import logging,logging.handlers
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil

class CInclude:
    gdb = [-1]
    tcfenv_fname = "C:\jDev\MyWorks\PycharmProjects\Roian\\env\\tcf.env.win"
    tcfenv_fname_unix = "/home/u402/env/tcf.env.unix"
    output_dir = "C:\\jDev\\MyWorks\\PycharmProjects\\Roian\log\\output"
    unix_output_dir = "/home/u402/log/output"
    ibatisini_fname = 'C:\jDev\MyWorks\PycharmProjects\Roian\ibatis\sql.ini'
    comibatisini_fname = 'C:\jDev\MyWorks\PycharmProjects\Roian\ibatis\sql.ini'
    start_timeit = timeit.default_timer()
    end_timeit = timeit.default_timer()
    gtpbeginflag = 0

    gcominfo = {
        'com_info': {
            'svcname': '',
            'sysdate': '',
            'intime': '',
            'outtime': '',
            'hostprog': '',
            'logfile': '',
            'interval': ''},
        'dbconn': [],
        "pid": '',
        "ostype": '',
        'err_info': {
            'count': 0,
            'err1cod': '',
            'err1msg': '',
            'err2cod': '',
            'err2msg': '',
            'err3cod': '',
            'err3msg': '',
            'err4cod': '',
            'err4msg': '',
            'err5cod': '',
            'err5msg': '',
            'err6cod': '',
            'err6msg': '',
            'err7cod': '',
            'err7msg': '',
            'finalcd': 'Z'
        },
        'sysargv': [],
        'indata': [],
        'outdata': []
    }
    gtcfenv = {
        'db_host': '',
        'db_user': '',
        'db_password': '',
        'db_dbname': '',
        'watson_user': '',
        'watson_password': '',
        'watson_version': '',
        'ibatisini_fname': '',
        'comibatisini_fname': '',
        'output_dir': '',
        'unix_output_dir': ''
    }

    def __init__(self):
        pass

    def showCominfo(self) :
        comlogging.logger.info('#######################################################')
        comlogging.logger.info(self.gcominfo)
        comlogging.logger.info('#######################################################')

    def getErrCnt(self) :
        return self.gcominfo['err_info']['count']

    def setComInfoInit(self) :

        self.gcominfo['com_info']['svcname'] = ''
        self.gcominfo['com_info']['sysdate'] = ''
        self.gcominfo['com_info']['intime'] = ''
        self.gcominfo['com_info']['outtime'] = ''
        self.gcominfo['com_info']['logfile'] = ''
        self.gcominfo['com_info']['interval'] = ''
        self.gcominfo['dbconn'] = []
        self.gcominfo['pid'] = ''
        self.gcominfo['ostype'] = ''
        self.gcominfo['err_info']['count'] = 0
        self.gcominfo['err_info']['err1cod'] = ''
        self.gcominfo['err_info']['err2cod'] = ''
        self.gcominfo['err_info']['err3cod'] = ''
        self.gcominfo['err_info']['err4cod'] = ''
        self.gcominfo['err_info']['err5cod'] = ''
        self.gcominfo['err_info']['err6cod'] = ''
        self.gcominfo['err_info']['err7cod'] = ''
        self.gcominfo['err_info']['err1msg'] = ''
        self.gcominfo['err_info']['err2msg'] = ''
        self.gcominfo['err_info']['err3msg'] = ''
        self.gcominfo['err_info']['err4msg'] = ''
        self.gcominfo['err_info']['err5msg'] = ''
        self.gcominfo['err_info']['err6msg'] = ''
        self.gcominfo['err_info']['err7msg'] = ''
        self.gcominfo['err_info']['finalcd'] = 'Z'
        self.gcominfo['sysargv'] = []
        self.gcominfo['indata'] = []
        self.gcominfo['outdata'] = []

        self.setOSType()


    def setIndata(self,indata) :
        self.gcominfo['indata'].append(self,indata)

    def getIndata(self) :
        return self.gcominfo['indata']

    def setOutdata(self,outdata) :
        self.gcominfo['outdata'].append(self,outdata)

    def getOutdata(self) :
        return self.gcominfo['outdata']

    def setErr(self,errcode,errmsg) :
        errcnt = self.getErrCnt()
        if errcnt < 7  :
            errcnt += 1
            meta_no = 'err%dcod' % errcnt
            meta_ms = 'err%dmsg' % errcnt
            self.gcominfo['err_info'][meta_no] = errcode
            self.gcominfo['err_info'][meta_ms] = errmsg
            self.gcominfo['err_info']['finalcd'] = errcode
            self.gcominfo['err_info']['count'] += 1
        else :
            comlogging.logger.error('현재 메시지 갯수[' + str(errcnt) + '] 더이상 추가할 수 없음')

    def setServiceName(self,svcname) :
        self.gcominfo['com_info']['svcname'] = svcname

    def setPid(self) :
        self.gcominfo['pid'] = comutil.getpid()

    def setArgv(self,argv) :
        self.gcominfo['sysargv'] = argv

    def getArgv(self) :
        return self.gcominfo['sysargv']

    def setStartTime(self) :
        global start_timeit
        start_timeit = timeit.default_timer(self)

    def setEndTime(self) :
        global end_timeit
        end_timeit = timeit.default_timer(self)

    def setIntervaletf(self) :
        global end_timeit, start_timeit
        end_timeit = timeit.default_timer()
        self.gcominfo['com_info']['interval'] = ('%f' % (end_timeit - start_timeit))

    def setHostProg(self,hostprog) :
        self.gcominfo['com_info']['hostprog'] = hostprog

    def setSysDate(self) :
        self.gcominfo['com_info']['sysdate'] = comutil.getsysdate()

    def getSysDate(self) :
        return self.gcominfo['com_info']['sysdate']

    def setInSysTime(self) :
        self.gcominfo['com_info']['intime'] = comutil.getsystime()

    def setOutSysTime(self) :
        self.gcominfo['com_info']['outtime'] = comutil.getsystime()

    def setOSType(self) :
        self.gcominfo['ostype'] = comutil.getostype()

    def getOSType(self) :
        return self.gcominfo['ostype']

    def setInterval(self,val) :
        self.gcominfo['com_info']['interval'] = val

    def getInterval(self) :
        return self.gcominfo['com_info']['interval']

    def setLogFile(self,logfile) :
        self.gcominfo['com_info']['logfile'] = logfile

    def getLogFile(self) :
        return self.gcominfo['com_info']['logfile']


    def isError(self) :
        if self.gcominfo['err_info']['finalcd'][0] == 'E':
            return True
        elif self.gcominfo['err_info']['finalcd'][0] == 'Z':
            return False
        else:
            return False

    def getHostProg(self) :
        return self.gcominfo['com_info']['hostprog']

    def getServiceName(self) :
        return self.gcominfo['com_info']['svcname']

    def getDBHost(self) :
        return self.gtcfenv['db_host']

    def getDBuser(self) :
        return self.gtcfenv['db_user']

    def getDBpasswd(self) :
        return self.gtcfenv['db_password']

    def getDBname(self) :
        return self.gtcfenv['db_dbname']

    def getWatsonUserName(self) :
        return self.gtcfenv['watson_user']

    def getWatsonPasswd(self) :
        return self.gtcfenv['watson_password']

    def getWatsonVersion(self):
        return self.gtcfenv['watson_version']
