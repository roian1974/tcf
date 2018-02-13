import threading
import time

class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print ("Starting " + self.name)
        startTime = int(time.time())
        countdown(100000000)
        endTime = int(time.time())
        print (self.name, "의 작업시간", (endTime-startTime))
        print ("Exiting " + self.name)
        print()

def countdown(n):
    while n > 0:
        n = n-1;

thread1 = myThread("Thread_1")

startTime = int(time.time())
thread1.start()

thread1.join()

print ("Exiting Main Thread")
endTime = int(time.time())
print("총 작업 시간", (endTime - startTime))