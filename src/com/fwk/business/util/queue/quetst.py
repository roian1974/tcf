try:
    import threading
except ImportError:
    import dummy_threading as threading
    
import pymysql.cursors
import time
from src.com.fwk.business.util.queue import queue


def worker():
    while True:
        print('worker ... waiting')
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

def do_work(item):
    print("do_work start --")
    print(item)

def dbinit(phost,puser,passwd,pdbname):

    rtn = 0
    try :
        global gdbmsSession
        conn = pymysql.connect(host=phost,
                               user=puser,
                               password=passwd,
                               db=pdbname,
                               charset='utf8mb4')
    except Exception as err :
        print('▲dbinit()-ERR:'+ str(err))
        print( 'dbinit()-'+ str(err))
    else :
        print( 'dbinit'+ '성공')
    finally:
        return conn


q = queue.Queue()
threads = []
num_worker_threads = 2
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    print("queue start b--")
    t.start()
    print("queue start a--")

    threads.append(t)
print('------s1')
source = [1,2]

host='169.56.68.67'
user = 'root'
password = ''
db = 'o2'

for item in source:
    print('-----q b')
    conn = dbinit(host,user,password,db)
    q.put(conn)
    time.sleep(3)
    print('-----q a')

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)

for t in threads:
    t.join()
    

