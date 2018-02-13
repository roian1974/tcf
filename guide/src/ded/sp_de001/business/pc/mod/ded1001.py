import xlrd
import time
import sys

from src.com.fwk.business.util.parser import comparser
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include

srcList = []

#----------------------------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------------------------
def DED1001():
    rtn = 0
    try:
        comutil.fprint(__file__, "DED1001_start() start ")
        rtn = DED1001_start()
        comutil.fprint(__file__, "DED1001_start() end ")

        if rtn  == include.SUCCESS :
            rtn = DED1001_processing()

    except Exception as err:
        comutil.ferrprint(__file__, 'ded1001', str(err))
        include.setErr('EDED001', 'ded1001' + str(err))
    else:
        comutil.fsusprint(__file__, 'ded1001', '성공')
    finally:
        DED1001_end()
        return include.SUCCESS

def DED1001_start() :
    rtn = 0
    try:
        if len( sys.argv ) != 3 :
            comutil.ferrprint(__file__, 'DED1001_start', '인자가 부족합니다.' + str(len(sys.argv)))
            include.setErr('EDED001', 'DED1001_start,인자가 부족합니다.' + str(len(sys.argv)))
            return -1

        # 읽어야 될 파일정보를 저장한다.
        # test_group_1.xlsx
        fname = include.gcominfo['sysargv'][2]
        fname = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\%s" % (fname)
        srcList.append(fname)

    except Exception as err:
        comutil.ferrprint(__file__, 'DED1001_start', str(err))
        include.setErr('EDED001', 'DED1001_start,' + str(err))
    else:
        comutil.fsusprint(__file__, 'DED1001_start', '성공')
    finally:
        return include.SUCCESS

def DED1001_processing() :
    rtn = 0
    try:
        print("#################################################################", getIntTime())
        # 엑셀파일 하나당 작업을 시작합니다.
        for i in range(len(srcList)):
            # 엑셀파일로부터 시트별로 데이타를 가지고온다.(가지고올때 파일의 전체데이타를 가지고 온다.
            db = ST01_dataReaderFromExcel(srcList[i])

            print('---nulResult--before')
            # 왓슨을 호출하고 결과를 가지고 온다.
            ResultData = ST02_getNLUResultFromWatson(db)
            if ResultData ==  -1 :
                print("ST02_getNLUResultFromWatson call error")
                print("#################################################################", getIntTime())

                print('분석 작업이 완료되었습니다.', getTime())
                return -1

            print('---nulResult--after',ResultData)

            #호출된 결과를 파일로 저장합니다.
            ST03_saveDocSentiment(ResultData)
        print("#################################################################", getIntTime())
        print('분석 작업이 완료되었습니다.', getTime())
    except Exception as err:
        comutil.ferrprint(__file__, 'DED1001_processing', str(err))
        include.setErr('EDED001', 'DED1001_processing,' + str(err))
    else:
        comutil.fsusprint(__file__, 'DED1001_processing', '성공')
    finally:
        return include.SUCCESS

def DED1001_end() :
    rtn = 0
    try:
        pass
    except Exception as err:
        comutil.ferrprint(__file__, 'DED1001_end', str(err))
        include.setErr('EDED001', 'DED1001_end,' + str(err))
    else:
        comutil.fsusprint(__file__, 'DED1001_end', '성공')
    finally:
        return include.SUCCESS

#-----------------------------------------------------------------------------------------------------------------------

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())

# src : 엑셀파일명 - test_group_1.xlsx
# return value :
# wDict = {
#   'document': {
#        'DOC0004': ['기사원문 내용', [기업리스트]],
#        'DOC0012': ['기사원문 내용', [기업리스트]]
#    },
#    'sentence': {
#        'DOC0004': {
#            'SENT01': '문장내용.',
#            'SENT02': '문장내용.',
#            'SENT03': '문장내용.'},
#        'DOC0012': {
#            'SENT01': '문장내용.',
#            'SENT02': '문장내용.',
#            'SENT03': '문장내용.'},
#        }
#    }
# }
def ST01_dataReaderFromExcel(src):
    # Read
    wbDict = {'document':{}, 'sentence':{}}
    wb = xlrd.open_workbook(src)

    #wsList : 엑셀파일의 시트명
    wsList = wb.sheet_names()

    # 여기서 작업은 엑셀을 시트별로 열어서
    # 문서별로 문장단위로 해서 결과를 저장하는 역할을 하는 것이다.
    for i in range(len(wsList)):
        ws = wb.sheet_by_name(wsList[i])
        print('파일명-',src,'-',wsList[i],'-',ws.nrows)

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

    return wbDict

