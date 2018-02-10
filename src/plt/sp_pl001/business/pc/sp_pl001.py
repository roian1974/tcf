from src.com.fwk.business.info import include
from src.plt.sp_pl001.business.pc.mod import plt1000,plt1001,plt1002
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_pl001():
    try:
        comlogging.logger.info('SJF_SP_pl001 xxxxxxxx')
        pass
    except Exception as err:
        comlogging.logger.error( 'SJF_SP_pl001-'+ str(err))
        include.setErr('ECOM001', 'SJF_SP_pl001' + str(err))
    else:
        comlogging.logger.info( 'SJF_SP_pl001-성공')
    finally:

        if include.isError() == True :
            return False
        else:
            return True


def EJF_SP_pl001():
    try:
        pass
    except Exception as err:
        comlogging.logger.error( 'EJF_SP_pl001' + str(err))
        include.setErr('ECOM002', 'EJF_SP_pl001' + str(err))
    else:
        comlogging.logger.info( 'EJF_SP_pl001-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

def SP_pl001():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'PLT1000' :
            plt1000.PLT1000()
        elif hostprog == 'PLT1001' :
            plt1001.PLT1001()
        elif hostprog == 'PLT1002' :
            plt1002.PLT1002()
        else :
            include.setErr('ECOM003', 'Host Proam을 설정하지 않았다')
            raise Exception('Host Program을 설정하지 않았습니다.')

        if include.isError() == True :
            include.setErr('ECOM004', 'SP_pl001 수행중 오류발생')

    except Exception as err:
        comlogging.logger.error( 'SP_pl001-' +  str(err))
        include.setErr('ECOM005', 'SP_pl001' + str(err))
    else:
        comlogging.logger.info( 'SP_pl001-성공')
    finally:
        if include.isError() == True :
            return False
        else:
            return True

