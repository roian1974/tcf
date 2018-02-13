import os
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

gwatsonSession = [-1]

def tpsinit(pusername,ppasswd,pversion) :
    rtn = SUCCESS
    try:
        watsonSession = NaturalLanguageUnderstandingV1(
            username=pusername,
            password=ppasswd,
            version=pversion)
        {
            "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
            "username": pusername,
            "password": ppasswd
        }

        global gwatsonSession
        gwatsonSession[0]=watsonSession

    except Exception as err:
        print('▲tpsinit()-ERR:', str(err))
        include.setErr('ETP001', '함수(tpsinit) 에러내용:' + str(err))
        rtn = FAIL
    else:

        print('▲tpsinit()-성공:', gwatsonSession)
    finally:
        if rtn == FAIL:
            return FAIL
        else:
            return SUCCESS

def tpsinit_processor() :

    username = include.gtcfenv['watson_user']
    passwd = include.gtcfenv['watson_password']
    version = include.gtcfenv['watson_version']

    rtn = True
    try:
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
        print('▲tpsinit()-ERR:', str(err),os.getpid())
        rtn = False
    else:
        print('▲tpsinit()-성공:', gwatsonSession, os.getpid())
    finally:
        return rtn

# senddata = 기사본문
# flag = sentiment , entity
# targets = [ 'sk', '에스케이', '주SK' ]
#
def tpssendrecv(flag, senddata, targets) :
    rtn = SUCCESS
    try:
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

            # response = gwatsonSession[0].analyze(
            #     text=senddata,
            #     features=Features(semantic_roles=SemanticRolesOptions(), entities=EntitiesOptions())
            # )

            # response = gwatsonSession[0].analyze(
            #     text=senddata,
            #     features=Features(entities=EntitiesOptions())
            # )

        else :
            print('▲tpssendrecv()-ERR-1:', 'flag not set-',flag)
            include.setErr('ETP002', '함수(tpssendrecv) 에러내용:' + "flag not set")
            return FAIL
    except Exception as err:
        print('▲tpssendrecv()-ERR-2:', str(err))
        include.setErr('ETP003', '함수(tpssendrecv) 에러내용:' + str(err))
        rtn = FAIL
    else:
        print('▲tpssendrecv():성공-수신데이타[',response,']')
    finally:
        if rtn == FAIL:
            return FAIL
        else:
            return response

def interface_tpssendrecv(flag, senddata, targets) :
    rtn = SUCCESS
    try:
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
        print('▲tpssendrecv()-ERR:', str(err))
    else:
        print('▲tpssendrecv():성공')
    finally:
        return response

# work_flag = "insert"
# sql_id = "delete_doc_sentiment_07"
def tpbegin_1(work_flag,sql_id) :
    try :
        if comdbutil.ibatisload() == False :
            return  False,False
        sql,parameter = comdbutil.getsql(work_flag, sql_id)
        if sql == False:
            print('getsql fail')
            return False,False
    except Exception as err:
        print('▲tpbegin()-ERR:', str(err))
        return False,False
    else:
        print('▲tpbegin()-성공:')
    finally:
        return sql,parameter

def tpbegin() :
    try :
        host = include.gtcfenv['db_host']
        user = include.gtcfenv['db_user']
        password = include.gtcfenv['db_password']
        db = include.gtcfenv['db_dbname']

        print('-----------------------------')
        print(host, user, password, db)
        print('-----------------------------')

        rtn = comdbutil.dbinit(host, user, password, db)
        if rtn == -1:
            comutil.fprint(__file__, "▲ dbconnect() call failed")
            include.setErr('ECOM002', 'DB connect fail')
            return -1
        else:
            comutil.fprint(__file__, "dbconnect() call success")
            include.gcominfo['dbconn'] = include.gdb
            include.gcominfo['dbconn'] = comdbutil.gdbmsSession

        if comdbutil.ibatisload() == False :
            return  False

    except Exception as err:
        print('▲tpbegin()-실패 ERR:', str(err))
        return False
    else:
        # print('▲tpbegin()-성공:')
        pass
    finally:
        return True

def tpcommit() :
    try :

        conn = comdbutil.gdbmsSession[0]
        conn.commit()
    except Exception as err:
        print('▲tpcommit()-ERR:', str(err))
        return False
    else:
        print('▲tpcommit()-성공:')
    finally:
        return True

def tprollback() :
    try :
        conn = comdbutil.gdbmsSession[0]
        conn.rollback()
    except Exception as err:
        print('▲tprollback()-ERR:', str(err))
        return False
    else:
        print('▲tprollback()-성공:')
    finally:
        return True


def tpenv() :
    filename = include.tcfenv_fname
    str=''
    f = open(filename)

    while True:
        line = f.readline()
        if line == '--endof' : break
        str = line.split("=")
        key = str[0]
        value = str[1].replace("\n","")
        include.gtcfenv[key] = value
        if not line: break

    f.close()

def tpenv2() :
    # filename = "C:\jDev\MyWorks\PycharmProjects\Roian\\bin\\tcf.env"
    filename = include.tcfenv_fname
    str=''
    with open(filename) as f:
        lines = f.readlines()
        lines = lines.replace('\n','')

    print(lines)

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
    print(doc)  # 파일내용 출력
    # print(json.dumps(response, indent=2))  # NLU 결과출력



