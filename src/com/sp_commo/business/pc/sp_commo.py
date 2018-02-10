from src.com.fwk.business.info import include
from src.com.sp_commo.business.pc.mod import com1001, com1000, com1002, com1005
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_commo():
    try:
        comlogging.logger.info('SJF_SP_commo xxxxxxxx')
        print('====')
        pass
    except Exception as err:
        comlogging.logger.error( 'SJF_SP_commo-'+ str(err))
        include.setErr('ECOM001', 'SJF_SP_commo' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_commo-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True


def EJF_SP_commo():
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'EJF_SP_commo' + str(err))
        include.setErr('ECOM002', 'EJF_SP_commo' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_commo-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

def SP_commo():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'COM1000' :
            com1000.COM1000()
        elif hostprog == 'COM1001' :
            com1001.COM1001()
        elif hostprog == 'COM1002' :
            com1002.COM1002()
        elif hostprog == 'COM1005' :
            com1005.COM1005()
        else :
            include.setErr('ECOM003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('ECOM004', 'SP_commo 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_commo-' +  str(err))
        include.setErr('ECOM005', 'SP_commo' + str(err))
    else:
        comlogging.logger.info( 'SP_commo-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

