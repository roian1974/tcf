from src.com.fwk.business.util.logging import comlogging


def 긍부정기사분리() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲긍부정기사분리()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲긍부정기사분리()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False
