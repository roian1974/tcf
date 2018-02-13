# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 파서 관리 모듈
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------

import json
from src.com.fwk.business.info import include
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1  import Features, SentimentOptions,  EntitiesOptions

SUCCESS = 0
FAIL = 0
__USERNAME__ = "f842a62b-e902-4cd4-a443-239e49976f59"
__PASSWORD__ = "nDGL7hG4zQaO"
__VERSION__ = '2017-02-27'
gsNLU = ''

# "username": "f842a62b-e902-4cd4-a443-239e49976f59",
# "password": "nDGL7hG4zQaO"
# __USERNAME__ = "1cf8e15d-6661-4ab2-9a35-696b35c684fb"
# __PASSWORD__ = "M4JXgbFSBeNO"


def login_watson() :
    rtn = SUCCESS
    try:
        gsNLU = NaturalLanguageUnderstandingV1( username=__USERNAME__,password=__PASSWORD__,version=__VERSION__ )
    except Exception as err:
        print('login_watson-ERR:', str(err))
        rtn = FAIL
    else:
        print('login_watson() 성공',gsNLU)
    finally:
        if rtn == FAIL:
            return FAIL
        else:
            return SUCCESS

def call_sentiment_tst() :
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username='1cf8e15d-6661-4ab2-9a35-696b35c684fb',
        password='M4JXgbFSBeNO',
        version='2017-02-27')

    response = natural_language_understanding.analyze(
        url='www.wsj.com/news/markets',
        features=Features(
            sentiment=SentimentOptions(
                targets=['stocks'])))

    print(json.dumps(response, indent=2))


# text = 기사본문
# targets = [ 'sk', '에스케이', '주SK' ]
#
def call_sentiment(text,targets) :
    rtn = SUCCESS
    response = ''
    try:
        if login_watson() == SUCCESS :
            print('IN-',text)
            print('TARGET-',targets)

            response = gsNLU.analyze(
                text=text,
                features=Features(sentiment=SentimentOptions(targets=targets)))

    except Exception as err:
        print('▲▲▲ ERR :', err)
        rtn = FAIL
    else:
        print('▲▲▲ call_sentiment():에러없음▲▲▲')

    finally:
        if rtn == FAIL :
            print('▲▲▲ call_sentiment call failed ▲▲▲')

            #------------------------------------------------------------------------------------------------
            # 20180110 강제테스트
            # ------------------------------------------------------------------------------------------------
            str_sentiment = '{ \
            "usage": { "text_units": 1, "text_characters": 1188,  "features": 1  },  \
            "sentiment": {   \
                "targets": [   \
                    { "text": "stocks", "score": 0.279964, "label": "positive" },{ "text": "sk", "score": 0.379964, "label": "positive" }   \
                            ],    \
                "document": {      "score": 0.127034,      "label": "positive"    }  \
                        },  \
            "retrieved_url": "https://www.wsj.com/news/markets",  \
            "language": "en"} '

            return str_sentiment

        else :
            return response


# text = 기사본문
def call_entities_old(text) :
    rtn = SUCCESS
    try:
        response = gsNLU. \
            analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(
                    sentiment=True,
                    emotion=True,
                    limit=250)))
    except Exception as err:
        print('ERR:', str(err))
        rtn = FAIL
    else:
        print('call_entities():에러없음')
    finally:
        return response

# str은 watson으로 수신한 response
def parser_entity(docid,str) :

    try :
        # json_d = json.loads(str)
        # if type(json_d) is dict :
        #     pass
        # else:
        #     return FAIL
        json_d = str

        sudata_s = []; sudata_e = []; sudata_y = []
        s_no = 0; e_no = 0

        for key1, value1 in json_d.items():
            if key1 == "usage" :
                pass
            elif key1 == "language" :
                pass
            elif key1 == "retrieved_url" :
                pass
            elif key1 == "entities" :
                for record in value1:
                    sentiment = dict();
                    emotion = dict();
                    subtype=dict();
                    sentiment['docid'] = emotion['docid'] = subtype['docid'] = docid

                    for key2, value2 in record.items() :
                        # print('###',key2,'|',value2)
                        if key2 == "type" :
                            sentiment[key2] = value2
                        elif key2 == "text" :
                            sentiment[key2] = value2
                            emotion[key2] = value2
                            subtype[key2] = value2
                        elif key2 == "sentiment" :
                            for key3,value3 in value2.items() :
                                if key3 == "score" :
                                    sentiment[key3] = value3
                                elif key3 == "label" :
                                    sentiment[key3] = value3
                                else :
                                    pass
                        elif key2 == "emotions" :
                            for key3,value3 in value2.items() :
                                emotion[key3] = value3
                                sentiment[key3] = value3
                        elif key2 == "disambiguation" :
                            for key3,value3 in value2.items() :
                                if key3 == "subtype" :
                                    subtype[key3] = value3
                                    sentiment[key3] = value3
                                elif key3 == "name" :
                                    subtype[key3] = value3
                                else :
                                    pass
                        elif key2 == "count" :
                            sentiment[key2] = value2
                        else :
                            pass
                    # print('---1',sentiment,emotion,subtype)
                    sudata_s.append(sentiment)
                    sudata_e.append(emotion)
                    sudata_y.append(subtype)
            else :
                pass
    except Exception as err:
        print("paser_entity-에러가 발생",str(err))
        include.setErr('EPR001', '함수(parser-entity) 에러내용:' + str(err))
    else:
        print("parser_entity()호출 성공")
    finally:
        # sudata_s - 전체
        # sudata_e - 감정
        # sudata_y - 서브타입
        return sudata_s, sudata_e, sudata_y