# INPUT VALUE :
# dataset = {
#   'document': {
#        'DOC0004': ['기사원문 내용', [기업리스트]],
#        'DOC0012': ['기사원문 내용', [기업리스트]]
#    },
#    'sentence': {
#        'DOC0004': {
#            'SENT01': '문장내용.',
#            'SENT02': '문장내용.',
#            'SENT03': '문장내용.'},
#        'DOC0012': {
#            'SENT01': '문장내용.',
#            'SENT02': '문장내용.',
#            'SENT03': '문장내용.'},
#        }
#    }
# }

def ST02_getNLUResultFromWatson(dataset) :
    sorted_db_dict = {'semantic_roles': {}, 'sentiment': {}, 'entities': {}, 'document': {}, 'sentence': {}}
    dbKeyList = list(dataset.keys())

    print('dbKeyList-', dbKeyList)

    # Looping을 돌려면 document.docid 별로 기사원문을 읽어서 왓슨에 호출한다.
    jsonList = []
    cnt = 0
    for j in range(len(dbKeyList)):
        # documenmt
        if dbKeyList[j] == 'document':
            # 문서ID
            docKeyList = list(dataset['document'].keys())
            for k in range(len(docKeyList)):

                docid = docKeyList[k]
                print('분석 작업이 진행 중 입니다.-',docKeyList[k])

                text = dataset['document'][docKeyList[k]][0]
                target = dataset['document'][docKeyList[k]][1]

                if docKeyList[k] in sorted_db_dict['document'].keys():
                    pass
                else:
                    sorted_db_dict['document'][docKeyList[k]] = text

                # text : 기사본문
                # target : 기업명
                print('nlu-calldata-docid-', docid)
                print('nlu-calldata-text-', text)
                print('nlu-calldata-target-', target)
                dic = dict()
                #nluResult = comparser.call_sentiment(text,target)
                nluResult = tpsutil.tpssendrecv('sentiment', text, target)
                # nluResult = tpsutil.interface_tpssendrecv('sentiment', text, target)
                if nluResult == include.FAIL :
                    comutil.ferrprint(__file__, 'ST02_getNLUResultFromWatson', 'tpssendrecv 에러가 발생')
                    include.setErr('EDED009', 'ST02_getNLUResultFromWatson()' + 'tpssendrecv 에러가 발생')
                    return include.FAIL

                dic['docid'] = docid
                dic['response'] = nluResult
                # print("==============================")
                # {
                # 'usage': {'text_units': 1, 'text_characters': 1188, 'features': 1},
                # 'sentiment': {'targets': [
                #                               {'text': 'samsung', 'score': 0.279964, 'label': 'positive'},
                #                               {'text': 'sk', 'score': 0.312345, 'label': 'positive'}
                #                           ],
                #               'document': {'score': 0.127034, 'label': 'positive'}},
                # 'retrieved_url': 'https://www.wsj.com/news/markets',
                # 'language': 'en'
                # }
                # nluResult['sentiment']['document']['label'] == positive
                # print("==============================")
                cnt += 1
                jsonList.append(dic)
    return jsonList


def ST03_saveDocSentiment(pListJson) :

    s_logfile = "{0}\\{1}.doc.{2}.{3}".format("C:\\jDev\\MyWorks\\PycharmProjects\\Roian\log\\output\\sentiment",
                                        'Sentiment', comutil.getsysdate(), comutil.getsystime())
    t_logfile = "{0}\\{1}.tar.{2}.{3}".format("C:\\jDev\\MyWorks\\PycharmProjects\\Roian\log\\output\\sentiment",
                                        'Sentiment', comutil.getsysdate(), comutil.getsystime())

    fs = open(s_logfile, 'a')
    ft = open(t_logfile, 'a')

    try :

        for record in pListJson :
            docid = record['docid']
            response = record['response']
            # sudata_s : 문서에 대한 감성
            # sudata_t : 기업에 대한 감성
            sudata_s,sudata_t = comparser.parser_sentiment(docid, response)
            print('sudata-s',str(sudata_s))
            for value in sudata_s:
                docid = value['docid']
                # text = value['text']
                score = value['score']
                label = value['label']
                fs.write(docid + '\t' + str(score) + '\t' + label + '\t' + '\n')

            print('sudata-t',str(sudata_t))
            for value in sudata_t:
                docid = value['docid']
                text = value['text']
                score = value['score']
                label = value['label']
                ft.write(docid + '\t' + text + '\t' + str(score) + '\t' + label + '\t' + '\n')

    except Exception as err:
        comutil.ferrprint(__file__, 'ST03_saveDocSentiment', str(err))
        include.setErr('EDED009', '함수(ST03_saveDocSentiment) 에러:' + str(err))
    else:
        comutil.fsusprint(__file__, 'ST03_saveDocSentiment', '성공')
    finally:
        fs.close()
        ft.close()



