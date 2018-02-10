import json
from src.com.fwk.util import incdbutil
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include


def ibatisload() :
    incdbutil.ibatisini = json.load(open('C:\jDev\MyWorks\PycharmProjects\Roian\ibatis\sql.ini'))
    # pprint(incdbutil.ibatisini)

def getsql(flag,id) :
    if flag == 'insert' :
        r = incdbutil.ibatisini['insert']
    elif flag == 'select' :
        r = incdbutil.ibatisini['select']
    elif flag == 'update':
        r = incdbutil.ibatisini['update']
    else :
        return -1

    for val in r :
        if id == val['id'] :
            sql = val['sql']
            parameter = val['parameter']
            return sql,parameter
    return 'not match'


# sqlid = insert_doc_sentiment_01
def insert(sql_id,data) :
    try:
        tpsutil.tpenv()
        host = include.gtcfenv['db_host']
        user = include.gtcfenv['db_user']
        password = include.gtcfenv['db_password']
        db = include.gtcfenv['db_dbname']
        rtn = tpsutil.dbinit(host, user, password, db)
        if rtn == -1:
            print('dbinit fail')
            return False
        else:
            print('dbinit success')

        ibatisload()
        sql,parameter = getsql("insert",sql_id)
        if sql == 'not':
            print('getsql fail')
            return False
        print('sql-',sql)
        print('data-len',len(data))
        conn = tpsutil.gdbmsSession[0]
        cursor = conn.cursor()
        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            cursor.close()
            conn.close()
            return False
        conn.commit()
        print(cursor.lastrowid)

    except Exception as err:
        print('▲insert()-ERR:', str(err))
    else:
        print('▲insert()-성공:')
    finally:
        cursor.close()
        conn.close()

# sqlid = insert_doc_sentiment_01
def update(sql_id,data) :
    try:
        tpsutil.tpenv()
        host = include.gtcfenv['db_host']
        user = include.gtcfenv['db_user']
        password = include.gtcfenv['db_password']
        db = include.gtcfenv['db_dbname']
        rtn = tpsutil.dbinit(host, user, password, db)
        if rtn == -1:
            print('dbinit fail')
            return False
        else:
            print('dbinit success')

        ibatisload()
        sql,parameter = getsql("insert",sql_id)
        if sql == 'not':
            print('getsql fail')
            return False
        print('sql-',sql)
        print('data-len',len(data))
        conn = tpsutil.gdbmsSession[0]
        cursor = conn.cursor()
        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            cursor.close()
            conn.close()
            return False
        conn.commit()
        print(cursor.lastrowid)

    except Exception as err:
        print('▲update()-ERR:', str(err))
    else:
        print('▲update()-성공:')
    finally:
        cursor.close()
        conn.close()


date = comutil.getsysdate()
time = comutil.getsystime()
data = [('DO0001','-0.123456','positive','2017-12-27','N',date,time,date,time),
        ('DO0002','-0.123457','positive','2017-12-27','N',date,time,date,time),
        ('D00003','-0.123458','positive','2017-12-27','N',date,time,date,time)]

insert('insert_doc_sentiment_01',data)


# ibatisload()
# sql,parameter = getsql('insert','insert_doc_sentiment_01')
# if sql == 'not' :
#     print('fail')
# else :
#     print(sql,parameter)
#

