from src.com.fwk.business.info import include
from src.big.sp_bg002.business.pc.mod import big2000, big2001, big2002, big2003
from src.com.fwk.business.util.logging import comlogging


def SJF_SP_bg002():
    try:
        comlogging.logger.info('SJF_SP_bg002 call')
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

def SP_bg002():

    hostprog = include.getHostProg()

    try:
        if hostprog == 'BIG2000' :
            big2000.BIG2000()
        elif hostprog == 'BIG2001' :
            big2001.BIG2001()
        elif hostprog == 'BIG2002' :
            big2002.BIG2002()
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

