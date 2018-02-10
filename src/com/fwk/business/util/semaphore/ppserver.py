import sys,threading
import pp

class myTest :
    def __init__(self):
        self.value = 0
        self.lock = thread.allocate_lock()

    def result(self,value):
        self.lock.acquire()
        self.value +=value
        self.lock.release()


def mysum(n):
    result =0
    for i in range(1,1000):
        result += i
    return result

sum = myTest()
ppserver = ppservers =("*",)
job_server = pp.Server(ppservers=ppservers)

job1 = job_server.submit(mysum,(100),callback=sum.result)
job_server.print_stats()


