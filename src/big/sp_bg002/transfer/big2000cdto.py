import json
from pprint import pprint
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
        pass


class BIG2000CDTO(HEAD):

    indata = dict()
    outdata = dict()
    ddto = dict()

    def __init__(self,servicename,hostprog,userid,tpfq):
        self.servicename = servicename
        self.hostprog = hostprog
        self.tpfq = tpfq
        self.userid = userid
        self.sysdate = comutil.getsysdate()
        self.sysintime = comutil.getsystime()
        self.sysouttime = comutil.getsystime()
        self.hostname = comutil.gethostname()





