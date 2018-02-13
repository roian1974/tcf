from src.com.fwk.business.util.logging import comlogging


def 모형검증() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲모형검증()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲모형검증()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False
