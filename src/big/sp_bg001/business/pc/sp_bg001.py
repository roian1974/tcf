from src.com.fwk.business.info import include
from src.big.sp_bg001.business.pc.mod import big1000, big1001, big1002, big1003, big1004, big1005
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_bg001():
    try:
        comlogging.logger.info('SJF_SP_bg001 call')
        pass
    except Exception as err:
        comlogging.logger.error( 'SJF_SP_bg001-'+ str(err))
        include.setErr('EBIG001', 'SJF_SP_bg001' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_bg001-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True


def EJF_SP_bg001():
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'EJF_SP_bg001' + str(err))
        include.setErr('EBIG002', 'EJF_SP_bg001' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_bg001-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

def SP_bg001():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'BIG1000' :
            big1000.BIG1000()
        elif hostprog == 'BIG1001' :
            big1001.BIG1001()
        elif hostprog == 'BIG1002' :
            big1002.BIG1002()
        elif hostprog == 'BIG1003' :
            big1003.BIG1003()
        elif hostprog == 'BIG1004' :
            big1004.BIG1004()
        elif hostprog == 'BIG1005' :
            big1005.BIG1005()
        else :
            include.setErr('EBIG003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('EBIG004', 'SP_bg001 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_bg001-' +  str(err))
        include.setErr('EBIG005', 'SP_bg001' + str(err))
    else:
        comlogging.logger.info( 'SP_bg001-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

