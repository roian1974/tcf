import time
import os
import logging,logging.handlers

from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.dbms import comdbutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.util.logging import comlogging

def queryDocument(sql_id, parameter) :
    try:
        rtn = True
        rows = comdbutil.select_sqlid("fetchall", sql_id, parameter)
    except Exception as err:
        rtn = False
        comlogging.logger.error( 'queryDocument' + str(err))
    else:
        comlogging.logger.info( 'queryDocument-성공-'+rows)
    finally:
        if rtn == True :
            return rows
        else :
            return rtn

def upsertDocument(sql_id, parameter,tup) :
    try:
        rtn = True
        if comdbutil.upsert(sql_id, parameter, tup) == True:
            print('insert insert_doc_sentiment_01- doc_sentiment success')
        else:
            raise Exception('insert_doc_sentiment_01 update error')

    except Exception as err:
        rtn = False
        comlogging.logger.error( 'upsertDocument' + str(err))
    else:
        comlogging.logger.info( 'upsertDocument-성공')
    finally:
        return rtn



