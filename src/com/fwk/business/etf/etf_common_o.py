import timeit
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include


def ETF():
    rtn = 0
    try:
        comutil.fprint(__file__, "프로세스 종료시간을 설정한다")

        setInterval()
        comutil.fprint(__file__, "인터벌은 " + include.gcominfo['com_info']['interval'])

        comutil.fprint(__file__, "로그를 저장합니다")
        ETF_logging()

    except Exception as err:
        comutil.ferrprint(__file__, 'ETF', str(err))
        include.setErr('ECOM003', 'ETF Error-' + str(err))
    else:
        comutil.fsusprint(__file__, 'ETF', '성공')
    finally:
        return 0

def ETF_logging() :

    print('filename=='+ include.getLogFile()+ '----'+ str(include.gcominfo))
    comutil.file_append(include.getLogFile(), str(include.gcominfo))
    return

def setInterval() :
    include.end_timeit = timeit.default_timer()
    include.gcominfo['com_info']['interval'] = ('%f' % (include.end_timeit - include.start_timeit))

