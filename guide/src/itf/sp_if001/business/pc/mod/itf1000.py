import time
import os
import signal
from multiprocessing import Process
from multiprocessing import Queue
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.itf.sp_if001.business.dc import dc_if001
from src.com.fwk.business.tcf import tcf_sp_commo

#-----------------------------------------------------------------------------------------------------------------------
# Wastson 관련 인터페이스 담당하는 컴포넌트 서비스 ... sk c&c roian..2018-02-01
# 멀티프로세스 형태로 제작 데몬형 서비스 제공
# ITF1000 - ITF1001은 PAIR 서비스 형태이다.
#-----------------------------------------------------------------------------------------------------------------------

# python mn_sp_if001.py sp_if001 ITF1000 3(프로세스갯수)
# python mn_sp_if001.py sp_if001 ITF1000 1(프로세스갯수) : 1인 경우는 3초단위로 프로세스 하나씩 포커시면서 처리한다.

def ITF1000() :
    rtn = True
    try:
        comlogging.logger.info( "ITF1000_start() start ")

        while True:
            time.sleep(2)
            comlogging.logger.info("=============================================================================")
            comlogging.logger.info("#                                MAIN START                                  ")
            comlogging.logger.info("=============================================================================")
            comlogging.logger.info("##########" + str(time.mktime(time.localtime())))
            rtn = tpsutil.tpbegin()
            if rtn == False:
                print('tpbegin fail')
                continue
            parameter=[]
            rows = dc_if001.queryDocument("select_document_01", parameter)
            if rows == False or rows == 1403 :
                comlogging.logger.error('select_document_01')
                time.sleep(1)
                tpsutil.tprollback()
            else:
                if len(rows) == 0:
                    continue
                per_data_processing = int(include.gcominfo['sysargv'][3])
                job_r2ows = dc_if001.divide_task(rows, per_data_processing)
                processor_list = []                
                queue = Queue()                
                processor_cnt = 0
                if include.getOSType() != 'Windows':
                    signal.signal(signal.SIGCHLD, child_exited)
                comlogging.logger.error( '▲ 전체건수:' +  str(len(rows) ) + " ,루핑건수:"  + str(len(job_r2ows)) )
                for r2ow in job_r2ows :
                    if per_data_processing == 1 :
                        time.sleep(3)
                    comlogging.logger.error("   내부프로세스 전달건수(r2ow ):" + str(len(r2ow)) + '  ,프로세스 기동건수-' + str(processor_cnt))
                    processor = Process(target=subprocessor_function, args=(r2ow, queue,))
                    processor_list.append(processor)
                    processor.start()
                    processor_cnt += 1
                queue_message_cnt=0
                loop_cnt=0
                while True :
                    time.sleep(0.1)
                    loop_cnt += 1
                    if loop_cnt % 30 == 0 :
                        comlogging.logger.error("    메인프로세스 대기중..." + '잡완료건수:' + str(queue_message_cnt) + ' 프로세스대상건수:' + str(processor_cnt))
                    q_res = ''
                    if not queue.empty() :
                        q_res = queue.get()
                        queue_message_cnt += 1
                    if queue_message_cnt == processor_cnt :
                        comlogging.logger.error('  (이너 프로세스 종료) job message:' + q_res + ', 프로세스 기동건수:' + str(processor_cnt) + ' ,큐수신메시지건수:' + str(queue_message_cnt))
                        break
                for processor in processor_list:
                    processor.join
                queue.close()
                comlogging.logger.error( '  (메인프로세스 종료)......')
                tpsutil.tpcommit()
            comlogging.logger.info("############" + str(time.mktime(time.localtime())))
    except Exception as err:
        comlogging.logger.error( 'ITF1000-'+ str(err))
        include.setErr('EITF1000', 'ITF1000' + str(err))

    else:
        comlogging.logger.info( 'ITF1000-성공')
    finally:
        queue.close()
        if include.isError() == False :
            return True
        else :
            return False

def child_exited(sig, frame):
    pid, exitcode = os.wait()
    print("Child process {pid} exited with code {exitcode}".format(pid=pid, exitcode=exitcode))

def subprocessor_function(r2ow,queue) :
    rtn = True
    try:
        argv = ['tcf_sp_commo', 'sp_if001', 'ITF1001', r2ow ]
        tcf_sp_commo.main(argv)
    except Exception as err:
        comlogging.logger.error( 'subprocessor-'+ str(err))
        include.setErr('EITF001', 'subprocessor' + str(err))
    else:
        pass
    finally:
        queue.put(str(os.getpid()) + ' job end')
        if include.isError() == False :
            return True
        else :
            return False
