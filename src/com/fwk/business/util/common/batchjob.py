#!/usr/bin/env python

import workerpool

def test_print(x):
        print (x)

pool = workerpool.WorkerPool(size=8)

pool.map(test_print, range(0, 1000000))

pool.shutdown()
pool.wait()