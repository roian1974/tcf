import time
import os
import logging,logging.handlers
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.util.parser import comparser

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging

from src.com.sp_comrc.transfer import com1100CDTO, com9001CDTO
from src.com.sp_comrc.business.dc.dao import queryDAO
from src.com.sp_comrc.business.dc import dc_comrc
from src.com.sp_comrc.business.pc.mod import common
from src.com.fwk.business.util.dbms import comdbutil
from src.com.fwk.business.util.tpm import tpsutil


def COM9001():
    rtn = True
    try:
        comlogging.logger.info( "COM9001_start() start ")
        if COM9001_start() == True :
            comlogging.logger.info( "COM9001_processing() start ")
            COM9001_processing()
        else :
            raise Exception('COM9001_start 함수에서 에러가 발생')
    except Exception as err:
        comlogging.logger.error( 'COM9001-'+ str(err))
        include.setErr('ECOM9001', 'COM9001' + str(err))
    else:
        comlogging.logger.info( 'COM9001-성공')
    finally:
        COM9001_end()

        if include.isError() == False :
            return True
        else :
            return False

def COM9001_start() :
    try:
        # 클라이언트로 부터 수신한 데이타를 전달받는다.
        # com9001CDTO.COM9001CDTO_I[0] = (include.getIndata())[0]
        com9001CDTO.COM9001CDTO_I.append(include.gcominfo['indata'][0])
        print('----com9001CDTO.COM9001CDTO_I[0]-------------------',com9001CDTO.COM9001CDTO_I[0])
        comlogging.logger.info("COM9001_start() start " )

    except Exception as err:
        comlogging.logger.error( 'COM9001_start-' + str(err))
        include.setErr('ECOM9001', 'COM9001_start,' + str(err))
    else:
        comlogging.logger.info( 'COM9001_start-성공')
    finally:
        print("--------COM9001_start success")
        if include.isError() == False :
            print('----True')
            return True
        else :
            print('----Error')
            return False

def COM9001_processing() :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        # r2ow = com9001CDTO.COM9001CDTO_I[0]
        r2ow = com9001CDTO.COM9001CDTO_I[0]

        rcnt = 0
        for r3ow in r2ow:
            rcnt += 1
            # print("--nlu call--", rcnt, "-------------------------------", r3ow[0], os.getpid())
            comlogging.logger.error("시작-" + str(rcnt) + " ======================================================================:" + r3ow[0])

            dic_response_s = nlu_sentiment(r3ow)
            if dic_response_s == False :
                comlogging.logger.error(" NLU(Sentiment) 호출실패:" + r3ow[0] )
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                dc_comrc.upsertDocument("update_document_01", [], tup)
                # include.setErr('ECOM9001', 'COM9001_processing nlu_sentiment 에러 ')
                continue

            dic_response_e = nlu_entity(r3ow)
            if dic_response_e == False :
                comlogging.logger.error(" NLU(Entity) 호출실패:" + r3ow[0])
                tup = [('X', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
                dc_comrc.upsertDocument("update_document_01", [], tup)
                # include.setErr('ECOM9001', 'COM9001_processing nlu_entity 에러 ')
                continue

            print("--save data--", rcnt, "-------------------------------", r3ow[0], os.getpid())
            if result_processing_document(dic_response_s) == False :
                txflag = False
                # raise Exception('result_processing_document exception 발생')
                # include.setErr('ECOM9001', 'COM9001_processing result_processing_document 에러 ')
                break

            if  result_processing_entity(dic_response_e) == False :
                txflag = False
                # print("#================================================",txflag)
                # raise Exception('result_processing_entity exception 발생')
                # include.setErr('ECOM9001', 'COM9001_processing result_processing_entity 에러 ')
                break



            tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0])]
            # tup = [('Y', comutil.getsysdate(), comutil.getsystime(), r3ow[0], getNo(r3ow[0]))]
            # if comdbutil.upsert("update_document_01", [], tup) == False:
            if dc_comrc.upsertDocument("update_document_01", [], tup) != True:
            # if dc_comrc.upsertDocument("update_document_02", [], tup) != True:
                include.setErr('ECOM9001', 'COM9001_processing upsertDocument 에러 ')
                break


        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'COM9001_processing '+ str(err) )
        include.setErr('ECOM9001', 'COM9001_processing,' + str(err))
        # print("-----err cd-",include.gcominfo['err_info']['err1cod'])
    else:
        comlogging.logger.info( 'COM9001_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def COM9001_end() :
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'COM9001_end '+ str(err))
        include.setErr('ECOM9001', 'COM9001_end,' + str(err))
    else:
        comlogging.logger.info( 'COM9001_end-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False
#-----------------------------------------------------------------------------------------------------------------------

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


def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())

def getNo(id) :
    sql = "select no,doc_id from document where doc_id=" + id
    conn = comdbutil.gdbmsSession[0]
    curs = conn.cursor()
    curs.execute(sql)
    rows = curs.fetchall()
    curs.close()

    return rows[0][0]
