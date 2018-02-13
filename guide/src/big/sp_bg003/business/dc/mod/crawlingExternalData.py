from src.com.fwk.business.util.logging import comlogging


def excute() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲excute()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲excute()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False
