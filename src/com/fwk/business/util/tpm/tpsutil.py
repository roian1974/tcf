# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 왓슨과 연동하기 위한 기본 모듈 탑재
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------

import os
import time
import logging,logging.handlers

from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.dbms import comdbutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions, EntitiesOptions

SUCCESS = 0
FAIL = -1

__USERNAME__ = "f842a62b-e902-4cd4-a443-239e49976f59"
__PASSWORD__ = "nDGL7hG4zQaO"
__VERSION__ = '2017-02-27'
# jurl "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",

gwatsonSession = [-1]

def tpsinit(pusername,ppasswd,pversion) :
    try:
        url = 'https://gateway.aibril-watson.kr/natural-language-understanding/api'
        rtn = True

        watsonSession = NaturalLanguageUnderstandingV1(
            username=pusername,
            password=ppasswd,
            version=pversion)
        {
            "url": url,
            "username": pusername,
            "password": ppasswd
        }
        watsonSession.set_url(url)

        global gwatsonSession
        gwatsonSession[0]=watsonSession

    except Exception as err:
        comlogging.logger.error('▲tpsinit()-ERR:'+ str(err))
        rtn = False
        # include.setErr('ETP001', '함수(tpsinit) 에러내용:' + str(err))
    else:
        comlogging.logger.info('▲tpsinit()-성공:'+ gwatsonSession)
    finally:
        return rtn

def tpsinit_processor() :

    username = include.getWatsonUserName()
    passwd = include.getWatsonPasswd()
    version = include.getWatsonVersion()

    try:
        rtn = True
        watsonSession = NaturalLanguageUnderstandingV1(
            username=username,
            password=passwd,
            version=version)
        {
            "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
            "username": username,
            "password": passwd
        }

        global gwatsonSession
        gwatsonSession[0] = watsonSession

    except Exception as err:
        comlogging.logger.error('▲tpsinit()-ERR:'+ str(err) + os.getpid())
        # include.setErr('ETP001', '함수(tpsinit_processor) 에러내용:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲tpsinit()-성공:'+ gwatsonSession + os.getpid())
    finally:
        return rtn

# senddata = 기사본문
# flag = sentiment , entity
# targets = [ 'sk', '에스케이', '주SK' ]
#
def tpssendrecv(flag, senddata, targets) :
    try:
        comlogging.logger.info('▲tpssendrecv()--송신전')
        rtn = True
        global gwatsonSession

        if flag == 'sentiment' :
            response = gwatsonSession[0].analyze(
                text=senddata,
                features=Features(sentiment=SentimentOptions(targets=targets)))

        elif flag == "entity" :

            response = gwatsonSession[0].analyze(
                text=senddata,
                features=Features(
                    entities=EntitiesOptions(
                        sentiment=True,
                        emotion=True,
                        limit=250)))
        else :
            comlogging.logger.info('▲tpssendrecv()-ERR-1:'+ 'flag not set-' + str(flag))
            raise Exception('함수(tpssendrecv) 에러내용:' + "flag not set")
    except Exception as err:
        comlogging.logger.error('▲tpssendrecv()-ERR-2:'+ str(err))
        # include.setErr('ETP003', '함수(tpssendrecv) 에러내용:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲tpssendrecv():성공-수신데이타['+ str(response) + ']')
    finally:
        comlogging.logger.info('▲tpssendrecv():end-'+ str(rtn))
        if rtn == False :
            return False
        else :
            return response

