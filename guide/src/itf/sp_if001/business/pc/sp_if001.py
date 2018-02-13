from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging
from src.itf.sp_if001.business.pc.mod import itf1001, itf1000, itf1002

#-----------------------------------------------------------------------------------------------------------------------
# Wastson 관련 인터페이스 담당하는 컴포넌트 서비스 ... sk c&c roian..2018-02-01
#-----------------------------------------------------------------------------------------------------------------------

def SJF_SP_if001():
    return True

def EJF_SP_if001():
    return True

def SP_if001():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'ITF1000' :
            itf1000.ITF1000()
        elif hostprog == 'ITF1001' :
            itf1001.ITF1001()
        elif hostprog == 'ITF1002' :
            itf1002.ITF1002()
        else :
            include.setErr('EITF003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('EITF004', 'SP_commo 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_if001-' +  str(err))
        include.setErr('EITF005', 'SP_if001' + str(err))
    else:
        comlogging.logger.info( 'SP_if001-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

