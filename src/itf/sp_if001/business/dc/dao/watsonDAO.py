import os, time, threading
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.itf.sp_if001.business.dc.dao import queryDAO
from src.com.fwk.business.util.parser import comparser
from src.com.fwk.business.util.dbms import comdbutil

def callsentimentWATSON(r3ow) :
    rtn = False

    if len(r3ow) == 0:
        return False
    doc_id = r3ow[0]
    doc_content = r3ow[1]
    dic = dict()
    nluResult = tpsutil.tpssendrecv('sentiment', doc_content, [])
    if nluResult == include.FAIL or nluResult == False :
        return False

    dic['docid'] = doc_id
    dic['response'] = nluResult
    return dic

def callentityWATSON(r3ow) :
    rtn = False

    if len(r3ow) == 0:
        return False

    doc_id = r3ow[0]
    doc_content = r3ow[1]
    dic = dict()
    nluResult = tpsutil.tpssendrecv('entity', doc_content, [])
    if nluResult == include.FAIL or nluResult == False:
        return False

    dic['docid'] = doc_id
    dic['response'] = nluResult
    return dic
