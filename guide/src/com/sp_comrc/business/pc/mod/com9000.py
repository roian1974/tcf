import time
import os
import signal
from multiprocessing import Process
from multiprocessing import Queue

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil

from src.com.sp_comrc.transfer import com1100CDTO
from src.com.sp_comrc.business.dc.dao import queryDAO
from src.com.sp_comrc.business.dc import dc_comrc
from src.com.sp_comrc.business.pc.mod import call_subprocessor



def COM9000() :
    rtn = True
    try:
        comlogging.logger.info( "COM9000_start() start ")


        while True:

            time.sleep(2)

            comlogging.logger.info("=============================================================================")
            comlogging.logger.info("#                                                                            ")
            comlogging.logger.info("#                                                                            ")
            comlogging.logger.info("#                 MAIN START                                                 ")
            comlogging.logger.info("#                                                                            ")
            comlogging.logger.info("#                                                                            ")
            comlogging.logger.info("#                                                                            ")
            comlogging.logger.info("=============================================================================")


            comlogging.logger.info("##########" + str(time.mktime(time.localtime())))
            rtn = tpsutil.tpbegin()
            # rtn = tpsutil.tpbegin_ty2()
            if rtn == False:
                print('tpbegin fail')
                continue

            parameter=[]
            rows = dc_comrc.queryDocument("select_document_01", parameter)
            if rows == False or rows == 1403 :
                comlogging.logger.error('select_document_01')
                time.sleep(1)
                tpsutil.tprollback()
            else:
                print('1.document read count in "N"(', len(rows),')')
                if len(rows) == 0:
                    continue

                # 3건단위로 리스트를 작성해서 Processor에 할당한다.
                per_data_processing = int(include.gcominfo['sysargv'][3])
                job_r2ows = call_subprocessor.divide_task(rows, per_data_processing)
                processor_list = []
                queue = Queue()
                processor_cnt = 0

                if include.getOSType() != 'Windows':
                    signal.signal(signal.SIGCHLD, child_exited)

                comlogging.logger.error( '▲ 전체건수:' +  str(len(rows) ) + " ,루핑건수:"  + str(len(job_r2ows)) )
                for r2ow in job_r2ows :
                    # com1100CDTO.COM1100CDTO_I.append(r2ow)
                    # com1100CDTO.COM1100CDTO_I.append(queue)

                    if per_data_processing == 1 :
                        time.sleep(5)

                    comlogging.logger.error("   내부프로세스 전달건수(r2ow ):" + str(len(r2ow)) + '  ,프로세스 기동건수-' + str(processor_cnt))
                    processor = Process(target=call_subprocessor.subprocessor_ty2, args=(r2ow, queue,))

                    # 성공한 프로세스 모델
                    # processor = Process(target=call_subprocessor.subprocessor_function, args=(r2ow, queue,))

                    processor_list.append(processor)
                    processor.start()
                    processor_cnt += 1

                queue_message_cnt=0
                loop_cnt=0
                while True :
                    time.sleep(0.1)
                    loop_cnt += 1
                    # print("3.main_queue waiting....main processor..", os.getpid(), '-que', queue_message_cnt, '-pro', processor_cnt)

                    if loop_cnt % 30 == 0 :
                        comlogging.logger.error(
                            "    메인프로세스 대기중..." + '잡완료건수:' + str(queue_message_cnt) + ' 프로세스대상건수:' + str(processor_cnt))

                    q_res = ''
                    if not queue.empty() :
                        q_res = queue.get()
                        queue_message_cnt += 1
                        # print('3.1 main_queue message..[', q_res, '] processor_cnt-', processor_cnt, 'queue_message_cnt-', queue_message_cnt)

                    if queue_message_cnt == processor_cnt :
                        comlogging.logger.error(
                            '  (이너 프로세스 종료) job message:' + q_res + ', 프로세스 기동건수:' + str(processor_cnt) + ' ,큐수신메시지건수:' + str(
                                queue_message_cnt))
                        break

                for processor in processor_list:
                    processor.join

                queue.close()
                comlogging.logger.error( '  (메인프로세스 종료)......')
                tpsutil.tpcommit()


            comlogging.logger.info("############" + str(time.mktime(time.localtime())))

    except Exception as err:
        comlogging.logger.error( 'COM9000-'+ str(err))
        include.setErr('ECOM9000', 'COM9000' + str(err))

    else:
        comlogging.logger.info( 'COM9000-성공')
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

