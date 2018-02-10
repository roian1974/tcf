import time
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg003.business.dc import dc_bg003


def BIG3003():
    rtn = True
    try:
        comlogging.logger.info("BIG3003_start() start ")
        data = BIG3003_start()

        if include.isError() == False:
            comlogging.logger.info("BIG3003_processing() start ")

            tdata = BIG3003_processing(data)

        else:
            raise Exception('BIG3003_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error('BIG3003-' + str(err))
        include.setErr('EBIG3003', 'BIG3003' + str(err))
    else:
        comlogging.logger.info('BIG3003-성공')
    finally:

        BIG3003_end(tdata)

        if include.isError() == False:
            return True
        else:
            return False

def BIG3003_start():
    try:

        dc_bg003.훈련모형()

    except Exception as err:
        comlogging.logger.error('BIG3003_start-' + str(err))
        include.setErr('EBIG3003', 'BIG3003_start,' + str(err))
    else:
        comlogging.logger.info('BIG3003_start-성공')
    finally:
        if include.isError() == False:
            return data
        else:
            return False


def BIG3003_processing(data):
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        dc_bg003.훈련모형()

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error('BIG3003_processing ' + str(err))
        include.setErr('EBIG3003', 'BIG3003_processing,' + str(err))
    else:
        comlogging.logger.info('BIG3003_processing-성공')
    finally:
        if include.isError() == False:
            return True
        else:
            return False


def BIG3003_end(tdata):
    try:
        # ------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        outfile = include.gcominfo['sysargv'][4]
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"


    except Exception as err:
        comlogging.logger.error('BIG3003_end ' + str(err))
        include.setErr('EBIG3003', 'BIG3003_end,' + str(err))
    else:
        comlogging.logger.info('BIG3003_end-성공')
    finally:

        if include.isError() == False:
            return True
        else:
            return False


# -----------------------------------------------------------------------------------------------------------------------

def getTime():
    t3 = time.localtime()
    return '{}년{}월{}일-{}시{}분{}초'.format(t3.tm_year, t3.tm_mon, t3.tm_mday, t3.tm_hour, t3.tm_min, t3.tm_sec)


def getIntTime():
    return time.mktime(time.localtime())
