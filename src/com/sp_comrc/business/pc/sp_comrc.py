from src.com.fwk.business.info import include
from src.com.fwk.business.util.logging import comlogging

from src.com.sp_comrc.business.pc.mod import com9001, com9000, com9002, com9003, com8000, com8001


def SJF_SP_comrc():
    return True

def EJF_SP_comrc():
    return True

def SP_comrc():

    hostprog = include.getHostProg()

    try:

        if hostprog == 'COM9000' :
            com9000.COM9000()
        elif hostprog == 'COM9001' :
            com9001.COM9001()
        elif hostprog == 'COM9002' :
            com9002.COM9002()
        elif hostprog == 'COM9003' :
            com9003.COM9003()
        elif hostprog == 'COM8000' :
            com8000.COM8000()
        elif hostprog == 'COM8001' :
            com8001.COM8001()

        else :
            include.setErr('ECOM003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('ECOM004', 'SP_commo 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_comrc-' +  str(err))
        include.setErr('ECOM005', 'SP_comrc' + str(err))
    else:
        comlogging.logger.info( 'SP_comrc-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

