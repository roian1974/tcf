from src.com.fwk.business.info import include
from src.big.sp_bg800.business.pc.mod import big8000, big8001, big8002, big8003
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_bg800():
    try:
        comlogging.logger.info('SJF_SP_bg800 xxxxxxxx')
        pass
    except Exception as err:
        comlogging.logger.error( 'SJF_SP_bg800-'+ str(err))
        include.setErr('EBIG001', 'SJF_SP_bg800' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_bg800-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True


def EJF_SP_bg800():
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'EJF_SP_bg800' + str(err))
        include.setErr('EBIG002', 'EJF_SP_bg800' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_bg800-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

def SP_bg800():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'BIG8000' :
            big8000.BIG8000()
        elif hostprog == 'BIG8001' :
            big8001.BIG8001()  # 전처리 과정과 훈련모델를 생성하는 과정
        elif hostprog == 'BIG8002' :
            big8002.BIG8002()  # 훈련모델을 가지고 테스팅하는 단계
        elif hostprog == 'BIG8003' :
            big8003.BIG8003()
        else :
            include.setErr('EBIG003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('EBIG004', 'SP_bg800 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_bg800-' +  str(err))
        include.setErr('EBIG005', 'SP_bg800' + str(err))
    else:
        comlogging.logger.info( 'SP_bg800-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

