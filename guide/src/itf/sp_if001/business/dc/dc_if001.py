import os, time, threading
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.itf.sp_if001.business.dc.dao import queryDAO,watsonDAO
from src.com.fwk.business.util.parser import comparser
from src.com.fwk.business.util.dbms import comdbutil
from src.itf.sp_if001.business.dc.mod import crudManger

myLock = threading.Lock()

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

def divide_task(rows,cutting_rows) :

    flag = False
    n1rows = []
    n2rows = []
    for row in rows:
        doc_id = row[0]
        doc_content = row[1]
        if len(n2rows) <= cutting_rows :
            n2rows.append(row)
        if len(n2rows) == cutting_rows :
            n1rows.append(n2rows)
            n2rows = []
    n1rows.append(n2rows)
    return n1rows

def watsonNLUmanager(incdto) :

    try:
        r2ow = incdto.getDic()['indata'][0]

        rcnt = 0
        for r3ow in r2ow:
            rcnt += 1
            comlogging.logger.error("시작-" + str(rcnt) + " ======================================================================:" + r3ow[0])
            dic_response_s = watsonDAO.callsentimentWATSON(r3ow)
            if dic_response_s == False :
                comlogging.logger.error(" NLU(Sentiment) 호출실패:" + r3ow[0] )
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                upsertDocument("update_document_01", [], tup)
                continue

            dic_response_e = watsonDAO.callentityWATSON(r3ow)
            if dic_response_e == False :
                comlogging.logger.error(" NLU(Entity) 호출실패:" + r3ow[0])
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                upsertDocument("update_document_01", [], tup)
                continue

            if crudManger.saveDocsentiment(dic_response_s) == False :
                break

            if  crudManger.saveTargetsentiment(dic_response_e) == False :
                break

            tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
            if upsertDocument("update_document_01", [], tup) != True:
                include.setErr('EITF1001', 'ITF1001_processing upsertDocument 에러 ')
                break

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



def watsonNLUmanageTHREAD(r2ow, queue, name) :

    try :
        rtn = True
        tpsutil.tpenv()

        cnt=0
        for r3ow in r2ow:
            cnt += 1
            comlogging.logger.error("Thread[" + str(name) + "] " + str(cnt) +" =============================:" + r3ow[0])
            dic_response_s = watsonDAO.callsentimentWATSON(r3ow)
            waston_nlu_call_rtn=True

            if dic_response_s == False  :
                comlogging.logger.error("Thread["+str(name) + "]" +" NLU(Sentiment) 호출실패:" + r3ow[0])
                waston_nlu_call_rtn = False
            else :
                dic_response_e = watsonDAO.callentityWATSON(r3ow)
                if dic_response_e == False :
                    comlogging.logger.error("Thread["+str(name) + "]" +" NLU(Entity) 호출실패:" + r3ow[0])
                    waston_nlu_call_rtn = False

            comlogging.logger.error("Thread[" + str(name) + "]" + " gtpbeginflag=" + str(include.gtpbeginflag))
            while True :
                time.sleep(0.5)
                if include.gtpbeginflag == 1 :
                    comlogging.logger.error("Thread[" + str(name) + "]" + " gtpbeginflag=" + str(include.gtpbeginflag))
                    continue
                else :
                    break
            
            myLock.acquire(True)
            include.gtpbeginflag = 0
            tpsutil.tpbegin()
            myLock.release()

            if waston_nlu_call_rtn == False :
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                continue

            if crudManger.saveDocsentiment(dic_response_s) == False :
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                break

            if  crudManger.saveTargetsentiment(dic_response_e) == False :
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                break

            tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
            if comdbutil.upsert("update_document_01", [], tup) == False:
                pass

            tpsutil.tpcommit()

    except Exception as err:
        comlogging.logger.error('▲subprocessor_function()-ERR:'+ str(err))
        rtn = False
        tpsutil.tprollback()
    else:
        comlogging.logger.info('▲subprocessor_function()-성공:')
    finally:
        queue.put(str(os.getpid()) + ' job end')
        return rtn

