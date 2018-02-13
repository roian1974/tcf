import time
import pymysql
from sqlalchemy import pool, create_engine
import sys
import mysql.connector as mysql





loop = 5000
dsn = { 'host':'169.56.68.67', 'db':'o2', 'user':'root', }

def test(drvname):

    engine = create_engine('mysql+%s://root@169.56.68.67/o2' % drvname.lower(), pool_size=3, max_overflow=0)

    s = time.time()

    for _ in range(loop):

        conn = engine.connect()

        conn.execute('SELECT SLEEP(0.001)')

        conn.close()

    drvname = 'mysql  ' if drvname == 'mysqlconnector' else drvname

    print('sqlalchemy+%s: %f sec' % (drvname, time.time() - s))



for drvname in ['pymysql', 'MySQLdb', 'mysqlconnector']:

    test(drvname)

    time.sleep(1)





def test1(drv):

    drvname = drv.__name__

    if drvname == 'mysql.connector':

        drvname = 'mysql  '

        _dsn = dsn.copy()

        _dsn['buffered'] = True

    else:

        _dsn = dsn



    mypool = pool.QueuePool(lambda: drv.connect(**_dsn), pool_size=3, max_overflow=0)

    s = time.time()

    for _ in range(loop):

        conn = mypool.connect()

        cursor = conn.cursor()

        cursor.execute('SELECT SLEEP(0.001)')

        cursor.close()

        conn.close()

    print('sqlalchemy(only pool)+%s: %f sec' % (drvname, time.time() - s))




mypool = mysql.pooling.MySQLConnectionPool(pool_name = 'mypool', pool_size=3, buffered=True, **dsn)

s = time.time()

for _ in range(loop):

    conn = mypool.get_connection()

    cursor = conn.cursor()

    cursor.execute('SELECT SLEEP(0.001)')

    cursor.close()

    conn.close()

print('mysql.connector.pool: %f sec' % (time.time() - s))