import time
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg002.business.dc import dc_bg002

# python tcf_sp_commo.py sp_bg002 BIG2002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv             --3
#                                         C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\mod.logistic.20180131     --4
#                                         LogisR[NaiveEyes,RF,SVMGusian,SVMLinear]                                       --5

def BIG2002():
    rtn = True
    try:
        comlogging.logger.info( "BIG2002_start() start ")

        infile, modelfname, modelType = BIG2002_start()

        if include.isError() == False:

            comlogging.logger.info( "BIG2002_processing() start ")

            tdata = BIG2002_processing(infile, modelfname, modelType)

        else :
            raise Exception('BIG2002_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG2002-'+ str(err))
        include.setErr('EBIG2002', 'BIG2002' + str(err))
    else:
        comlogging.logger.info( 'BIG2002-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG2002_end(tdata)

        if include.isError() == False :
            return True
        else :
            return False

#----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
#----------------------------------------------------------------------------------------------------------------------
def BIG2002_start() :
    try:
        comlogging.logger.info("STEP-01: 전처리된 데이타를 입력한다")
        comlogging.logger.info("   >> IN: C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv")
        infile = include.gcominfo['sysargv'][3]
        modelType = include.gcominfo['sysargv'][4]
        baseDate = include.gcominfo['sysargv'][5]
    except Exception as err:
        comlogging.logger.error('BIG2001_start-' + str(err))
        include.setErr('EBIG2001', 'BIG2001_start,' + str(err))
    else:
        comlogging.logger.info('BIG2001_start-성공')
    finally:
        if include.isError() == False:
            return infile, modelType, baseDate
        else:
            return False


def BIG2002_processing(infile,modelType,baseDate) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))

        train, headlines = dc_bg002.preAnalysis(infile, baseDate, ">")  # > 201401231
        if headlines  != True :
            comlogging.logger.info('• 2. 모델 훈련과 모델을 생성한다.')
            out = dc_bg002.testModel(modelType, train, headlines)


        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG2002_processing '+ str(err) )
        include.setErr('EBIG2002', 'BIG2002_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG2002_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG2002_end(tdata) :
    try:
        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        outfile = include.gcominfo['sysargv'][4]
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"
        comutil.file_append( outfile, str(tdata) )


    except Exception as err:
        comlogging.logger.error( 'BIG2002_end '+ str(err))
        include.setErr('EBIG2002', 'BIG2002_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG2002_end-성공')
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
