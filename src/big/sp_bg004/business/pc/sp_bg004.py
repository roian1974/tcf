from src.com.fwk.business.info import include
from src.big.sp_bg004.business.pc.mod import big4000, big4001, big4002, big4003
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_bg004():
    try:
        comlogging.logger.info('SJF_SP_bg004 xxxxxxxx')
        pass
    except Exception as err:
        comlogging.logger.error( 'SJF_SP_bg004-'+ str(err))
        include.setErr('EBIG001', 'SJF_SP_bg004' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_bg004-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True


def EJF_SP_bg004():
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'EJF_SP_bg004' + str(err))
        include.setErr('EBIG002', 'EJF_SP_bg004' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_bg004-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

def SP_bg004():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'BIG4000' :
            big4000.BIG4000()
        elif hostprog == 'BIG4001' :
            big4001.BIG4001()
        elif hostprog == 'BIG4002' :
            big4002.BIG4002()
        elif hostprog == 'BIG4003' :
            big4003.BIG4003()
        else :
            include.setErr('EBIG003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('EBIG004', 'SP_bg004 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_bg004-' +  str(err))
        include.setErr('EBIG005', 'SP_bg004' + str(err))
    else:
        comlogging.logger.info( 'SP_bg004-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

