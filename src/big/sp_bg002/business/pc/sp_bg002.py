from src.com.fwk.business.info import include
from src.big.sp_bg002.business.pc.mod import big2000, big2001, big2002, big2003
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_bg002():
    try:
        comlogging.logger.info('SJF_SP_bg002 xxxxxxxx')
        pass
    except Exception as err:
        comlogging.logger.error( 'SJF_SP_bg002-'+ str(err))
        include.setErr('EBIG001', 'SJF_SP_bg002' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_bg002-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True


def EJF_SP_bg002():
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'EJF_SP_bg002' + str(err))
        include.setErr('EBIG002', 'EJF_SP_bg002' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_bg002-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

# 실행방식
# sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv LogisR 20150101
# sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv NaiveEyes 20150101
# python tcf_sp_commo.py sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv NaiveEyes 20150101
# python tcf_sp_commo.py sp_bg002 BIG2002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv NaiveEyes 20141231

# python tcf_sp_commo.py sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv RF 20150101
# python tcf_sp_commo.py sp_bg002 BIG2002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv RF 20141231

# python tcf_sp_commo.py sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv SVMGusian 20150101
# python tcf_sp_commo.py sp_bg002 BIG2002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv SVMGusian 20141231

# python tcf_sp_commo.py sp_bg002 BIG2001 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv SVMLinear 20150101
# python tcf_sp_commo.py sp_bg002 BIG2002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv SVMLinear 20141231

# sp_bg002 BIG2002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv LogisR 20141231
# sp_bg002 BIG2002 C:\jDev\MyWorks\PycharmProjects\Roian\log\input\\big\Full_Data.csv NaiveEyes 20141231

# 모델 = [LogisR, NaiveEyes, RF, SVMGusian, SVMLinear]

def SP_bg002():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'BIG2000' :
            big2000.BIG2000()
        elif hostprog == 'BIG2001' :
            big2001.BIG2001()  # 전처리 과정과 훈련모델를 생성하는 과정
        elif hostprog == 'BIG2002' :
            big2002.BIG2002()  # 훈련모델을 가지고 테스팅하는 단계
        elif hostprog == 'BIG2003' :
            big2003.BIG2003()
        else :
            include.setErr('EBIG003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('EBIG004', 'SP_bg002 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_bg002-' +  str(err))
        include.setErr('EBIG005', 'SP_bg002' + str(err))
    else:
        comlogging.logger.info( 'SP_bg002-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

