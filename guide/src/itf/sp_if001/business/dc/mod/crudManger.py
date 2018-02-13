import os, time, threading
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.itf.sp_if001.business.dc.dao import queryDAO,watsonDAO
from src.com.fwk.business.util.parser import comparser
from src.com.fwk.business.util.dbms import comdbutil


def saveDocsentiment(dic) :
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
            if comdbutil.upsert("insert_doc_sentiment_01", [], tup) == False:
                pass
            else :
                raise Exception('insert_doc_sentiment_01 update error')
                break

    except Exception as err:
        rtn = False
    else:
        pass
    finally:
        return rtn

def saveTargetsentiment(dic) :
    try :
        rtn = True
        date = comutil.getsysdate()
        tm = comutil.getsystime()

        doc_id = dic['docid']
        response = dic['response']

        sudata_s, sudata_e, sudata_y = comparser.parser_entity(doc_id, response)

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
            if comdbutil.upsert("insert_target_sentiment_02", [], tup) == False:
                pass
            else:
                raise Exception('insert_target_sentiment_02 update error')
    except Exception as err:
        rtn = False
    else:
        pass
    finally:
        return rtn
