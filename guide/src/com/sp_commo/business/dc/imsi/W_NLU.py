# -*- coding: utf-8 -*-
import operator
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SemanticRolesOptions, SentimentOptions, EntitiesOptions
import json
import  xlrd
import  xlwt
import time
from pandas import Series, DataFrame


model_id=''

def printRecord(j_response):
    sentiment_targets_text1 = j_response['sentiment']['targets'][0]['text'] # samsung
    sentiment_targets_score1 = j_response['sentiment']['targets'][0]['score']  # 0.27
    sentiment_targets_label1 = j_response['sentiment']['targets'][0]['label']  # positive

    sentiment_targets_text2 = j_response['sentiment']['targets'][1]['text'] # sk
    sentiment_targets_score2 = j_response['sentiment']['targets'][1]['score']  # 0.3
    sentiment_targets_label2 = j_response['sentiment']['targets'][1]['label']  # positive

    sentiment_document_score = j_response['sentiment']['document']['score']
    sentiment_document_label = j_response['sentiment']['document']['label']

    print("===========================================================================================")
    print("%-10.10s %-10.10s %-10.10s %-10.10s %-8.8s %-8.8s %-8.8s" % ("문서ID", "기사스코어", "레이블", "모델ID", "사용여부", "등록일자", "수정일자"))
    print("===========================================================================================")
    print("%-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s" % ("00001", sentiment_document_score, sentiment_document_label, "2017-12-31", "N", "20180105","20180105" ))

    print("===========================================================================================")
    print("%-10.10s %-10.10s %-10.10s %-10.10s %-8.8s %-8.8s %-8.8s" % ("문서ID", "기업명", "기사스코어", "레이블", "사용여부", "등록일자", "수정일자"))
    print("===========================================================================================")

    for dicitem in j_response['sentiment']['targets']:
        print("%-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s %-10.10s" % ("00001", dicitem['text'], dicitem['score'], dicitem['label'], "Y", "20180105","20180105" ))


def imsiResponse():
    j_response = {
        "usage": {
            "text_units": 1, "text_characters": 1188, "features": 1
        },
        "sentiment": {
            "targets": [  { "text": "samsung", "score": 0.279964, "label": "positive" } ,
                           { "text": "sk",       "score": 0.312345,  "label": "positive" }   ],
            "document": { "score": 0.127034, "label": "positive"  }
        },
        "retrieved_url": "https://www.wsj.com/news/markets",
        "language": "en"
    }

    jsentiment  = j_response['sentiment']
    jtargets    = j_response['sentiment']['targets']

    printRecord(j_response)

    return j_response


def nluProcessDoc(text, target):

    #nlu = NaturalLanguageUnderstandingV1(
    #  username="ed7537ca-4c0e-44fd-bdb3-405f6678bfa5",
    #  password="XqD3kHaBN7yS",
    #  version="2017-02-27")

    print('############################### login be')
    nlu = NaturalLanguageUnderstandingV1(
        username="f842a62b-e902-4cd4-a443-239e49976f59",
        password="nDGL7hG4zQaO",
        version="2017-02-27")

    model_id = "2017-02-27"
    print('############################### login af-',nlu)

    #-------------------------------------------
    # 2018.1.05 임시막음
    print('IN-',text)
    print('TARGET-',target)
    response = nlu.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions(targets=target)),
    )
    #response = imsiResponse()
    #-----------------------------------------------

    result = json.dumps(response, indent=2)
    return json.loads(result)



