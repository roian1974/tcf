from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
import timeit

def STF():
    rtn = 0

    try:
        comutil.fprint(__file__, "시스템 일자시간을 가져온다")
        include.gcominfo['com_info']['sysdate'] = comutil.getsysdate()
        include.gcominfo['com_info']['intime'] = comutil.getsystime()
        include.gcominfo['com_info']['outtime'] = comutil.getsystime()

        include.gcominfo['ostype'] = comutil.getostype()
        include.end_timeit = timeit.default_timer()

        comutil.fprint(__file__, "서비스로그파일을 정한다.-일자별처리")
        if include.gcominfo['ostype'] == 'Windows' :
            logfile = "{0}\\{1}.log.{2}".format(include.output_dir,
                                                include.gcominfo['com_info']['svcname'],
                                                include.gcominfo['com_info']['sysdate'])
        else :
            logfile = "{0}/log/{1}.log.{2}".format(include.unix_output_dir,
                                                   include.gcominfo['com_info']['svcname'],
                                                   include.gcominfo['com_info']['sysdate'])

        comutil.fprint(__file__, "인터벌을 초기화하고 로그파일 셋팅")
        include.gcominfo['com_info']['interval'] = 0
        include.gcominfo['com_info']['logfile'] = logfile

    except Exception as err:
        comutil.ferrprint(__file__, 'STF', str(err))
        include.setErr('ECOM002', 'STF Error-' + str(err))
        rtn == -1
    else:
        comutil.fsusprint(__file__, 'STF', '성공')
    finally:
        return rtn

