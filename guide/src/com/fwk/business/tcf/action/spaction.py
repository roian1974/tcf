# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : 각 주요 메인 타스크를 관리하기위해 작성된 모듈
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------

from src.com.fwk.business.util.reflection import reflection

def action(svcname) :

    if svcname == "sp_commo":
        reflection.reflection('src.com.sp_commo.business.pc.sp_commo', 'SP_commo')
    elif svcname == "sp_comrc":
        reflection.reflection('src.com.sp_comrc.business.pc.sp_comrc', 'SP_comrc')
    elif svcname == "sp_pl001":
        reflection.reflection('src.plt.sp_pl001.business.pc.sp_pl001', 'SP_pl001')
    elif svcname == "sp_bg001":
        reflection.reflection('src.big.sp_bg001.business.pc.sp_bg001', 'SP_bg001')
    elif svcname == "sp_bg002":
        reflection.reflection('src.big.sp_bg002.business.pc.sp_bg002', 'SP_bg002')
    elif svcname == "sp_bg003":
        reflection.reflection('src.big.sp_bg003.business.pc.sp_bg003', 'SP_bg003')
    elif svcname == "sp_bg004":
        reflection.reflection('src.big.sp_bg004.business.pc.sp_bg004', 'SP_bg004')
    elif svcname == "sp_bg800":
        reflection.reflection('src.big.sp_bg800.business.pc.sp_bg800', 'SP_bg800')
    elif svcname == "sp_bg901":
        reflection.reflection('src.big.sp_bg901.business.pc.sp_bg901', 'SP_bg901')
    elif svcname == "sp_if001":
        reflection.reflection('src.itf.sp_if001.business.pc.sp_if001', 'SP_if001')
    else:
        raise Exception('Not Service Name')
