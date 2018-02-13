import time
from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.common import comutil
from src.big.sp_bg004.business.dc import dc_bg004

# python tcf_sp_commo.py sp_bg002 BIG4002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv             --3
#                                         C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\mod.logistic.20180131     --4
#                                         LogisR[NaiveEyes,RF,SVMGusian,SVMLinear]                                       --5

def BIG4002():
    rtn = True
    try:
        comlogging.logger.info( "BIG4002_start() start ")

        infile, modelfname, modelType, ftype = BIG4002_start()


        if include.isError() == False:

            comlogging.logger.info( "BIG4002_processing() start ")

            tdata = BIG4002_processing(infile, modelfname, modelType, ftype)

        else :
            raise Exception('BIG4002_start 함수에서 에러가 발생')

    except Exception as err:
        comlogging.logger.error( 'BIG4002-'+ str(err))
        include.setErr('EBIG4002', 'BIG4002' + str(err))
    else:
        comlogging.logger.info( 'BIG4002-성공')
    finally:

        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        BIG4002_end(tdata)

        if include.isError() == False :
            return True
        else :
            return False

#----------------------------------------------------------------------------------------------------------------------
# 전처리된 입력파일에 대한 로딩작업을 진행한다.
#----------------------------------------------------------------------------------------------------------------------
def BIG4002_start() :
    try:
        comlogging.logger.info("STEP-01: 전처리된 데이타를 입력한다")
        infile = include.gcominfo['sysargv'][3]
        modelType = include.gcominfo['sysargv'][4]
        baseDate = include.gcominfo['sysargv'][5]

        if len( include.gcominfo['sysargv'] ) == 7 :
            ftype = include.gcominfo['sysargv'][6]
        else :
            ftype = 'EN'

    except Exception as err:
        comlogging.logger.error('BIG4001_start-' + str(err))
        include.setErr('EBIG4001', 'BIG4001_start,' + str(err))
    else:
        comlogging.logger.info('BIG4001_start-성공')
    finally:
        if include.isError() == False:
            return infile, modelType, baseDate, ftype
        else:
            return False


def BIG4002_processing(infile,modelType,baseDate, ftype) :
    try:
        comlogging.logger.info("#################################################################" + str(getIntTime()))


        train, headlines = dc_bg004.preAnalysis(infile, baseDate, ">", ftype)  # > 201401231
        if headlines  != True :
            comlogging.logger.info('• 2. 모델 훈련과 모델을 생성한다.')
            out = dc_bg004.testModel(modelType, train, headlines)


        comlogging.logger.info("#################################################################" + str(getIntTime()))
    except Exception as err:
        comlogging.logger.error( 'BIG4002_processing '+ str(err) )
        include.setErr('EBIG4002', 'BIG4002_processing,' + str(err))
    else:
        comlogging.logger.info( 'BIG4002_processing-성공')
    finally:
        if include.isError() == False :
            return True
        else :
            return False

def BIG4002_end(tdata) :
    try:
        #------------------------------------------------------------------------------------------------------------
        # 훈련데이타를 파일로 저장한다
        # ------------------------------------------------------------------------------------------------------------
        outfile = include.gcominfo['sysargv'][4]
        outfile = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\input\plt\Combined_News_DJIA.csv'
        outfile = outfile + ".out"
        comutil.file_append( outfile, str(tdata) )


    except Exception as err:
        comlogging.logger.error( 'BIG4002_end '+ str(err))
        include.setErr('EBIG4002', 'BIG4002_end,' + str(err))
    else:
        comlogging.logger.info( 'BIG4002_end-성공')
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
