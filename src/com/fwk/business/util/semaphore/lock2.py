import time
import os
import json
import signal
from multiprocessing import Queue
import threading

# https://blog.naver.com/shumin/220919388654

g_cnt=0
myLock = threading.Lock()

NumberOfThread = 5
# 실행중인 Thread 갯수
ThreadsLeft = NumberOfThread


def f1() :
    thread_list = []
    arg=1
    thread = threading.Thread(target=exe, args=(arg,))
    thread.start()
    thread_list.append(thread)

    arg=2
    thread2 = threading.Thread(target=exe, args=(arg,))
    thread2.start()
    thread_list.append(thread2)

    arg=3
    thread3 = threading.Thread(target=exe, args=(arg,))
    thread3.start()
    thread_list.append(thread3)

    arg=4
    thread4 = threading.Thread(target=exe, args=(arg,))
    thread4.start()
    thread_list.append(thread4)

    for thread in thread_list:
        thread.join

def exe(arg) :

    cnt=0
    while True :
        time.sleep(arg)
        cnt += 1
        if cnt ==10 :
            break

        myLock.acquire()
        try :
            g_cnt = arg
            print(arg, '-thread:', g_cnt)
        except Exception as err:
            print(err)
        finally:
            myLock.release()

# Thread 종료처리 함수
def threadexit(id):
    global ThreadsLeft
    print ('thread %d is quitting' % id)
    myLock.acquire()
    ThreadsLeft -= 1
    myLock.release()


f1()