def nluProcessSent(text):

    #--------------------------------------------------------
    # 강선임
    #--------------------------------------------------------

    # --------------------------------------------------------
    __USERNAME__ = "f842a62b-e902-4cd4-a443-239e49976f59"
    __PASSWORD__ = "nDGL7hG4zQaO"
    __VERSION__ = '2017-02-27'

    watsonSession = NaturalLanguageUnderstandingV1(
        username=__USERNAME__,
        password=__PASSWORD__,
        version=__VERSION__)
    {
        "url": "https://gateway.watsonplatform.net/natural-language-understanding/api",
        "username": __USERNAME__,
        "password": __PASSWORD__
    }

    # nlu = NaturalLanguageUnderstandingV1(
    #   username="ed7537ca-4c0e-44fd-bdb3-405f6678bfa5",
    #   password="XqD3kHaBN7yS",
    #   version="2017-02-27")

    # response = natural_language_understanding.analyze(
    #     text = doc,
    #     features=[
    #         Features.Sentiment(
    #               targets=["주식시장","증권사"]
    #                 )
    #              ]
    #        )

    # response = watsonSession.analyze(
    #     text=text,
    #     features=Features(semantic_roles=SemanticRolesOptions(), entities=EntitiesOptions())
    # )

    response = watsonSession.analyze(
        text=text,
        features=Features(entities=EntitiesOptions())
    )

    result = json.dumps(response, indent=2)
    print("=========RCVDATA=",result)
    return json.loads(result)

# src == 엑셀파일
def dataReader(src):
    # Read
    wbDict = {'document':{}, 'sentence':{}}
    wb = xlrd.open_workbook(src)

    #wsList : 엑셀파일의 시트명
    wsList = wb.sheet_names()

    print("#####>>>>   wsList",wsList)
    print("#####>>>>   wsList", len(wsList))

    # 여기서 작업은 엑셀을 시트별로 열어서
    # 문서별로 문장단위로 해서 결과를 저장하는 역할을 하는 것이다.
    for i in range(len(wsList)):
        ws = wb.sheet_by_name(wsList[i])
        print('시트명-1-',src,'-',wsList[i],'-',ws.nrows)

        if wsList[i] == 'Semantic Roles' or wsList[i] == 'Entity':
            # 시트의 줄수가 얼마인지 체킹한다.
            # 실제데이타는 4부터 시작한다.
            for j in range(ws.nrows):
                if j >= 3:
                    wsRow = ws.row_values(j)
                    if wsRow[1] in wbDict['sentence'].keys():
                        pass
                    else:
                        wbDict['sentence'][wsRow[1]] = {}
                    if wsRow[2] in wbDict['sentence'][wsRow[1]].keys():
                        pass
                    else:
                        wbDict['sentence'][wsRow[1]][wsRow[2]] = wsRow[3]

        elif wsList[i] == 'Sentiment':
            for j in range(ws.nrows):
                if j >= 4:

                    wsRow = ws.row_values(j)
                    targets = wsRow[4]
                    targets = targets.split('^')
                    if targets == ['']:
                        targets = []

                    # print('wsRow[1]=',wsRow[1],'targets=',targets)
                    # print('wsRow[0]=', wsRow[0], 'wsRow[2]=', wsRow[2],)
                    # wsRow[1] : 문서ID 컬럼
                    # wsRow[2] : 문서 컬럼
                    # wsRow[3] : 문서(긍정/중립/부정) 컬럼
                    # wsRow[4] : 타켓-기업명 컬럼 = target
                    # wsRow[5] : 타켓-긍정/중립/부정

                    wbDict['document'][wsRow[1]] = [wsRow[2], targets]
                    #wDict = {'document': { 'DOC0004-문서ID-wsRow[1]': ['[기사내용-문서컬럼 wsRow[2]]', ['기업명-wsRow[4]targets']]}, 'sentence': {} }
                    #wDict['document']['DOC0004']==>['[aaaaaaaaaaaaaaa aaaaaaaaaa]', ['삼성','LG']]
                    #print ('wDict',wbDict)
        else:
            pass


    print('=============================')
    print(wbDict)
    print('=============================')

    #Entity - wDict = {
    #   'document': {
    #        'DOC0004': ['aaa. bbb. ccc.', []],
    #        'DOC0012': ['ddd. eee. fff.', []]
    #    },
    #    'sentence': {
    #        'DOC0004': {
    #            'SENT01': 'aaa.',
    #            'SENT02': 'bbb.',
    #            'SENT03': 'ccc.'},
    #        'DOC0012': {
    #            'SENT01': 'ddd.',
    #            'SENT02': 'eee.',
    #            'SENT03': 'ffff.'
    #        }
    #    }
    #}

    return wbDict



