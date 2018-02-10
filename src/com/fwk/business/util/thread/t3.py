from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

def g(x):

    return x[0]*x[1]

if __name__ == '__main__':
    pool = Pool(processes=4)              # start 4 worker processes

    # print "[0, 1, 4,..., 81]"
    print (pool.map(f, range(10)))

    time.sleep(4)


    # print same numbers in arbitrary order
    for i in pool.imap_unordered(f, range(10)):
        print (i)

    # evaluate "f(20)" asynchronously
    res = pool.apply_async(f, (20,))      # runs in *only* one process
    print (res.get(timeout=1))              # prints "400"

    # evaluate "os.getpid()" asynchronously
    res = pool.apply_async(os.getpid, ()) # runs in *only* one process
    print (res.get(timeout=1))              # prints the PID of that process

    time.sleep(5)
    print("------------------------------------------------------------")
    # launching multiple evaluations asynchronously *may* use more processes
    r2ow = [1,2,3,4]
    multiple_results = [pool.apply_async(r2ow, ()) for i in range(4)]
    print ([res.get(timeout=1) for res in multiple_results])
    print("------------------------------------------------------------")
    time.sleep(5)



    # make a single worker sleep for 10 secs
    res = pool.apply_async(time.sleep, (10,))
    try:
        print (res.get(timeout=1))
    except TimeoutError:
        print ("We lacked patience and got a multiprocessing.TimeoutError")