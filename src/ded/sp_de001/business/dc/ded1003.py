import time
import os
from multiprocessing import Process
from multiprocessing import Queue

from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.parser import comparser
from src.com.fwk.business.util.dbms import comdbutil


#----------------------------------------------------------------------------------------------------------------------
def DED1003():
    rtn_val = include.SUCCESS
    try:
        comutil.fprint(__file__, "DED1003_start() start ")
        rtn_val = DED1003_start()
        comutil.fprint(__file__, "DED1003_start() end ")

        if rtn_val  == include.SUCCESS :
            rtn_val = DED1003_processing()

    except Exception as err:
        comutil.ferrprint(__file__, 'ded1003', str(err))
        include.setErr('EDE030', 'ded1003' + str(err))
        rtn_val = include.FAIL
    else:
        comutil.fsusprint(__file__, 'ded1003', '성공')
        rtn_val = include.SUCCESS
    finally:
        DED1003_end()
        return rtn_val

def DED1003_start() :
    rtn_val = 0
    try:
        pass

    except Exception as err:
        comutil.ferrprint(__file__, 'DED1003_start', str(err))
        include.setErr('EDE041', 'DED1003_start,' + str(err))
        rtn_val = include.FAIL
    else:
        comutil.fsusprint(__file__, 'DED1003_start', '성공')
        rtn_val = include.SUCCESS
    finally:
        return rtn_val

def DED1003_processing() :
    rtn_val = include.FAIL

    try:
        while True:
            time.sleep(5)
            print("#################################################################", time.mktime(time.localtime()))
            rtn = tpsutil.tpbegin()
            if rtn == False:
                print('tpbegin fail')

            parameter=[]
            rows = comdbutil.select_sqlid("fetchall", "select_document_01", parameter)
            if rows == False:
                print('select fail')
            else:
                #------------------------------------------------------------------------------------------------------
                # fetch 된 데이타를 1000건 단위로 분배한다.
                #------------------------------------------------------------------------------------------------------
                print('1.document read count in "N"(', len(rows),')')
                if len(rows) == 0:
                    continue

                # 3건단위로 리스트를 작성해서 Processor에 할당한다.
                r2ows = divide_rows(rows,3)
                procs = []
                queue = Queue()
                pcnt = 0
                for r2ow in r2ows :
                    print('=Pcall')
                    proc = Process(target=subprocessor_function, args=(r2ow,queue,))
                    procs.append(proc)
                    proc.start()
                    pcnt += 1
                mcnt=0
                lcnt=0
                while True :
                    print("3.queue waiting....")
                    time.sleep(1)
                    lcnt += 1

                    # 3시간 이상 작업
                    if lcnt == (3600 * 3) :
                        break
                    if not queue.empty() :
                        res = queue.get()
                        mcnt += 1
                        print('3.1 queue message..[', res, '] pcnt-', pcnt, 'mcnt-', mcnt)
                    if mcnt == pcnt :
                        break

                for proc in procs:
                    proc.join

                queue.close()


        # 엑셀파일 하나당 작업을 시작합니다.
        print("#################################################################", time.mktime(time.localtime()))
    except Exception as err:
        comutil.ferrprint(__file__, 'DED1003_processing', str(err))
        include.setErr('EDE042', 'DED1003_processing,' + str(err))
        rtn_val = include.FAIL
    else:
        comutil.fsusprint(__file__, 'DED1003_processing', '성공')
        rtn_val = include.SUCCESS
    finally:
        return include.SUCCESS

def DED1003_end() :
    rtn_val = include.FAIL
    try:
        pass
    except Exception as err:
        comutil.ferrprint(__file__, 'DED1003_end', str(err))
        include.setErr('EDE043', 'DED1003_end,' + str(err))
        rtn_val = include.FAIL
    else:
        comutil.fsusprint(__file__, 'DED1003_end', '성공')
        rtn_val = include.SUCCESS
    finally:
        return rtn_val

#-----------------------------------------------------------------------------------------------------------------------
# 여기서 부터 모듈을 작성하세요
#-----------------------------------------------------------------------------------------------------------------------

def call_watson(a,b) :
    print("---", 'watson call', a, b)
    return True

def divide_rows(rows,cutting_rows) :

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

def start_subprocess(r2ow) :
    procs = []
    proc = Process(target=function, args=(r2ow,))
    procs.append(proc)
    proc.start()

    for proc in procs :
        proc.join

