import time
import os
from multiprocessing import Process
from multiprocessing import Queue
import threading
import signal
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil

from src.com.sp_comrc.transfer import com1100CDTO
from src.com.sp_comrc.business.dc.dao import queryDAO
from src.com.sp_comrc.business.dc import dc_comrc
from src.com.sp_comrc.business.pc.mod import call_subprocessor
from src.com.fwk.business.util.dbms import comdbutil
from src.com.sp_comrc.business.pc.mod import com9001
from src.com.fwk.business.util.common import comutil



# 100건을 한번체 처리하고 죽는다.
gCallCnt=0
def COM9003() :
    rtn = True
    try:
        comlogging.logger.info( "COM9003_start() start ")


        comlogging.logger.info("##########" + str(time.mktime(time.localtime())))
        parameter=[]
        rows = dc_comrc.queryDocument("select_document_01", parameter)

        if rows == False or rows == 1403 :
            comlogging.logger.error('select_document_01')
            raise Exception("Data Not Found-1")
        else:
            print('1.document read count in "N"(', len(rows),')')
            if len(rows) == 0:
                raise Exception("Data Not Found-2")

            # 3건단위로 리스트를 작성해서 Processor에 할당한다.
            thread_cnt = int( include.gcominfo['sysargv'][3])
            per_data_processing = int(include.gcominfo['sysargv'][3])
            job_r2ows = call_subprocessor.divide_task(rows, thread_cnt)
            processor_cnt = 0

            if include.getOSType() != 'Windows':
                signal.signal(signal.SIGCHLD, child_exited)

            comlogging.logger.error('▲ 전체건수:' + str(len(rows)) + " ,루핑건수:" + str(len(job_r2ows)))
            greadcnt = 0
            for r2ow in job_r2ows :
                comlogging.logger.error("   내부프로세스 전달건수(r2ow ):" + str(len(r2ow)) + '  ,프로세스 기동건수-' + str(processor_cnt))
                if subprocessor_exe(r2ow) == False :
                    raise Exception("..처리중 에러")
                    break

        comlogging.logger.info("############" + str(time.mktime(time.localtime())))

    except Exception as err:
        comlogging.logger.error( 'COM9003-'+ str(err))
        include.setErr('ECOM9003', 'COM9003' + str(err))

    else:
        comlogging.logger.info( 'COM9003-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False

def child_exited(sig, frame):
    pid, exitcode = os.wait()
    print("Child process {pid} exited with code {exitcode}".format(pid=pid, exitcode=exitcode))

#-----------------------------------------------------------------------------------------------------------------------

def subprocessor_exe (r2ow) :

    try :
        global gCallCnt
        txflag = True
        rtn = True

        tpsutil.tpenv()

        cnt=0
        for r3ow in r2ow:
            cnt += 1
            gCallCnt += 1
            comlogging.logger.error("시작 " + str(gCallCnt) + ' ' + str(cnt) +" ======================================================================:" + r3ow[0])
            dic_response_s = com9001.nlu_sentiment(r3ow)
            comlogging.logger.error(" NLU(Sentiment) 호출실패:" + r3ow[0])
            if dic_response_s == False :
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                comdbutil.upsert("update_document_01", [], tup)
                continue

            dic_response_e = com9001.nlu_entity(r3ow)
            if dic_response_e == False :
                comlogging.logger.error(" NLU(Entity) 호출실패:" + r3ow[0])
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                comdbutil.upsert("update_document_01", [], tup)
                continue

            if com9001.result_processing_document(dic_response_s) == False :
                rtn = False
                break

            if  com9001.result_processing_entity(dic_response_e) == False :
                rtn = False
                break

            tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
            if comdbutil.upsert("update_document_01", [], tup) == False:
                include.setErr('ECOM9001', 'COM9001_processing upsertDocument 에러 ')
                rtn = False
                break

    except Exception as err:
        print('▲subprocessor_function()-ERR:', str(err),os.getpid())
        txflag = False
        rtn = False
    else:
        print('▲subprocessor_function()-성공:',os.getpid())
    finally:
        print("--------", rtn)
        return rtn
