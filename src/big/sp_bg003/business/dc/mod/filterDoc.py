from src.com.fwk.business.util.logging import comlogging


def 본문없는기사제거() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲본문없는기사제거()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲본문없는기사제거()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False

def 중복기사제거() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲중복기사제거()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲중복기사제거()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def 종합성기사제거() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲종합성기사제거()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲종합성기사제거()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def 부가정보매핑() :
    try:

        rtn = True
        # 업종/법인/사업자번호 추가

    except Exception as err:
        comlogging.logger.error('▲부가정보매핑()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲부가정보매핑()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False
