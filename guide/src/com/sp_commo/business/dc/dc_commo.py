import pymysql.cursors
import json
import time
import logging,logging.handlers
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.sp_commo.business.dc.dao import queryDAO

def queryDocument(sql_id, parameter) :
    try:
        rtn = True
        rows = queryDAO.queryDocument(sql_id, parameter)
        if rows == False:
            comlogging.logger.error(sql_id + 'fetch error')
        else:
            if len(rows) == 0:
                rtn = 1403
                raise Exception('Data Not Found')
    except Exception as err:
        comlogging.logger.error('▲queryDocument()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲queryDocument()-성공:')
    finally:
        if rtn == True :
            return rows
        elif rtn == 1403 or rtn == False :
            return rtn
        else :
            return False

def upsertDocument(sql_id, parameter,tup) :
    try:
        rtn = True
        if queryDAO.upsertDocument(sql_id, parameter, tup) == True:
            print('insert insert_doc_sentiment_01- doc_sentiment success')
        else:
            rtn = False
            raise Exception('upsertDocument error')
    except Exception as err:
        comlogging.logger.error('▲queryDocument()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲queryDocument()-성공:')
    finally:
        return rtn