def interface_tpssendrecv(flag, senddata, targets) :
    rtn = SUCCESS
    try:
        # time.sleep(1)
        if flag == 'sentiment' :
            # watson call sentiment response data
            response = '{ \
            "usage": { "text_units": 1, "text_characters": 1188,  "features": 1  },  \
            "sentiment": {   \
                "targets": [   \
                    { "text": "stocks", "score": 0.279964, "label": "positive" },{ "text": "sk", "score": 0.379964, "label": "positive" }   \
                            ],    \
                "document": {      "score": 0.127034,      "label": "positive"    }  \
                        },  \
            "retrieved_url": "https://www.wsj.com/news/markets",  \
            "language": "en"} '
        elif flag == "entity" :
            response = '{ "usage": { "text_units": 1, "text_characters": 1536, "features": 1 }, \
                    "keywords": [ \
                        {   "text": "curated online courses", \
                            "sentiment": { "score": 0.792454  },\
                            "relevance": 0.864624, \
                            "emotions": {  \
                                "sadness": 0.188625,        \
                                "joy": 0.522781,        \
                                "fear": 0.12012,        \
                                "disgust": 0.103212,        \
                                "anger": 0.106669      }    \
                        },    \
                        {  "text": "free virtual server",      \
                            "sentiment": { "score": 0.664726  },      \
                            "relevance": 0.864593, \
                            "emotions": {  \
                                "sadness": 0.265225,  \
                                "joy": 0.532354, \
                                "fear": 0.07773, \
                                "disgust": 0.090112,  \
                                "anger": 0.102242  \
                                        } \
                        } \
                     ],  \
                    "language": "en", \
                    "retrieved_url": "https://www.ibm.com/us-en/", \
                    "entities" : [\
                        {   "type": "Company",                 \
                            "text": "CNN",                 \
                            "sentiment": {                     \
                                "score": 0.2,                     \
                                "label": "neutral"                 \
                                            },                 \
                            "emotions": {  \
                                "sadness": 0.265225,  \
                                "joy": 0.532354, \
                                "fear": 0.07773, \
                                "disgust": 0.090112,  \
                                "anger": 0.102242  \
                                    }, \
                    "relevance": 0.784947,                 \
                    "disambiguation": {                     \
                            "subtype": [ "Broadcast", "AwardWinner", "RadioNetwork", "TVNetwork" ], \
                            "name": "CNN",                    \
                            "dbpedia_resource": "http://dbpedia.org/resource/CNN"                \
                        },                \
                        "count": 9            \
                    }        \
                    ] \
                }'
        else :
            pass

    except Exception as err:
        comlogging.logger.error('▲tpssendrecv()-ERR:'+ str(err))
    else:
        comlogging.logger.info('▲tpssendrecv():성공')
    finally:
        return response

# work_flag = "insert"
# sql_id = "delete_doc_sentiment_07"
def tpbegin_1(work_flag,sql_id) :
    try :
        rtn = True
        if comdbutil.ibatisload() == False :
            raise Exception('ibatisload error')
        sql,parameter = comdbutil.getsql(work_flag, sql_id)
        if sql == False:
            comlogging.logger.info('getsql fail')
            raise Exception('getsql error')
    except Exception as err:
        rtn = False
        comlogging.logger.error('▲tpbegin_1()-ERR:' + str(err))
        # include.setErr('ETP004', '함수(tpbegin_1) 에러내용:' + str(err))
    else:
        comlogging.logger.info('▲tpbegin_1()-성공:')
    finally:

        if rtn == False :
            return False,False
        else :
            return sql,parameter

def tpbegin() :
    try :
        rtn = True
        host = include.getDBHost()
        user = include.getDBuser()
        password = include.getDBpasswd()
        db = include.getDBname()


        # rtn = comdbutil.dbinit(host, user, password, db)
        # if rtn == -1:
        #     comlogging.logger.error( "▲ dbconnect() call failed")
        #     include.setErr('ETP005', 'DB connect fail')
        # else:
        #     rtn = True
        #     comlogging.logger.info( "dbconnect() call success")
        #     include.gcominfo['dbconn'] = include.gdb
        #     include.gcominfo['dbconn'] = comdbutil.gdbmsSession
        #
        #     if comdbutil.ibatisload() == False :
        #         raise Exception('ibatisload시에 에러발생')

        if include.gtpbeginflag == 0 :
            conn = comdbutil.gdbmsSession[0]
            conn.begin()

            # sql = " select @@autocommit;"
            # curs = conn.cursor()
            # curs.execute(sql)
            # rows = curs.fetchall()
            # curs.close()

            if comdbutil.ibatisload() == False :
                raise Exception('ibatisload시에 에러발생')
        else:
            comlogging.logger.error('▲트랜잭션이 이미 시작되었다. :' + str(include.gtpbeginflag))

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲tpbegin()-실패 ERR:'+ str(err))
        # include.setErr('ETP006', '함수(tpbegin) 에러내용:' + str(err))
        include.gtpbeginflag = 0
    else:
        comlogging.logger.info('▲tpbegin()-성공:' + str(rtn))
        include.gtpbeginflag = 1
    finally:
        return rtn


