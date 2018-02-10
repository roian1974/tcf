import xlrd
import time
import sys

from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.info import include
from src.com.fwk.business.util.parser import comparser

srcList = []

#----------------------------------------------------------------------------------------------------------------------
#
#
#----------------------------------------------------------------------------------------------------------------------
def DED1002():
    rtn = 0
    try:
        comutil.fprint(__file__, "DED1002_start() start ")
        rtn = DED1002_start()
        comutil.fprint(__file__, "DED1002_start() end ")

        if rtn  == include.SUCCESS :
            rtn = DED1002_processing()

    except Exception as err:
        comutil.ferrprint(__file__, 'ded1001', str(err))
        include.setErr('EDE030', 'ded1001' + str(err))
    else:
        comutil.fsusprint(__file__, 'ded1001', '성공')
    finally:
        DED1002_end()
        return include.SUCCESS

def DED1002_start() :
    rtn = 0
    try:
        # 읽어야 될 파일정보를 저장한다.
        # test_group_1.xlsx
        if len( sys.argv ) != 3 :
            comutil.ferrprint(__file__, 'DED1002_start', '인자가 부족합니다.' + str(len(sys.argv)))
            include.setErr('EDE031', 'DED1002_start,인자가 부족합니다.' + str(len(sys.argv)))
            return -1

        fname = include.gcominfo['sysargv'][2]
        fname = "C:\jDev\MyWorks\PycharmProjects\Roian\log\input\%s" % (fname)
        srcList.append(fname)

    except Exception as err:
        comutil.ferrprint(__file__, 'DED1002_start', str(err))
        include.setErr('EDE031', 'DED1002_start,' + str(err))
    else:
        comutil.fsusprint(__file__, 'DED1002_start', '성공')
    finally:
        return include.SUCCESS

def DED1002_processing() :
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
        comutil.ferrprint(__file__, 'DED1002_processing', str(err))
        include.setErr('EDE032', 'DED1002_processing,' + str(err))
    else:
        comutil.fsusprint(__file__, 'DED1002_processing', '성공')
    finally:
        return include.SUCCESS

def DED1002_end() :
    rtn = 0
    try:
        pass
    except Exception as err:
        comutil.ferrprint(__file__, 'DED1002_end', str(err))
        include.setErr('EDE033', 'DED1002_end,' + str(err))
    else:
        comutil.fsusprint(__file__, 'DED1002_end', '성공')
    finally:
        return include.SUCCESS

#-----------------------------------------------------------------------------------------------------------------------

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())

def ST01_dataReaderFromExcel(src):
    wbDict = {'document':{}, 'sentence':{}}
    wb = xlrd.open_workbook(src)

    #wsList : 엑셀파일의 시트명
    wsList = wb.sheet_names()

    # 여기서 작업은 엑셀을 시트별로 열어서
    # 문서별로 문장단위로 해서 결과를 저장하는 역할을 하는 것이다.
    for i in range(len(wsList)):
        ws = wb.sheet_by_name(wsList[i])
        print('파일명-',src,'-',wsList[i],'-',ws.nrows)

        if wsList[i] == 'Entity':
            for j in range(ws.nrows):
                if j >= 4:
                    wsRow = ws.row_values(j)
                    targets = wsRow[4]
                    targets = targets.split('^')
                    if targets == ['']:
                        targets = []
                    wbDict['document'][wsRow[1]] = [wsRow[2], targets]
        else:
            pass

    print('=============================')
    print(wbDict)
    print('=============================')

    return wbDict

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
                nluResult = tpsutil.tpssendrecv('entity', text, target)
                # nluResult = tpsutil.interface_tpssendrecv('entity', text, target)
                if nluResult == include.FAIL :
                    comutil.ferrprint(__file__, 'ST02_getNLUResultFromWatson', 'tpssendrecv 에러가 발생')
                    include.setErr('EDE021', 'ST02_getNLUResultFromWatson()-' + 'tpssendrecv 에러가 발생')
                    return include.FAIL

                dic['docid'] = docid
                dic['response'] = nluResult
                cnt += 1
                jsonList.append(dic)
    return jsonList


def ST03_saveDocSentiment(pListJson) :

    t_logfile = "{0}\\{1}.tar.{2}.{3}".format("C:\\jDev\\MyWorks\\PycharmProjects\\Roian\log\\output\\entity",
                                        'Entity', comutil.getsysdate(), comutil.getsystime())

    fs = open(t_logfile, 'a', encoding='utf8')


    try :

        print('----len--',len(pListJson))
        cnt = 0
        for record in pListJson :
            cnt += 1
            print("=======================cnt=====================",cnt)
            docid = record['docid']
            response = record['response']

            # sudata_s : 기업에 대한 감성
            sudata_s, sudata_e, sudata_y = comparser.parser_entity(docid, response)

            print('sudata-s',str(sudata_s))

            for value in sudata_s:
                if 'docid' not in value : docid = "DOCXXX"
                else :
                    docid = value['docid']

                if 'type'  not in value : type = 'XXXX'
                else :
                    type = value['type']

                if 'text' not in value :  text = 'XXXX'
                else :
                    text = value['text']
                    text = text.encode('utf-8')
                    text = text.decode('utf-8')

                if 'score' not in value : score = 0.0
                else :
                    score = value['score']

                if 'label' not in value : label = 'XXXX'
                else :
                    label = value['label']

                if 'sadness' not in value :  sadness = 0.0
                else :
                    sadness = value['sadness']

                if 'joy' not in value : joy = 0.0
                else :
                    joy = value['joy']

                if 'fear' not in value : fear = 0.0
                else :
                    fear = value['fear']

                if 'disgust' not in value : disgust = 0.0
                else :
                    disgust = value['disgust']

                if 'anger' not in value : anger = 0.0
                else :
                    anger = value['anger']

                if 'subtype' not in value : subtype = 'XXXX'
                else :
                    subtype = value['subtype']

                if 'count' not in value : count = 0
                else :
                    count = value['count']

                data = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (docid, type, text, str(score),label,str(sadness),str(joy),str(fear),str(disgust),str(anger),subtype,str(count))
                fs.write(data+"\n")

    except Exception as err:
        comutil.ferrprint(__file__, 'ST03_saveDocSentiment', str(err))
        include.setErr('EDE009', '함수(ST03_saveDocSentiment) 에러:' + str(err))
    else:
        comutil.fsusprint(__file__, 'ST03_saveDocSentiment', '성공')
    finally:
        fs.close()