def subprocessor_function (r2ow,queue) :

    try :
        rcnt = False
        txflag = True

        tpsutil.tpenv()

        rtn = tpsutil.tpbegin()
        if rtn == False:
            queue.put(str(os.getpid()) + ' job end')
            print('tpbegin fail-', os.getpid())
            raise Exception('tpbegin error')

        rtn = tpsutil.tpsinit_processor()
        if rtn == False:
            queue.put(str(os.getpid()) + ' job end')
            print('tpsinit_processor fail-', os.getpid())
            raise Exception('tpsinit_processor error')

        for r3ow in r2ow:
            rcnt += 1
            print("--nlu call--", rcnt, "-------------------------------", r3ow[0], os.getpid())

            dic_response_s = nlu_sentiment(r3ow)
            if dic_response_s == False :
                continue

            dic_response_e = nlu_entity(r3ow)
            if dic_response_e == False :
                continue

            print("--save data--", rcnt, "-------------------------------", r3ow[0], os.getpid())
            if result_processing_document(dic_response_s) == False :
                txflag = False
                break

            if  result_processing_entity(dic_response_e) == False :
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

        if txflag == True :
            tpsutil.tpcommit()
        else:
            tpsutil.tprollback()

        queue.put(str(os.getpid()) + ' job end')

        return rtn

def function (r2ow,queue) :

    try :
        rcnt = False
        tpsutil.tpenv()

        rtn = tpsutil.tpbegin()
        if rtn == False:
            queue.put(str(os.getpid()) + ' job end')
            print('tpbegin fail-', os.getpid())
            return False

        rtn = tpsutil.tpsinit_processor()
        if rtn == False:
            queue.put(str(os.getpid()) + ' job end')
            print('tpsinit_processor fail-', os.getpid())
            return False

        for r3ow in r2ow:
            print("--sentiment---------------------------------", r3ow[0], os.getpid())
            rcnt += 1
            print("\t2.1 call watson-sentiment(", rcnt, ")", os.getpid())
            dic_response = nlu_sentiment(r3ow)
            if dic_response != False :
                print("\t2.2 dbms update(", rcnt, ")", os.getpid())
                result_processing_document(dic_response)

    except Exception as err:
        print('▲subprocessor_function()-ERR:', str(err),os.getpid())
    else:
        print('▲subprocessor_function()-성공:',os.getpid())
    finally:
        queue.put(str(os.getpid()) + ' job end')
        tpsutil.tpcommit()
        return True


def nlu_sentiment(r3ow) :
    rtn = False

    if len(r3ow) == 0:
        return False

    doc_id = r3ow[0]
    doc_content = r3ow[1]
    # print('docid-', os.getpid(), doc_id)
    # print('document-', os.getpid(), doc_content)

    dic = dict()
    nluResult = tpsutil.tpssendrecv('sentiment', doc_content, [])
    if nluResult == include.FAIL:
        comutil.ferrprint(__file__, 'call_watson_processing', 'tpssendrecv 에러가 발생')
        include.setErr('EDE0059', 'call_watson_processing()' + 'tpssendrecv 에러가 발생')
        return False
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

    dic = dict()
    nluResult = tpsutil.tpssendrecv('entity', doc_content, [])
    if nluResult == include.FAIL:
        comutil.ferrprint(__file__, 'call_watson_processing', 'tpssendrecv 에러가 발생')
        include.setErr('EDE0059', 'call_watson_processing()' + 'tpssendrecv 에러가 발생')
        return False
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
            if comdbutil.upsert("insert_doc_sentiment_01", [], tup) == True:
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
            if comdbutil.upsert("insert_target_sentiment_02", [], tup) == True:
                print('insert insert_target_sentiment_02- target_sentiment success')
            else:
                print('▲result_processing_entity()-ERR:Not Exception', os.getpid())
                raise Exception('insert_doc_sentiment_01 update error')
        #----------------------------------------------------------------------------------------------------------------
    except Exception as err:
        print('▲result_processing_entity()-ERR:', str(err),os.getpid())
        rtn = False
    else:
        print('▲result_processing_entity()-성공:',os.getpid())
    finally:
        return rtn

def update_dbsession() :
    host = include.gtcfenv['db_host']
    user = include.gtcfenv['db_user']
    password = include.gtcfenv['db_password']
    db = include.gtcfenv['db_dbname']
    comdbutil.dbinit(host, user, password, db)