def tpbegin_ty2() :
    try :
        rtn = True
        host = include.getDBHost()
        user = include.getDBuser()
        password = include.getDBpasswd()
        db = include.getDBname()

        if comdbutil.ibatisload() == False :
            raise Exception('ibatisload시에 에러발생')

    except Exception as err:
        rtn = False
        comlogging.logger.error('▲tpbegin()-실패 ERR:'+ str(err))
        # include.setErr('ETP006', '함수(tpbegin) 에러내용:' + str(err))
    else:
        comlogging.logger.info('▲tpbegin()-성공:' + str(rtn))
        pass
    finally:
        return rtn

def tpcommit() :
    try :
        # comlogging.logger.error('▲commit()-=====================start:')
        rtn = True
        conn = comdbutil.gdbmsSession[0]
        conn.commit()
    except Exception as err:
        comlogging.logger.error('▲tpcommit()-ERR:' + str(err))
        # include.setErr('ETP007', '함수(tpcommit) 에러내용:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲tpcommit()-성공:')
        # comlogging.logger.error('▲tpcommit()-성공:' + str(os.getpid()))
    finally:
        include.gtpbeginflag = 0
        return rtn

def tprollback() :
    try :
        # comlogging.logger.error('▲tprollback()-=====================start:' )
        rtn = True
        conn = comdbutil.gdbmsSession[0]
        conn.rollback()
    except Exception as err:
        comlogging.logger.error('▲tprollback()-ERR:'+ str(err))
        # include.setErr('ETP008', '함수(tprollback) 에러내용:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲tprollback()-성공:')
        # comlogging.logger.error('▲tprollback()-성공:'+ str(os.getpid()))
    finally:
        include.gtpbeginflag = 0
        return rtn

def tpenv() :
    try :
        rtn = True
        if include.getOSType() == 'Windows':
            filename = include.tcfenv_fname
        else :
            filename = include.tcfenv_fname_unix
        str=''
        f = open(filename)
        while True:
            line = f.readline()
            if line == '--endof' :
                break
            str = line.split("=")
            key = str[0]
            value = str[1].replace("\n","")
            include.gtcfenv[key] = value
            if not line: break
        f.close()
    except Exception as err:
        rtn = False
        comlogging.logger.error('▲tpenv()-ERR:' + str(err))
        # include.setErr('ETP009', '함수(tpenv) 에러내용:' + str(err))
    else:
        comlogging.logger.info('▲tpenv()-성공:')
    finally:
        return rtn

def tpenv2() :
    # filename = "C:\jDev\MyWorks\PycharmProjects\Roian\\bin\\tcf.env"
    filename = include.tcfenv_fname
    str=''
    with open(filename) as f:
        lines = f.readlines()
        lines = lines.replace('\n','')

    comlogging.logger.info(lines)

def test() :
    from watson_developer_cloud import NaturalLanguageUnderstandingV1
    import watson_developer_cloud.natural_language_understanding.features.v1 as Features

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username="f842a62b-e902-4cd4-a443-239e49976f59",
        password="nDGL7hG4zQaO",
        version="2017-02-27")

    {
        "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
        "username": "f842a62b-e902-4cd4-a443-239e49976f59",
        "password": "nDGL7hG4zQaO"
    }

    # f1 = open('C:\\Users\\05455\\Documents\\NLU-PRAC2\\기사1.txt','rt')   # 파일 오픈
    # doc = f1.read()                                                      # 파일내용 읽기
    doc = "I am a boy. I go to school."
    response = natural_language_understanding.analyze(
        text=doc,
        features=[
            Features.Sentiment(
                targets=[]
            )
        ]
    )
    comlogging.logger.info(doc)  # 파일내용 출력
    # comlogging.logger.info(json.dumps(response, indent=2))  # NLU 결과출력






