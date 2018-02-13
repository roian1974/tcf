import threading
import time

class myThread (threading.Thread):
    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        print ("Starting " + self.name)
        print_count(self.name, self.delay, 5)
        print ("Exiting " + self.name)

def print_count(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print ("%s: %d" % (threadName, counter))
        counter -= 1

thread1 = myThread("Thread_1", 1)
thread2 = myThread("Thread_2", 2)

thread1.start()
thread2.start()

print ("Exiting Main Thread")