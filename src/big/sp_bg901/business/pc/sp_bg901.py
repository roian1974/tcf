from src.com.fwk.business.info import include
from src.big.sp_bg901.business.pc.mod import big9001_분석대상추출 
from src.big.sp_bg901.business.pc.mod import big9002_이벤트후보군데이터추출 
from src.big.sp_bg901.business.pc.mod import big9003_표제어추출 
from src.big.sp_bg901.business.pc.mod import big9004_동사타입변환 
from src.big.sp_bg901.business.pc.mod import big9005_이벤트후보군추출 
from src.big.sp_bg901.business.pc.mod import big9006_예측모델훈련 
from src.big.sp_bg901.business.pc.mod import big9007_모형결과적용
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_bg901():
    try:
        comlogging.logger.info('SJF_SP_bg901 xxxxxxxx')
        hostprog = include.getHostProg()

        if hostprog == 'BIG9001':
            pass
        elif hostprog == 'BIG9002':
            pass
        elif hostprog == 'BIG9003':
            pass
        elif hostprog == 'BIG9004':
            pass
        elif hostprog == 'BIG9005':
            pass
        elif hostprog == 'BIG9006':
            pass
        elif hostprog == 'BIG9007':
            pass
        else:
            include.setErr('EBIG003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

    except Exception as err:
        comlogging.logger.error( 'SJF_SP_bg901-'+ str(err))
        include.setErr('EBIG001', 'SJF_SP_bg901' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_bg901-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True

def EJF_SP_bg901():
    try:
        comlogging.logger.info('EJF_SP_bg901 xxxxxxxx')
        hostprog = include.getHostProg()

        if hostprog == 'BIG9001':
            pass
        elif hostprog == 'BIG9002':
            pass
        elif hostprog == 'BIG9003':
            pass
        elif hostprog == 'BIG9004':
            pass
        elif hostprog == 'BIG9005':
            pass
        elif hostprog == 'BIG9006':
            pass
        elif hostprog == 'BIG9007':
            pass
        else :
            pass

    except Exception as err:
        comlogging.logger.error( 'EJF_SP_bg901' + str(err))
        include.setErr('EBIG002', 'EJF_SP_bg901' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_bg901-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

def SP_bg901():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'BIG9001' :
            big9001_분석대상추출.BIG9001()
        elif hostprog == 'BIG9002' :
            big9002_이벤트후보군데이터추출.BIG9002()
        elif hostprog == 'BIG9003' :
            big9003_표제어추출.BIG9003()
        elif hostprog == 'BIG9004' :
            big9004_동사타입변환.BIG9004()
        elif hostprog == 'BIG9005' :
            big9005_이벤트후보군추출.BIG9005()
        elif hostprog == 'BIG9006' :
            big9006_예측모델훈련.BIG9006()
        elif hostprog == 'BIG9007' :
            big9007_모형결과적용.BIG9007()
        else :
            include.setErr('EBIG003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('EBIG004', 'SP_bg901 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_bg901-' +  str(err))
        include.setErr('EBIG005', 'SP_bg901' + str(err))
    else:
        comlogging.logger.info( 'SP_bg901-성공')
    finally:
        return True

