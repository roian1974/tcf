import time, os, signal, threading
from multiprocessing import Queue
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.itf.sp_if001.business.dc import dc_if001
from src.com.fwk.business.util.dbms import comdbutil

def ITF1002() :
    rtn = True
    try:

        while True :
            time.sleep(2)

            comlogging.logger.info("================================================================MAIN 기동")
            comlogging.logger.info( "ITF1002_start() start ")

            rtn = tpsutil.tpbegin()
            if rtn == False:
                print('tpbegin fail')
                tpsutil.tprollback()
                comdbutil.dbclose()
                comdbutil.dbinit_conn()
                continue

            parameter=[]
            rows = dc_if001.queryDocument("select_document_01", parameter)
            tpsutil.tprollback()
            thread_list = []
            queue = Queue()
            if rows == False or rows == 1403 :
                comlogging.logger.error('select_document_01')
                continue
            else:
                if len(rows) == 0:
                    raise Exception("Data Not Found-2")
                thread_cnt = int( include.gcominfo['sysargv'][3])
                job_r2ows = dc_if001.divide_task(rows, thread_cnt)
                if include.getOSType() != 'Windows':
                    signal.signal(signal.SIGCHLD, child_exited)
                comlogging.logger.error('▲ 전체건수:' + str(len(rows)) + " ,루핑건수:" + str(len(job_r2ows)))
                t_cnt=0
                for r2ow in job_r2ows :
                    t_cnt += 1
                    thread = threading.Thread(target=dc_if001.watsonNLUmanageTHREAD, args=(r2ow, queue, t_cnt,))
                    comlogging.logger.error("   내부Thread 전달건수:" + str(len(r2ow)) + '  ,Thread 기동건수-' + str(t_cnt))
                    thread_list.append(thread)
                    thread.start()
                queue_message_cnt=0
                loop_cnt=0

                while True:
                    time.sleep(0.1)
                    loop_cnt += 1

                    if loop_cnt % 10 == 0:
                        comlogging.logger.error("    메인프로세스 대기중..." + '잡완료건수:' + str(queue_message_cnt) + ' Thread: 갯수' + str(t_cnt))
                    if not queue.empty():
                        res = queue.get()
                        queue_message_cnt += 1
                    if queue_message_cnt == t_cnt:
                        comlogging.logger.error('  Thread 기동갯수:' + str(t_cnt)  + ' (Inner Thread 종료) job message:' + res  + ' ,큐 수신메시지건수:' + str(queue_message_cnt))
                        break
                for thread in thread_list:
                    thread.join

                queue.close()

    except Exception as err:
        comlogging.logger.error( 'ITF1002-'+ str(err))
        include.setErr('EITF1002', 'ITF1002' + str(err))

    else:
        comlogging.logger.info( 'ITF1002-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False

def child_exited(sig, frame):
    pid, exitcode = os.wait()
    print("Child process {pid} exited with code {exitcode}".format(pid=pid, exitcode=exitcode))


