from src.com.fwk.business.util.logging import comlogging


def 형태소분리() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲형태소분리()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲형태소분리()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def 불용어처리() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲불용어처리()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲불용어처리()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def 중요도검사_TFIDF() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲중요도검사_TFIDF()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲중요도검사_TFIDF()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def 중요단어선정() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲중요단어선정()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲중요단어선정()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def 매체별중요단어포함현황체킹() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲매체별중요단어포함현황체킹()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲매체별중요단어포함현황체킹()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False


def 학습모델도출() :
    try:
        rtn = True
    except Exception as err:
        comlogging.logger.error('▲학습모델도출()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲학습모델도출()-성공:')
    finally:
        if rtn == True:
            return True
        else:
            return False