def translate(text):
    if text == 'neutral':
        return '중립'
    elif text == 'positive':
        return '긍정'
    elif text == 'negative':
        return '부정'

def nluResult(dataset):
    sorted_db_dict = {'semantic_roles' : {}, 'sentiment' : {}, 'entities' : {}, 'document' : {}, 'sentence' : {}}
    dbKeyList = list(dataset.keys())

    print ('dbKeyList-',dbKeyList)

    for j in range(len(dbKeyList)):
        # documenmt
        if dbKeyList[j] == 'document':
            # 문서ID
            docKeyList = list(dataset['document'].keys())
            for k in range(len(docKeyList)):
                print('분석 작업이 진행 중 입니다.')
                text = dataset['document'][docKeyList[k]][0]
                target = dataset['document'][docKeyList[k]][1]

                if docKeyList[k] in sorted_db_dict['document'].keys():
                    pass
                else:
                    sorted_db_dict['document'][docKeyList[k]] = text


                # text : 기사본문
                # target : 기업명
                # print(target)

                print('nlu-calldata-text-',text)
                print('nlu-calldata-target-', target)

                nluResult = nluProcessDoc(text, target)

                # print("==============================")
                # print(nluResult)
                # {
                #'usage': {'text_units': 1, 'text_characters': 1188, 'features': 1},
                #'sentiment': {'targets': [
                #                               {'text': 'samsung', 'score': 0.279964, 'label': 'positive'},
                #                               {'text': 'sk', 'score': 0.312345, 'label': 'positive'}
                #                           ],
                #               'document': {'score': 0.127034, 'label': 'positive'}},
                #'retrieved_url': 'https://www.wsj.com/news/markets',
                #'language': 'en'
                # }
                # nluResult['sentiment']['document']['label'] == positive
                # print("==============================")


                docSent = translate(nluResult['sentiment']['document']['label'])
                targets = nluResult['sentiment']['targets']
                target_list = []
                if len(targets) > 0:
                    for n in range(len(targets)):
                        targetTuple = (targets[n]['text'], translate(targets[n]['label']))
                        target_list.append(targetTuple)
                sorted_db_dict['sentiment'][docKeyList[k]] = [docSent, target_list]

        elif dbKeyList[j] == 'sentence':
            docKeyList = list(dataset['sentence'].keys())
            for h in range(len(docKeyList)):
                if docKeyList[h] in sorted_db_dict['sentence'].keys():
                    pass
                else:
                    sorted_db_dict['sentence'][docKeyList[h]] = {}
                sorted_db_dict['semantic_roles'][docKeyList[h]] = {}
                sorted_db_dict['entities'][docKeyList[h]] = {}
                sentKeyList = list(dataset['sentence'][docKeyList[h]].keys())
                for g in range(len(sentKeyList)):
                    print('분석 작업이 진행 중 입니다.')
                    sorted_db_dict['semantic_roles'][docKeyList[h]][sentKeyList[g]] = []
                    sorted_db_dict['entities'][docKeyList[h]][sentKeyList[g]] = {'Company':[], 'Person':[], 'Location':[], 'Organization':[]}
                    text = dataset['sentence'][docKeyList[h]][sentKeyList[g]]
                    if sentKeyList[g] in sorted_db_dict['sentence'][docKeyList[h]].keys():
                        pass
                    else:
                        sorted_db_dict['sentence'][docKeyList[h]][sentKeyList[g]] = text
                    nluResult = nluProcessSent(text)
                    # Semantic Roles
                    try:
                        if len(nluResult['semantic_roles']) > 0:
                            for t in range(len(nluResult['semantic_roles'])):
                                if 'subject' in nluResult['semantic_roles'][t].keys():
                                    subject = nluResult['semantic_roles'][t]['subject']['text']
                                else:
                                    subject = ''
                                if 'action' in nluResult['semantic_roles'][t].keys():
                                    action = nluResult['semantic_roles'][t]['action']['text']
                                else:
                                    action = ''
                                if 'object' in nluResult['semantic_roles'][t].keys():
                                    object = nluResult['semantic_roles'][t]['object']['text']
                                else:
                                    object = ''
                                svoResult = [subject, action, object]
                                sorted_db_dict['semantic_roles'][docKeyList[h]][sentKeyList[g]].append(svoResult)
                    except:
                        pass
                    # Entities
                    try:
                        if len(nluResult['entities']) > 0:
                            for t in range(len(nluResult['entities'])):
                                if nluResult['entities'][t]['type'] == 'Company':
                                    sorted_db_dict['entities'][docKeyList[h]][sentKeyList[g]]['Company'].append(nluResult['entities'][t]['text'])
                                elif nluResult['entities'][t]['type'] == 'Person':
                                    sorted_db_dict['entities'][docKeyList[h]][sentKeyList[g]]['Person'].append(nluResult['entities'][t]['text'])
                                elif nluResult['entities'][t]['type'] == 'Person':
                                    sorted_db_dict['entities'][docKeyList[h]][sentKeyList[g]]['Location'].append(nluResult['entities'][t]['text'])
                                elif nluResult['entities'][t]['type'] == 'Organization':
                                    sorted_db_dict['entities'][docKeyList[h]][sentKeyList[g]]['Organization'].append(nluResult['entities'][t]['text'])
                                else:
                                    pass
                    except:
                        pass

    # print("===========================stored_db_dict")
    # print(sorted_db_dict)
    example_sorted_db_dict = {
        'semantic_roles': {},
        'sentiment': {'DOC0004': ['긍정', [('samsung', '긍정'), ('sk', '긍정')]],
                      'DOC0012': ['긍정', [('samsung', '긍정'), ('sk', '긍정')]],
                      'DOC0019': ['긍정', [('samsung', '긍정'), ('sk', '긍정')]]},
        'entities': {},
        'document': {'DOC0004': 'aaaa',
                     'DOC0012': 'bbbb',
                     'DOC0019': 'cccc'},
        'sentence': {}
    }
    # print("===========================stored_db_dict")

    return sorted_db_dict

