from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
from src.ded.sp_de001.business.pc.mod import ded1001, ded1002, ded1003


def SJF_SP_de001():
    rtn = include.SUCCESS
    try:
        pass
    except Exception as err:
        comutil.ferrprint(__file__, 'SJF_SP_de001', str(err))
        include.setErr('EDED002', 'SJF_SP_de001' + str(err))
    else:
        comutil.fsusprint(__file__, 'SJF_SP_de001', '성공')
    finally:
        if rtn == include.FAIL:
            return include.FAIL
        else:
            return include.SUCCESS


def EJF_SP_de001():
    rtn = include.SUCCESS
    try:
        pass
    except Exception as err:
        comutil.ferrprint(__file__, 'EJF_SP_de001', str(err))
        include.setErr('EDED003', 'EJF_SP_de001' + str(err))
    else:
        comutil.fsusprint(__file__, 'EJF_SP_de001', '성공')
    finally:
        if rtn == include.FAIL:
            return include.FAIL
        else:
            return include.SUCCESS


def SP_de001():
    rtn = include.SUCCESS
    hostprog = include.gcominfo['com_info']['hostprog']

    try:
        if hostprog == 'DED1001' :
            ded1001.DED1001()
        elif hostprog == 'DED1002' :
            ded1002.DED1002()
        elif hostprog == 'DED1003':
            ded1003.DED1003()
        else :
            include.setErr('EDED004', 'HOSTPROG을 설정하지 않았다')
            return include.FAIL

        if include.gcominfo['err_info']['finalcd'][0] == 'E':
            include.setErr('EDED005', 'SP_de001 수행중 오류발생')
            return include.FAIL

    except Exception as err:
        comutil.ferrprint(__file__, 'SP_de001', str(err))
        include.setErr('EDED001', 'SP_de001' + str(err))
    else:
        comutil.fsusprint(__file__, 'SP_de001', '성공')
    finally:
        return include.SUCCESS

