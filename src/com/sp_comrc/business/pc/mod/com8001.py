import time
import os
import json
import signal
from multiprocessing import Queue
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil

from src.com.sp_comrc.business.dc import dc_comrc
from src.com.sp_comrc.business.pc.mod import call_subprocessor
from src.com.fwk.business.util.dbms import comdbutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.util.parser import comparser




gCallCnt=0
myLock = threading.Lock()

def COM8001() :
    rtn = True
    try:

        while True :
            time.sleep(3)

            comlogging.logger.info("")
            comlogging.logger.info("")
            comlogging.logger.info("================================================================MAIN 기동")
            comlogging.logger.info( "COM8001_start() start ")
            comlogging.logger.info("")
            comlogging.logger.info("")

            rtn = tpsutil.tpbegin()
            if rtn == False:
                print('tpbegin fail')
                tpsutil.tprollback()
                comdbutil.dbclose()
                comdbutil.dbinit_conn()
                continue

            parameter=[]
            rows = dc_comrc.queryDocument("select_document_01", parameter)

            tpsutil.tprollback()

            thread_list = []
            queue = Queue()

            if rows == False or rows == 1403 :
                comlogging.logger.error('select_document_01')
                continue
            else:
                print('1.document read count in "N"(', len(rows),')')
                if len(rows) == 0:
                    raise Exception("Data Not Found-2")

                thread_cnt = int( include.gcominfo['sysargv'][3])
                job_r2ows = call_subprocessor.divide_task(rows, thread_cnt)

                if include.getOSType() != 'Windows':
                    signal.signal(signal.SIGCHLD, child_exited)

                comlogging.logger.error('▲ 전체건수:' + str(len(rows)) + " ,루핑건수:" + str(len(job_r2ows)))
                t_cnt=0
                processor_list = []

                # executor.submit(load_url, url, 60), url)     for url in URLS)
                #
                # with ProcessPoolExecutor() as executor:
                #     for r2ow in job_r2ows :
                #         t_cnt += 1
                #         processor = zip(r2ow, executor.map(subprocessor_exe,r2ow, queue,t_cnt))
                #         comlogging.logger.error("   내부Processor 전달건수:" + str(len(r2ow)) + '  ,Processor 기동건수-' + str(t_cnt))
                #         processor_list.append(processor)
                #         # processor.start()

                queue_message_cnt=0
                loop_cnt=0

                while True:
                    time.sleep(0.3)
                    loop_cnt += 1

                    # 3시간 이상 작업
                    if loop_cnt % 10 == 0:
                        comlogging.logger.error(
                            "    메인프로세스 대기중..." + '잡완료건수:' + str(queue_message_cnt) + ' Thread: 갯수' + str(t_cnt))

                    if not queue.empty():
                        res = queue.get()
                        queue_message_cnt += 1

                    if queue_message_cnt == t_cnt:
                        comlogging.logger.error('  Thread 기동갯수:' + str(t_cnt)  + ' (Inner Thread 종료) job message:' + res  + ' ,큐 수신메시지건수:' + str(queue_message_cnt))
                        break

                for thread in thread_list:
                    thread.join

                queue.close()

        comlogging.logger.info("############" + str(time.mktime(time.localtime())))

    except Exception as err:
        comlogging.logger.error( 'COM8001-'+ str(err))
        include.setErr('ECOM8001', 'COM8001' + str(err))

    else:
        comlogging.logger.info( 'COM8001-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False

def child_exited(sig, frame):
    pid, exitcode = os.wait()
    print("Child process {pid} exited with code {exitcode}".format(pid=pid, exitcode=exitcode))

#-----------------------------------------------------------------------------------------------------------------------

def subprocessor_exe(r2ow,queue,name) :

    try :
        global gCallCnt
        txflag = True
        rtn = True

        tpsutil.tpenv()

        cnt=0

        fname_ds = 'doc_sentiment_' + comutil.getsysdate() + comutil.getsystime() + '.txt'
        fname_ts = 'target_sentiment_' + comutil.getsysdate() + comutil.getsystime()  + '.txt'

        txflag = True

        for r3ow in r2ow:

            cnt += 1
            gCallCnt += 1
            comlogging.logger.error("Thread["+str(name) + "] " + str(gCallCnt) + ' ' + str(cnt) +" =============================:" + r3ow[0])
            dic_response_s = nlu_sentiment(r3ow)
            nlu_flag=True

            if dic_response_s == False  :
                comlogging.logger.error("Thread["+str(name) + "]" +" NLU(Sentiment) 호출실패:" + r3ow[0])
                nlu_flag = False
            else :
                dic_response_e = nlu_entity(r3ow)
                if dic_response_e == False :
                    comlogging.logger.error("Thread["+str(name) + "]" +" NLU(Entity) 호출실패:" + r3ow[0])
                    nlu_flag = False

            #-----------------------------------------------------------------------------------------------------------
            # 하나의 쓰레드만이 진입을 허용한다.
            # -----------------------------------------------------------------------------------------------------------

            comlogging.logger.error("Thread[" + str(name) + "]" + " gtpbeginflag=" + str(include.gtpbeginflag))
            while True :
                time.sleep(0.5)

                if include.gtpbeginflag == 1 :
                    comlogging.logger.error("Thread[" + str(name) + "]" + " gtpbeginflag=" + str(include.gtpbeginflag))
                    continue
                else :
                    break

            txbegin()

            if nlu_flag == False :
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                dc_comrc.upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                continue

            if result_processing_document(dic_response_s) == False :
                txflag = False
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                dc_comrc.upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                break

            if  result_processing_entity(dic_response_e) == False :
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                dc_comrc.upsertDocument("update_document_01", [], tup)
                tpsutil.tpcommit()
                break

            tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
            if comdbutil.upsert("update_document_01", [], tup) == False:
                txflag = False

            tpsutil.tpcommit()
            # -----------------------------------------------------------------------------------------------------------


    except Exception as err:
        comlogging.logger.error('▲subprocessor_function()-ERR:'+ str(err))
        txflag = False
        rtn = False
        tpsutil.tprollback()
    else:
        comlogging.logger.info('▲subprocessor_function()-성공:')
    finally:

        queue.put(str(os.getpid()) + ' job end')

        return rtn


def txbegin() :
    myLock.acquire(True)
    include.gtpbeginflag =0
    tpsutil.tpbegin()
    myLock.release()



def nlu_sentiment(r3ow) :
    rtn = False

    if len(r3ow) == 0:
        return False

    doc_id = r3ow[0]
    doc_content = r3ow[1]
    # print('docid-', os.getpid(), doc_id)
    # print('document-', os.getpid(), doc_content)

    # print('tpcsendrecv-senddata-',doc_content)
    dic = dict()
    nluResult = tpsutil.tpssendrecv('sentiment', doc_content, [])
    # nluResult = tpsutil.interface_tpssendrecv('sentiment', doc_content, [])

    if nluResult == include.FAIL or nluResult == False :
        comutil.ferrprint(__file__, 'call_watson_processing', 'tpssendrecv 에러가 발생')
        # include.setErr('EDE0059', 'call_watson_processing()' + 'tpssendrecv 에러가 발생')
        return False
    # print('tpcsendrecv-recvdata-', nluResult)

    dic['docid'] = doc_id
    dic['response'] = nluResult
    return dic

def nlu_entity(r3ow) :
    rtn = False

    if len(r3ow) == 0:
        return False

    doc_id = r3ow[0]
    doc_content = r3ow[1]
    # print('docid-', os.getpid(), doc_id)
    # print('document-', os.getpid(), doc_content)

    # print('tpcsendrecv-senddata-',doc_content)

    dic = dict()
    nluResult = tpsutil.tpssendrecv('entity', doc_content, [])
    # nluResult = tpsutil.interface_tpssendrecv('entity', doc_content, [])
    if nluResult == include.FAIL or nluResult == False:
        comutil.ferrprint(__file__, 'call_watson_processing', 'tpssendrecv 에러가 발생')
        # include.setErr('EDE0059', 'call_watson_processing()' + 'tpssendrecv 에러가 발생')
        return False
    # print('tpcsendrecv-recvdata-', nluResult)

    dic['docid'] = doc_id
    dic['response'] = nluResult
    return dic


def result_processing_document(dic) :
    try :
        rtn = True
        date = comutil.getsysdate()
        tm = comutil.getsystime()
        doc_id = dic['docid']
        response = dic['response']

        sudata_s, sudata_t = comparser.parser_sentiment(doc_id, response)

        for value in sudata_s:
            docid = value['docid']
            score = value['score']
            label = value['label']
            tup = [(docid, score, label, include.gtcfenv['watson_version'], 'N', date, tm, date, tm)]
            # if comdbutil.upsert("insert_doc_sentiment_01", [], tup) == True:
            # if queryDAO.upsertDocument("insert_doc_sentiment_01", [], tup) == True:
            if dc_comrc.upsertDocument("insert_doc_sentiment_01", [], tup) == True:
                print('insert insert_doc_sentiment_01- doc_sentiment success')
            else :
                raise Exception('insert_doc_sentiment_01 update error')
                break

    except Exception as err:
        print('▲result_processing_document()-ERR:', str(err))
        rtn = False
    else:
        print('▲result_processing_document()-성공:')
    finally:
        return rtn

def result_processing_entity(dic) :
    try :
        rtn = True
        date = comutil.getsysdate()
        tm = comutil.getsystime()

        #----------------------------------------------------------------------------------------------------------------
        doc_id = dic['docid']
        response = dic['response']

        # sudata_s : 기업에 대한 감성
        sudata_s, sudata_e, sudata_y = comparser.parser_entity(doc_id, response)
        # print('sudata-s', str(sudata_s))

        for value in sudata_s:
            if 'docid' not in value:
                doc_id = "DOCXXX"
            else:
                doc_id = value['docid']

            if 'type' not in value:
                type = 'XXXX'
            else:
                type = value['type']

            if 'text' not in value:
                text = 'XXXX'
            else:
                text = value['text']
                text = text.encode('utf-8')
                text = text.decode('utf-8')

            if 'score' not in value:
                score = 0.0
            else:
                score = value['score']

            if 'label' not in value:
                label = 'XXXX'
            else:
                label = value['label']

            if 'sadness' not in value:
                sadness = 0.0
            else:
                sadness = value['sadness']

            if 'joy' not in value:
                joy = 0.0
            else:
                joy = value['joy']

            if 'fear' not in value:
                fear = 0.0
            else:
                fear = value['fear']

            if 'disgust' not in value:
                disgust = 0.0
            else:
                disgust = value['disgust']

            if 'anger' not in value:
                anger = 0.0
            else:
                anger = value['anger']

            if 'subtype' not in value:
                subtype = 'XXXX'
            else:
                subtype = value['subtype']
                if len(subtype) == 0 :
                    subtype = 'XXXX'
                else :
                    v=''
                    ii=0
                    for r in subtype :
                        if ii == 0 :
                            v = r
                        else :
                            v = "%s,%s" % (v,r)
                    subtype = v

            if 'count' not in value:
                count = 0
            else:
                count = value['count']

            tup = [ (doc_id, text, type, str(score), label, str(sadness), str(joy), str(fear), str(disgust), str(anger), subtype, str(count), 'N', date, tm, date, tm) ]
            # if comdbutil.upsert("insert_target_sentiment_02", [], tup) == True:
            if dc_comrc.upsertDocument("insert_target_sentiment_02", [], tup) == True:
                print('insert insert_target_sentiment_02- target_sentiment success')
            else:
                print('▲result_processing_entity()-ERR:Not Exception', os.getpid())
                raise Exception('insert_target_sentiment_02 update error')
        #----------------------------------------------------------------------------------------------------------------
    except Exception as err:
        print('▲result_processing_entity()-ERR:', str(err),os.getpid())
        rtn = False
    else:
        print('▲result_processing_entity()-성공:',os.getpid())
    finally:
        return rtn
