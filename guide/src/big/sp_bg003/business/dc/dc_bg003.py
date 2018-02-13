import pymysql.cursors
import json
import time
import logging,logging.handlers
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.big.sp_bg003.business.dc.dao import queryDAO
from src.big.sp_bg003.business.dc.mod import divideDocument, crawlingExternalData, filterDoc, trainReady, validateModel

def 외부데이터수집() :
    try:

        rtn = True
        crawlingExternalData.excute()

    except Exception as err:
        comlogging.logger.error('▲외부데이터수집()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲외부데이터수집()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False

def 데이터검증() :
    try:
        rtn = True
        divideDocument.긍부정기사분리()

    except Exception as err:
        comlogging.logger.error('▲외부데이터수집()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲외부데이터수집()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False


def 전처리() :
    try:
        rtn = True

        filterDoc.본문없는기사제거()

        filterDoc.중복기사제거()

        filterDoc.종합성기사제거()

        filterDoc.부가정보매핑()

    except Exception as err:
        comlogging.logger.error('▲전처리()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲전처리()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False


def 훈련모형() :
    try:
        trainReady.형태소분리()

        trainReady.불용어처리()

        trainReady.중요도검사_TFIDF()

        trainReady.중요단어선정()

        trainReady.매체별중요단어포함현황체킹()

        trainReady.학습모델도출()

        rtn = True
    except Exception as err:
        comlogging.logger.error('▲훈련모형()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲훈련모형()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False


def 예측() :
    try:
        rtn = True

        validateModel.모형검증()

    except Exception as err:
        comlogging.logger.error('▲예측()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲예측()-성공:')
    finally:
        if rtn == True :
            return True
        else :
            return False

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