def dataWriter(src, dataset):
    semantic_role = {'document_id': [], 'sentence_id': [], 'sentence': [], 'subject': [], 'action': [], 'object': []}
    document_list = list(dataset['semantic_roles'].keys())
    for i in range(len(document_list)):
        document_id = document_list[i]
        sentence_list = list(dataset['semantic_roles'][document_id].keys())
        for j in range(len(sentence_list)):
            sentence_id = sentence_list[j]
            semantic_role_list = dataset['semantic_roles'][document_id][sentence_id]
            if len(semantic_role_list) == 0:
                semantic_role['document_id'].append(document_id)
                semantic_role['sentence_id'].append(sentence_id)
                semantic_role['sentence'].append(dataset['sentence'][document_id][sentence_id])
                semantic_role['subject'].append('')
                semantic_role['action'].append('')
                semantic_role['object'].append('')
            else:
                for k in range(len(semantic_role_list)):
                    semantic_role['document_id'].append(document_id)
                    semantic_role['sentence_id'].append(sentence_id)
                    semantic_role['sentence'].append(dataset['sentence'][document_id][sentence_id])
                    semantic_role['subject'].append(semantic_role_list[k][0])
                    semantic_role['action'].append(semantic_role_list[k][1])
                    semantic_role['object'].append(semantic_role_list[k][2])
    df_semantic_roles = DataFrame(semantic_role)
    df_semantic_roles = df_semantic_roles.sort_values(by=['document_id'], axis=0)

    sentiment = {'document_id': [], 'document': [], 'doc_sent': [], 'target': [], 'target_sent': []}
    document_list = list(dataset['sentiment'].keys())
    for i in range(len(document_list)):
        document_id = document_list[i]
        doc_sent = dataset['sentiment'][document_id][0]
        targets = dataset['sentiment'][document_id][1]
        if len(targets) > 0:
            for j in range(len(targets)):
                sentiment['document_id'].append(document_id)
                sentiment['document'].append(dataset['document'][document_id])
                sentiment['doc_sent'].append(doc_sent)
                sentiment['target'].append(targets[j][0])
                sentiment['target_sent'].append(targets[j][1])
        else:
            sentiment['document_id'].append(document_id)
            sentiment['document'].append(dataset['document'][document_id])
            sentiment['doc_sent'].append(doc_sent)
            sentiment['target'].append('')
            sentiment['target_sent'].append('')

    df_sentiment = DataFrame(sentiment)
    df_sentiment = df_sentiment.sort_values(by=['document_id'], axis=0)

    entities = {'document_id': [], 'sentence_id': [], 'sentence': [], 'company': [], 'person': [], 'location': [],
                'organization': []}
    document_list = list(dataset['entities'].keys())
    for i in range(len(document_list)):
        document_id = document_list[i]
        sentence_list = list(dataset['entities'][document_id].keys())
        for j in range(len(sentence_list)):
            sentence_id = sentence_list[j]
            entities_list = dataset['entities'][document_id][sentence_id]
            company_list = entities_list['Company']
            person_list = entities_list['Person']
            location_list = entities_list['Location']
            organization_list = entities_list['Organization']
            count = [len(company_list), len(person_list), len(location_list), len(organization_list)]
            max_count = max(count)
            sorted_entities_list = []
            if max_count > 0:
                for k in range(max_count):
                    try:
                        company = company_list[k]
                    except:
                        company = ''
                    try:
                        person = person_list[k]
                    except:
                        person = ''
                    try:
                        location = location_list[k]
                    except:
                        location = ''
                    try:
                        organization = organization_list[k]
                    except:
                        organization = ''
                    sorted_entities = [company, person, location, organization]
                    sorted_entities_list.append(sorted_entities)
            else:
                sorted_entities_list.append(['', '', '', ''])
            for n in range(len(sorted_entities_list)):
                entities['document_id'].append(document_id)
                entities['sentence_id'].append(sentence_id)
                entities['sentence'].append(dataset['sentence'][document_id][sentence_id])
                entities['company'].append(sorted_entities_list[n][0])
                entities['person'].append(sorted_entities_list[n][1])
                entities['location'].append(sorted_entities_list[n][2])
                entities['organization'].append(sorted_entities_list[n][3])
    df_entities = DataFrame(entities)
    df_entities = df_entities.sort_values(by=['document_id'], axis=0)

    order = ['Semantic Roles', 'Sentiment', 'Entities']
    # Write
    wb = xlwt.Workbook(encoding='euc-kr')
    for i in range(len(order)):
        ws = wb.add_sheet(order[i])
        ws.col(0).width = 851
        if order[i] == 'Semantic Roles':
            ws.col(1).width = 2592
            ws.col(2).width = 5555
            ws.col(3).width = 22037
            ws.col(4).width = 5555
            ws.col(5).width = 5555
            ws.col(6).width = 5555
            ws.col(7).width = 851
            ws.write_merge(1, 2, 1, 1, '문서ID')
            ws.write_merge(1, 2, 2, 2, '문장ID')
            ws.write_merge(1, 2, 3, 3, '문장')
            ws.write_merge(1, 1, 4, 6, 'Semantic Roles')
            ws.write(2, 4, '주체')
            ws.write(2, 5, '행위')
            ws.write(2, 6, '대상')
            for j in range(len(df_semantic_roles.index)):
                row = j + 3
                ws.write(row, 1, df_semantic_roles['document_id'].ix[j])
                ws.write(row, 2, df_semantic_roles['sentence_id'].ix[j])
                ws.write(row, 3, df_semantic_roles['sentence'].ix[j])
                ws.write(row, 4, df_semantic_roles['subject'].ix[j])
                ws.write(row, 5, df_semantic_roles['action'].ix[j])
                ws.write(row, 6, df_semantic_roles['object'].ix[j])
        elif order[i] == 'Sentiment':
            ws.col(1).width = 2592
            ws.col(2).width = 21925
            ws.col(3).width = 7407
            ws.col(4).width = 7407
            ws.col(5).width = 7407
            ws.col(6).width = 851
            ws.write_merge(1, 3, 1, 1, '문서ID')
            ws.write_merge(1, 3, 2, 2, '문서')
            ws.write_merge(1, 1, 3, 5, 'Sentiment')
            ws.write_merge(2, 3, 3, 3, '문서\n(긍정/중립/부정)')
            ws.write_merge(2, 2, 4, 5, '타겟')
            ws.write(3, 4, '기업명')
            ws.write(3, 5, '긍정/중립/부정')
            for j in range(len(df_sentiment.index)):
                row = j + 4
                ws.write(row, 1, df_sentiment['document_id'].ix[j])
                ws.write(row, 2, df_sentiment['document'].ix[j])
                ws.write(row, 3, df_sentiment['doc_sent'].ix[j])
                ws.write(row, 4, df_sentiment['target'].ix[j])
                ws.write(row, 5, df_sentiment['target_sent'].ix[j])
        elif order[i] == 'Entities':
            ws.col(1).width = 2592
            ws.col(2).width = 5555
            ws.col(3).width = 16481
            ws.col(4).width = 5555
            ws.col(5).width = 5555
            ws.col(6).width = 5555
            ws.col(7).width = 5555
            ws.col(8).width = 851
            ws.write_merge(1, 2, 1, 1, '문서ID')
            ws.write_merge(1, 2, 2, 2, '문장ID')
            ws.write_merge(1, 2, 3, 3, '문장')
            ws.write_merge(1, 1, 4, 7, 'Entities')
            ws.write(2, 4, 'Company')
            ws.write(2, 5, 'Person')
            ws.write(2, 6, 'Location')
            ws.write(2, 7, 'Organization')
            for j in range(len(df_entities.index)):
                row = j + 3
                ws.write(row, 1, df_entities['document_id'].ix[j])
                ws.write(row, 2, df_entities['sentence_id'].ix[j])
                ws.write(row, 3, df_entities['sentence'].ix[j])
                ws.write(row, 4, df_entities['company'].ix[j])
                ws.write(row, 5, df_entities['person'].ix[j])
                ws.write(row, 6, df_entities['location'].ix[j])
                ws.write(row, 7, df_entities['organization'].ix[j])

    src_title = src.split('.x')
    new_src = '%s_after_nlu_test.xls' % (src_title[0])
    wb.save(new_src)

