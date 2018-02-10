from src.com.fwk.business.info import include
from src.big.sp_bg003.business.pc.mod import big3000_외부데이타수집
from src.big.sp_bg003.business.pc.mod import big3001_데이타검증
from src.big.sp_bg003.business.pc.mod import big3002_전처리
from src.big.sp_bg003.business.pc.mod import big3003_훈련모형
from src.big.sp_bg003.business.pc.mod import big3004_예측
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_bg003():
    try:
        comlogging.logger.info('SJF_SP_bg003 xxxxxxxx')
        pass
    except Exception as err:
        comlogging.logger.error( 'SJF_SP_bg003-'+ str(err))
        include.setErr('EBIG001', 'SJF_SP_bg003' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_bg003-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True


def EJF_SP_bg003():
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'EJF_SP_bg003' + str(err))
        include.setErr('EBIG002', 'EJF_SP_bg003' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_bg003-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

def SP_bg003():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'BIG3000' :
            big3000_외부데이타수집.BIG3000()
        elif hostprog == 'BIG3001' :
            big3001_데이타검증.BIG3001()
        elif hostprog == 'BIG3002' :
            big3002_전처리.BIG3002()
        elif hostprog == 'BIG3003' :
            big3003_훈련모형.BIG3003()
        elif hostprog == 'BIG3004' :
            big3004_예측.BIG3004()
        else :
            include.setErr('EBIG003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('EBIG004', 'SP_bg003 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_bg003-' +  str(err))
        include.setErr('EBIG005', 'SP_bg003' + str(err))
    else:
        comlogging.logger.info( 'SP_bg003-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

