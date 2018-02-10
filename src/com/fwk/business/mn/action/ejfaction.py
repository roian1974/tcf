# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 메인엔진에서 각 작업관리자에 대한 사전작업을 진행하기 위해서 작성된 모듈
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------

from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.reflection import reflection


def action(svcname) :

    if svcname == "sp_commo" :
        if reflection.reflection('src.com.sp_commo.business.pc.sp_commo', 'EJF_SP_commo') == False:
            comlogging.logger.error("EJF_SP_commo() call failed")
            return False
        else:
            comlogging.logger.info( "EJF_SP_commo() call success")
        return True
    elif svcname == "sp_comrc" :
        if reflection.reflection('src.com.sp_comrc.business.pc.sp_comrc', 'EJF_SP_comrc') == False:
            comlogging.logger.error("EJF_SP_comrc() call failed")
            return False
        else:
            comlogging.logger.info( "EJF_SP_comrc() call success")
        return True
    else :
        return True
