import time
import os
from multiprocessing import Process
from multiprocessing import Queue
import threading
import signal

from src.com.sp_comrc.transfer import com1100CDTO
from src.com.sp_comrc.business.dc import dc_comrc
from src.com.sp_comrc.business.pc.mod import call_subprocessor
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.dbms import comdbutil
from src.com.sp_comrc.business.pc.mod import com9001



# pyexe tcf_sp_commo.py sp_comrc COM9002 건수처리단위 (1건이면 5초단위로 1건씩 처리)

def COM9002() :
    rtn = True
    try:
        comlogging.logger.info( "COM9002_start() start ")

        while True:

            time.sleep(3)
            comlogging.logger.info("##########" + str(time.mktime(time.localtime())))
            # rtn = tpsutil.tpbegin()
            rtn = tpsutil.tpbegin_ty2()
            if rtn == False:
                print('tpbegin fail')
                continue

            parameter=[]
            rows = dc_comrc.queryDocument("select_document_01", parameter)


            if rows == False or rows == 1403 :
                comlogging.logger.error('select_document_01')
                time.sleep(1)
            else:
                print('1.document read count in "N"(', len(rows),')')
                if len(rows) == 0:
                    continue

                # 3건단위로 리스트를 작성해서 Processor에 할당한다.
                thread_cnt = int( include.gcominfo['sysargv'][3])
                per_data_processing = int(include.gcominfo['sysargv'][3])
                job_r2ows = call_subprocessor.divide_task(rows, thread_cnt)
                thread_list = []
                queue = Queue()
                processor_cnt = 0

                if include.getOSType() != 'Windows':
                    signal.signal(signal.SIGCHLD, child_exited)

                comlogging.logger.error('▲ 전체건수:' + str(len(rows)) + " ,루핑건수:" + str(len(job_r2ows)))
                for r2ow in job_r2ows :
                    com1100CDTO.COM1100CDTO_I.append(r2ow)
                    com1100CDTO.COM1100CDTO_I.append(queue)

                    if thread_cnt == 1 :
                        time.sleep(5)

                    comlogging.logger.error("   내부프로세스 전달건수(r2ow ):" + str(len(r2ow)) + '  ,프로세스 기동건수-' + str(processor_cnt))
                    thread = threading.Thread(target=subthread_function, args=(r2ow, queue,))

                    thread_list.append(thread)
                    thread.start()
                    processor_cnt += 1

                queue_message_cnt=0
                loop_cnt=0
                while True :
                    time.sleep(0.1)
                    print("3.queue waiting....main processor..", os.getpid())
                    loop_cnt += 1

                    # 3시간 이상 작업
                    if loop_cnt % 10 == 0 :
                        comlogging.logger.error(
                            "    메인프로세스 대기중..." + '잡완료건수:' + str(queue_message_cnt) + ' 프로세스대상건수:' + str(processor_cnt))

                    if not queue.empty() :
                        res = queue.get()
                        queue_message_cnt += 1
                        print('3.1 queue message..[', res, '] processor_cnt-', processor_cnt, 'queue_message_cnt-', queue_message_cnt)
                    if queue_message_cnt == processor_cnt :
                        comlogging.logger.error('  (이너 프로세스 종료) job message:' + res + ', 프로세스 기동건수:' + str(
                                processor_cnt) + ' ,큐수신메시지건수:' + str(
                                queue_message_cnt))
                        break

                for thread in thread_list:
                    thread.join

                queue.close()
                comlogging.logger.error('  (메인프로세스 종료)......')

            tpsutil.tpcommit()

            comlogging.logger.info("############" + str(time.mktime(time.localtime())))

    except Exception as err:
        comlogging.logger.error( 'COM9002-'+ str(err))
        include.setErr('ECOM9002', 'COM9002' + str(err))

    else:
        comlogging.logger.info( 'COM9002-성공')
    finally:

        queue.close()

        if include.isError() == False :
            return True
        else :
            return False

def child_exited(sig, frame):
    pid, exitcode = os.wait()
    print("Child process {pid} exited with code {exitcode}".format(pid=pid, exitcode=exitcode))

#-----------------------------------------------------------------------------------------------------------------------

def subthread_function(r2ow,queue) :

    try :
        rcnt = False
        txflag = True

        tpsutil.tpenv()

        # rtn = tpsutil.tpbegin()
        # if rtn == False:
        #     queue.put(str(os.getpid()) + ' job end')
        #     print('tpbegin fail-', os.getpid())
        #     raise Exception('tpbegin error')
        #
        # rtn = tpsutil.tpsinit_processor()
        # if rtn == False:
        #     queue.put(str(os.getpid()) + ' job end')
        #     print('tpsinit_processor fail-', os.getpid())
        #     raise Exception('tpsinit_processor error')



        for r3ow in r2ow:
            rcnt += 1
            comlogging.logger.error("시작-" + str(rcnt) + " ======================================================================:" + r3ow[0])


            dic_response_s = com9001.nlu_sentiment(r3ow)
            if dic_response_s == False :
                comlogging.logger.error(" NLU(Sentiment) 호출실패:" + r3ow[0] )
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                dc_comrc.upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                continue

            dic_response_e = com9001.nlu_entity(r3ow)
            if dic_response_e == False :
                comlogging.logger.error(" NLU(Sentiment) 호출실패:" + r3ow[0] )
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                dc_comrc.upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                continue

            print("--save data--", rcnt, "-------------------------------", r3ow[0], os.getpid())
            if com9001.result_processing_document(dic_response_s) == False :
                txflag = False
                break

            if  com9001.result_processing_entity(dic_response_e) == False :
                txflag = False
                print("#================================================",txflag)
                break

            tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
            if comdbutil.upsert("update_document_01", [], tup) == False:
                txflag = False
                break

    except Exception as err:
        print('▲subprocessor_function()-ERR:', str(err),os.getpid())
        txflag = False
        rtn = False
    else:
        print('▲subprocessor_function()-성공:',os.getpid())
        rtn = True
    finally:

        # if txflag == True :
        #     tpsutil.tpcommit()
        #     print("tpcommit success -child")
        # else:
        #     tpsutil.tprollback()
        #     print("tprollback success -child")

        queue.put(str(os.getpid()) + ' job end')

        return rtn