#---------------------------

def getTime():
    t3 = time.localtime()
    #print('{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec))
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())

#---------------------------

def handler(srcList):
    print('분석 작업을 시작합니다.',getTime())
    print("#################################################################",getIntTime())

    # 엑셀파일 하나당 작업을 시작합니다.
    print('srcList=',srcList)
    for i in range(len(srcList)):

        db = dataReader(srcList[i])

        # Entity - wDict = {'document': {
        #    'DOC0004': ['aaa. bbb. ccc.', []],
        #    'DOC0012': ['ddd. eee. fff.', []]},
        #    'sentence': {
        #        'DOC0004': {
        #            'SENT01': 'aaa.',
        #            'SENT02': 'bbb.',
        #            'SENT03': 'ccc.'},
        #        'DOC0012': {
        #            'SENT01': 'ddd.',
        #            'SENT02': 'eee.',
        #            'SENT03': 'ffff.'
        #        }
        #    }
        # }

        print('---nulResult--before')
        ResultData = nluResult(db)
        print('---nulResult--after')


        print('--------------------------------ResultData--------------------------------')
        print(ResultData)
        print("---srcList[",i,"]--",srcList[i])

        example_ResultData = {
            'semantic_roles': {},
            'sentiment': {'DOC0004': ['긍정', [('samsung', '긍정'), ('sk', '긍정')]],
                          'DOC0012': ['긍정', [('samsung', '긍정'), ('sk', '긍정')]],
                          'DOC0019': ['긍정', [('samsung', '긍정'), ('sk', '긍정')]]},
            'entities': {},
            'document': {'DOC0004': 'aaaa',
                         'DOC0012': 'bbbb',
                         'DOC0019': 'cccc'},
            'sentence': {}
        }

        dataWriter(srcList[i], ResultData)
    print("#################################################################",getIntTime())
    print('분석 작업이 완료되었습니다.',getTime())


#srcList = ['test_group_1.xlsx', 'test_group_2.xlsx']
srcList = []
if __name__ == "__main__":
    import sys, getopt
    print(sys.argv)
    srcList.append(sys.argv[1])
    handler(srcList)