# str은 watson으로 수신한 response
def parser_sentiment(docid,str) :

    try :
        # json_d = json.loads(str)
        # if type(json_d) is dict :
        #     pass
        # else:
        #     return -1
        json_d = str

        sudata_s = [];
        sudata_t = [];
        s_no = 0;

        for key1, value1 in json_d.items():
            if key1 == "usage" :
                pass
            elif key1 == "language" :
                pass
            elif key1 == "retrieved_url" :
                pass
            elif key1 == "sentiment" :
                for key2, value2 in value1.items() :
                    if key2 == "targets" :
                        for record in value2:
                            sentiment = dict();
                            sentiment['docid'] = docid
                            for key3, value3 in record.items():
                                sentiment[key3] = value3
                                #print('sentiment[',key3,']=',sentiment[key3])
                            sudata_t.append(sentiment)
                    elif key2 == "document":
                        sentiment = dict();
                        sentiment['docid'] = docid
                        for key3,value3 in value2.items() :
                            if key3 == "score" :
                                sentiment[key3] = value3
                            elif key3 == "label":
                                sentiment[key3] = value3
                            else :
                                pass
                        # sentiment 키와 tarkey을 같이 할 경우는 넣고 아니면 빼
                        # if 'text' not in sentiment.keys() :
                        #     sentiment['text'] = 'ROOT'
                        sudata_s.append(sentiment)
                    else :
                        pass
            else :
                print("parser_sentiment()호출 성공")
                pass
    except Exception as err:
        print(str(err))
    else:
        pass
    finally:
        print('end')
        return sudata_s,sudata_t


def parser_keyword(str,docid) :
    rtn = 0
    try:
        json_d = json.loads(str)
        if type(json_d) is dict:
            pass
        else:
            return -1

        sudata_s = [];
        sudata_e = []
        s_no = 0;
        e_no = 0

        for key1, value1 in json_d.items():
            if key1 == "usage":
                pass
            elif key1 == "keywords":
                for record in value1:  # value1은 리스트
                    sentiment = dict();
                    emotion = dict();
                    subtype = dict();
                    sentiment['docid'] = emotion['docid'] = subtype['docid'] = docid
                    for key2, value2 in record.items():
                        if key2 == 'text':
                            sentiment[key2] = value2
                            emotion[key2] = value2
                        elif key2 == "sentiment":
                            for key3, value3 in value2.items():
                                if key3 == 'score':
                                    sentiment[key3] = value3
                            sudata_s.append(sentiment)
                        elif key2 == 'relevance':
                            pass
                        elif key2 == "emotions":
                            for key3, value3 in value2.items():
                                emotion[key3] = value3
                            sudata_e.append(emotion)
                        else:
                            pass
            elif key1 == "language":
                pass
            elif key1 == "retrieved_url":
                pass
            else:
                pass
    except Exception as err:
        print(str(err))
    else:
        pass
    finally:
        return sudata_s, sudata_e


str_entities = '{ "usage": { "text_units": 1, "text_characters": 1536, "features": 1 }, \
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
                    "score": 0.0,                     \
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

# str_sentiment = "{'usage': {'text_units': 1, 'text_characters': 720, 'features': 1}, 'sentiment': {'targets': [], 'document': {'score': -0.704499, 'label': 'negative'}}, 'language': 'ko'}"

# str_sentiment = '{ \
# "usage": { "text_units": 1, "text_characters": 1188,  "features": 1  },  \
# "sentiment": {   \
#     "targets": [   \
#         { "text": "stocks", "score": 0.279964, "label": "positive" },{ "text": "sk", "score": 0.379964, "label": "positive" }   \
#                 ],    \
#     "document": {      "score": 0.127034,      "label": "positive"    }  \
#             },  \
# "retrieved_url": "https://www.wsj.com/news/markets",  \
# "language": "en"} '

# login_watson()
#call_sentiment_tst()
#exit(0)

# targets = []
# str_sentiment = call_sentiment(text,targets)
# exit(0)

# sudata_s = parser_sentiment(str_sentiment,'00000001')
# print("------------------------------------------------------------")
# for value in sudata_s:
#     print(value)
#
# exit(0)
#

# sudata_s,sudata_e,sudata_y = parser_entity(str_entities,'00000001')
#
# print("------------------------------------------------------------")
# for value in sudata_s:
#     print(value)

# print("------------------------------------------------------------")
# for value in sudata_e:
#    print(value)
#
# print("------------------------------------------------------------")
# for value in sudata_y:
#    print(value)
# exit(0)

#
