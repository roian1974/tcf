from src.com.fwk.business.util.common import comutil

class HEAD :
    servicename=''
    hostprog=''
    userid=''
    tpfq=0
    hostname=''
    sysdate=''
    sysintime=''
    sysouttime=''

    def __init__(self):
        self.sysdate = comutil.getsysdate()
        self.sysintime = comutil.getsystime()
        self.sysouttime = comutil.getsystime()
        self.hostname = comutil.gethostname()


