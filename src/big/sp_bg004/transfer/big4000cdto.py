import json
from pprint import pprint
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import head

class BIG4000CDTO(head.HEAD):
    indata = dict()
    outdata = dict()
    ddto = dict()

    def __init__(self,servicename,hostprog,userid,tpfq):
        self.servicename = servicename
        self.hostprog = hostprog
        self.tpfq = tpfq
        self.userid = userid





