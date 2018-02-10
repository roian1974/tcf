import signal



# 각각의 signal에 대한 핸들러
def sighandler(signum, frame):
    ''' 시그널 처리 '''
    raise Exception("Signal. %i" % signum)


# signal 수신 함수
def register_all_signal():
    ''' 모든 시그널 등록 '''
    for x in dir(signal):
        if not x.startswith("SIG"):
            continue

        try:
            signum = getattr(signal, x)
            signal.signal(signum, sighandler)
        except:
            # signal 등록에 실패하는 경우 표시
            print('Skipping the signal : %s' % x)
            continue


# signal을 수신하는 function 실행
register_all_signal()