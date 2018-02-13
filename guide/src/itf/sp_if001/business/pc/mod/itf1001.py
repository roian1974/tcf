import time
import os
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.itf.sp_if001.transfer.itf1001cdto import ITF1001CDTO
from src.itf.sp_if001.business.dc import dc_if001
from src.itf.sp_if001.business.dc.dao import watsonDAO
from src.com.fwk.business.util.dbms import comdbutil


def ITF1001():
    rtn = True
    try:
        comlogging.logger.info( "ITF1001_start() start ")
        incdto = ITF1001_start()
        if incdto != False :
            comlogging.logger.info( "ITF1001_processing() start ")
            ITF1001_processing(incdto)
        else :
            raise Exception('ITF1001_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'ITF1001-'+ str(err))
        include.setErr('EITF1001', 'ITF1001' + str(err))
    else:
        comlogging.logger.info( 'ITF1001-성공')
    finally:
        ITF1001_end(incdto)

        if include.isError() == False :
            return incdto
        else :
            return False

def ITF1001_start() :
    try:
        # 수신데이타 IN,OUT 작성
        incdto = ITF1001CDTO()
        incdto.setIndata(include.gcominfo['indata'][0])
        incdto.setOutdata(include.gcominfo['outdata'])
    except Exception as err:
        comlogging.logger.error( 'ITF1001_start-' + str(err))
        include.setErr('EITF1001', 'ITF1001_start,' + str(err))
    else:
        comlogging.logger.info( 'ITF1001_start-성공')
    finally:
        if include.isError() == False :
            return incdto
        else :
            return False

def ITF1001_processing(incdto) :
    try:

        dc_if001.watsonNLUmanager(incdto)

    except Exception as err:
        comlogging.logger.error( 'ITF1001_processing '+ str(err) )
        include.setErr('EITF1001', 'ITF1001_processing,' + str(err))
    else:
        comlogging.logger.info( 'ITF1001_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def ITF1001_end(incdto) :
    try:
        outdata = incdto.getDic()['outdata']
        outdata.append('SUCCESS')

        goutdata = include.getOutdata()
        goutdata.append(outdata[0])

    except Exception as err:
        comlogging.logger.error( 'ITF1001_end '+ str(err))
        include.setErr('EITF1001', 'ITF1001_end,' + str(err))
    else:
        comlogging.logger.info( 'ITF1001_end-성공')
    finally:

        if include.isError() == False :
            return incdto
        else :
            return False

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())

def getNo(id) :
    sql = "select no,doc_id from document where doc_id=" + id
    conn = comdbutil.gdbmsSession[0]
    curs = conn.cursor()
    curs.execute(sql)
    rows = curs.fetchall()
    curs.close()

    return rows[0][0]
