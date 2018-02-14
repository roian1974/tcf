import sys, os, yaml, time, glob, codecs, json, csv, time
import pandas as pd
import numpy as np
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.big.sp_bg002.business.dc import dc_bg003

def BIG2001():
    rtn = True
    try:
        comlogging.logger.info( "BIG2001_start() start ")
        cdto = BIG2001_start()

        if include.isError() == False:
            comlogging.logger.info( "BIG2001_processing() start ")
            cdto = BIG2001_processing(cdto)

        else :
            raise Exception('BIG2001_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG2001-'+ str(err))
        include.setErr('EBIG2001', 'BIG2001' + str(err))
    else:
        comlogging.logger.info( 'BIG2001-성공')
    finally:

        BIG2001_end(cdto)

        if include.isError() == False :
            return True
        else :
            return False

def BIG2001_start() :
    try:

        cdto = include.gcominfo['sysargv'][3]
        env_filename = cdto.indata['env_filename']
        config_filename = cdto.indata['config_filename']

        # yaml 환경정보를 저장한다.
        environment = yaml.load( codecs.open(env_filename, "r", "utf-8") )['running_env']
        envinfo =  yaml.load(codecs.open(config_filename, "r", "utf-8"))[environment]

        cdto.ddto['envinfo'] = envinfo

    except Exception as err:
        comlogging.logger.error( 'BIG2001_start-' + str(err))
        include.setErr('EBIG2001', 'BIG2001_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG2001_start-성공')
    finally:
        if include.isError() == False :
            return cdto
        else :
            return False

def BIG2001_processing(cdto) :
    try:

        comlogging.logger.info("#################################################################" + str(getIntTime()))

        cdto = dc_bg003.preAnalysis(cdto)
        if cdto  != True :
            if cdto.indata['domain_function'] == 'makeModel' :
                dc_bg003.makeModel(cdto)
            elif cdto.indata['domain_function'] == 'predictModel' :
                cdto = dc_bg003.predictModel(cdto)

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG2001_processing '+ str(err) )
        include.setErr('EBIG2001', 'BIG2001_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG2001_processing-성공')
    finally:
        if include.isError() == False :
            return cdto
        else :
            return False

def BIG2001_end(cdto) :
    try:
        #------------------------------------------------------------------------------------------------------------
        # 클라이언트로 전송할 내용을 저장한다.
        # ------------------------------------------------------------------------------------------------------------
        include.gcominfo['outdata'].append(cdto)

    except Exception as err:
        comlogging.logger.error( 'BIG2001_end '+ str(err))
        include.setErr('EBIG2001', 'BIG2001_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG2001_end-성공')
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
