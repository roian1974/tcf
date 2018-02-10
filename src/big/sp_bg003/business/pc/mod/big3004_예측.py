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


def BIG3004():
    rtn = True
    try:
        comlogging.logger.info("BIG3004_start() start ")
        data = BIG3004_start()

        if include.isError() == False:

            comlogging.logger.info("BIG3004_processing() start ")

            tdata = BIG3004_processing(data)

        else:
            raise Exception('BIG3004_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error('BIG3004-' + str(err))
        include.setErr('EBIG3004', 'BIG3004' + str(err))
    else:
        comlogging.logger.info('BIG3004-성공')
    finally:

        BIG3004_end(tdata)

        if include.isError() == False:
            return True
        else:
            return False


# ----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
# ----------------------------------------------------------------------------------------------------------------------
def BIG3004_start():
    try:
        pass
    except Exception as err:
        comlogging.logger.error('BIG3004_start-' + str(err))
        include.setErr('EBIG3004', 'BIG3004_start,' + str(err))
    else:
        comlogging.logger.info('BIG3004_start-성공')
    finally:
        if include.isError() == False:
            return True
        else:
            return False


def BIG3004_processing(data):
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        dc_bg003.예측()

        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error('BIG3004_processing ' + str(err))
        include.setErr('EBIG3004', 'BIG3004_processing,' + str(err))
    else:
        comlogging.logger.info('BIG3004_processing-성공')
    finally:
        if include.isError() == False:
            return True
        else:
            return False


def BIG3004_end(tdata):
    try:
        outfile = include.gcominfo['sysargv'][4]
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"


    except Exception as err:
        comlogging.logger.error('BIG3004_end ' + str(err))
        include.setErr('EBIG3004', 'BIG3004_end,' + str(err))
    else:
        comlogging.logger.info('BIG3004_end-성공')
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
