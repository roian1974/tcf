import time
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg002.business.dc import dc_bg002

def BIG2000():
    rtn = True
    try:
        comlogging.logger.info( "BIG2000_start() start ")
        # ------------------------------------------------------------------------------------------------------------
        # 전처리된 입력파일에 대한 로딩작업을 진행한다.
        # ------------------------------------------------------------------------------------------------------------
        cdto = BIG2000_start()

        if include.isError() == False:
            comlogging.logger.info( "BIG2000_processing() start ")
            #--------------------------------------------------------------------------------------------------------
            # 훈련데이타 와 데이타 데이터를 준비하는 과정을 거친다.
            #   > 데이타를 소문자로 치환하는 작업을 처리한다.
            #   > 문장을 읽어서 단어별로 리스트를 작성하고 단어별 빈도수를 작업한다.
            # --------------------------------------------------------------------------------------------------------
            cdto = BIG2000_processing(cdto)

        else :
            raise Exception('BIG2000_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG2000-'+ str(err))
        include.setErr('EBIG2000', 'BIG2000' + str(err))
    else:
        comlogging.logger.info( 'BIG2000-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG2000_end(cdto)

        if include.isError() == False :
            return True
        else :
            return False

#----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
#----------------------------------------------------------------------------------------------------------------------
def BIG2000_start() :
    try:

        big2000cdto = include.gcominfo['sysargv'][3]

    except Exception as err:
        comlogging.logger.error( 'BIG2000_start-' + str(err))
        include.setErr('EBIG2000', 'BIG2000_start,' + str(err))
    else:
        comlogging.logger.info( 'BIG2000_start-성공')
    finally:
        if include.isError() == False :
            return big2000cdto
        else :
            return False

def BIG2000_processing(big2000cdto) :
    try:

        infile = big2000cdto.indata['filename']
        modelType = big2000cdto.indata['model']
        baseDate = big2000cdto.indata['basedate']
        ftype = big2000cdto.indata['ftype']
        d_type = big2000cdto.indata['d_type']

        comlogging.logger.info("#################################################################" + str(getIntTime()))

        comlogging.logger.info('• 1. 훈련데이타와 테스트 데이터를 준비한다.')
        big2000cdto = dc_bg002.preAnalysis(big2000cdto)
        if big2000cdto  != True :
            comlogging.logger.info('• 2. 모델 훈련과 모델을 생성한다.')
            train = big2000cdto.ddto['train']
            headlines = big2000cdto.ddto['headlines']
            if d_type == "train" :
                dc_bg002.trainModel(modelType, train, headlines)
            elif d_type == "test":
                out = dc_bg002.testModel(modelType, train, headlines)
                big2000cdto.outdata['out'] = out


        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG2000_processing '+ str(err) )
        include.setErr('EBIG2000', 'BIG2000_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG2000_processing-성공')
    finally:
        if include.isError() == False :
            return big2000cdto
        else :
            return False

def BIG2000_end(cdto) :
    try:
        #------------------------------------------------------------------------------------------------------------
        # 클라이언트로 전송할 내용을 저장한다.
        # ------------------------------------------------------------------------------------------------------------
        include.gcominfo['outdata'].append(cdto)

    except Exception as err:
        comlogging.logger.error( 'BIG2000_end '+ str(err))
        include.setErr('EBIG2000', 'BIG2000_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG2000_end-성공')
    finally:

        if include.isError() == False :
            return True
        else :
            return False

#-----------------------------------------------------------------------------------------------------------------------

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday,t3.tm_hour, t3.tm_min, t3.tm_sec)

def getIntTime():
    return time.mktime(time.localtime())
