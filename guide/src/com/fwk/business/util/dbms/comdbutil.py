import pymysql.cursors
import json
import time
import logging,logging.handlers

from src.com.fwk.business.util.logging import comlogging
from src.com.fwk.business.util.tpm import tpsutil
from src.com.fwk.business.util.common import comutil
from src.com.fwk.business.info import include
# 참고사이트
# https://o7planning.org/en/11463/connecting-mysql-database-in-python-using-pymysql

gdbmsSession = [-1]
ibatisini=''

def dbopen():
    tpsutil.tpenv()
    host = include.gtcfenv['db_host']
    user = include.gtcfenv['db_user']
    password = include.gtcfenv['db_password']
    db = include.gtcfenv['db_dbname']
    rtn = dbinit(host, user, password, db)
    if rtn == -1:
        comlogging.logger.error('dbinit fail')
        return False
    else:
        comlogging.logger.info('dbinit success')

# host='192.168.199.129'
# user = 'root'
# password = '!1974yoe0'
# db = 'o2'
def dbinit(phost,puser,passwd,pdbname):

    rtn = 0
    try :
        global gdbmsSession
        conn = pymysql.connect(host=phost,
                               user=puser,
                               password=passwd,
                               db=pdbname,
                               autocommit=False,
                               charset='utf8mb4')

        include.gdb[0]=conn
        gdbmsSession[0]=conn
    except Exception as err :
        comlogging.logger.error('▲dbinit()-ERR:'+ str(err))
        # include.setErr('EDB004', '함수(dbinit) 에러내용:' + str(err))
        comlogging.logger.error( 'dbinit()-'+ str(err))
        include.gdb[0] = include.FAIL
        gdbmsSession[0] = include.FAIL
        rtn = include.FAIL
    else :
        rtn = include.SUCCESS
        comlogging.logger.info( 'dbinit'+ '성공')
    finally:
        return rtn

def dbinit_conn():

    rtn = 0
    try :

        tpsutil.tpenv()
        phost = include.gtcfenv['db_host']
        puser = include.gtcfenv['db_user']
        passwd = include.gtcfenv['db_password']
        pdb = include.gtcfenv['db_dbname']

        conn = pymysql.connect(host=phost,
                               user=puser,
                               password=passwd,
                               db=pdb,
                               charset='utf8mb4')
        include.gdb[0]=conn
        gdbmsSession[0]=conn
    except Exception as err :
        comlogging.logger.error('▲dbinit()-ERR:'+ str(err))
        comlogging.logger.error( 'dbinit()-'+ str(err))
        rtn = include.FAIL
    else :
        comlogging.logger.info( 'dbinit'+ '성공')
    finally:
        return conn


def dbclose():

	if gdbmsSession[0] != include.FAIL :
		db = gdbmsSession[0]
		db.close()
		comlogging.logger.info('db close')
	else :
		comlogging.logger.error('db connect already failed')


def ibatisload() :
    try :
        rtn = True
        global  ibatisini
        tpsutil.tpenv()
        ibatisini_fname = include.gtcfenv['ibatisini_fname']
        f = open(ibatisini_fname)
        ibatisini = json.load(  f  )
        # comlogging.logger.info(ibatisini)
    except Exception as err:
        comlogging.logger.error('▲ibatisload()-실패-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲ibatisload()-성공:')
        pass
    finally:
        f.close()
        return rtn

def domain_ibatisload(com_name) :
    try :
        rtn = True
        global  ibatisini
        tpsutil.tpenv()
        com_name = "%s_sql.ini" %(com_name)
        com_ibatisini_fname = include.gtcfenv[com_name]
        ibatisini = json.load(open(com_ibatisini_fname))
        # comlogging.logger.info(ibatisini)
    except Exception as err:
        comlogging.logger.error('▲ibatisload()-실패-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲ibatisload()-성공:')
        pass
    finally:
        return rtn

def getsql(id) :
    global ibatisini
    for key1,val1 in ibatisini.items() :
        for val in val1 :
            if id == val['id']:
                sql = val['sql']
                parameter = val['parameter']
                return sql, parameter

    return False,False

def getsql_1(flag,sql_id) :
    global ibatisini
    if flag == 'insert' :
        r = ibatisini['insert']
    elif flag == 'select' :
        r = ibatisini['select']
    elif flag == 'update':
        r = ibatisini['update']
    elif flag == 'delete':
        r = ibatisini['delete']
    else :
        comlogging.logger.error('getsql error')
        return False,False

    for val in r :
        if sql_id == val['id'] :
            sql = val['sql']
            parameter = val['parameter']

            return sql,parameter

    return False, False


def insert(sql,parameter,data) :
    rtn = True
    try:
        global gdbmsSession
        comlogging.logger.info('sql-' + sql)
        comlogging.logger.info('data-len'+len(data))
        conn = gdbmsSession[0]
        cursor = conn.cursor()

        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            rtn = False
            raise Exception('No Data Found')

        comlogging.logger.info(cursor.lastrowid)

    except Exception as err:
        comlogging.logger.error('▲insert()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲insert()-성공:')
    finally:
        cursor.close()
        return rtn


def insert_conn(conn,sql,parameter,data) :
    rtn = True
    try:
        comlogging.logger.info('sql-' + sql)
        comlogging.logger.info('data-len'+len(data))
        cursor = conn.cursor()

        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            rtn = False
            raise Exception('No Data Found')

        comlogging.logger.info(cursor.lastrowid)

    except Exception as err:
        comlogging.logger.error('▲insert()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲insert()-성공:')
    finally:
        cursor.close()
        return rtn

def upsert(sql_id,parameter,data) :
    rtn = True
    try:
        global gdbmsSession
        sql, parameter = getsql(sql_id)
        if sql == False:
            rtn = False
            raise Exception('getsql fail')
        else :
            comlogging.logger.info('sql-' + sql + ':' + str(data))
            conn = gdbmsSession[0]
            cursor = conn.cursor()
            if len(data) > 0 :
                cursor.executemany(sql, data)
            else :
                raise Exception('no data found-1')

    except Exception as err:
        comlogging.logger.error('▲upsert()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲upsert()-성공:')
    finally:
        cursor.close()
        return rtn

def upsert_conn(conn,sql_id,parameter,data) :
    rtn = True
    try:
        sql, parameter = getsql(sql_id)
        if sql == False:
            rtn = False
            raise Exception('getsql fail')
        else :
            comlogging.logger.info('sql-' + sql + ':' + str(data))
            cursor = conn.cursor()
            if len(data) > 0 :
                cursor.executemany(sql, data)
            else :
                raise Exception('no data found-1')

    except Exception as err:
        comlogging.logger.error('▲upsert()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲upsert()-성공:')
    finally:
        cursor.close()
        return rtn

def update(sql,parameter,data) :
    rtn = True
    try:
        global gdbmsSession
        comlogging.logger.info('sql-'+ sql)
        comlogging.logger.info('data-len-'+len(data))
        conn = gdbmsSession[0]
        cursor = conn.cursor()

        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            rtn = False
            raise Exception('no data found-1')

    except Exception as err:
        comlogging.logger.error('▲update()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲update()-성공:')
    finally:
        cursor.close()
        return rtn

def update_conn(conn,sql,parameter,data) :
    rtn = True
    try:
        comlogging.logger.info('sql-'+ sql)
        comlogging.logger.info('data-len-'+len(data))
        cursor = conn.cursor()

        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            rtn = False
            raise Exception('no data found-1')

    except Exception as err:
        comlogging.logger.error('▲update()-ERR:'+ str(err))
        rtn = False
    else:
        comlogging.logger.info('▲update()-성공:')
    finally:
        cursor.close()
        return rtn

def delete(sql,parameter,data) :
    rtn = True
    try:
        global gdbmsSession
        comlogging.logger.info('sql-'+ sql)
        comlogging.logger.info('data-len ' + len(data))
        conn = gdbmsSession[0]
        cursor = conn.cursor()

        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            rtn = False
            raise Exception('no data found')

    except Exception as err:
        comlogging.logger.error('▲delete()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲delete()-성공:')
    finally:
        cursor.close()
        return rtn


def delete_conn(conn,sql,parameter,data) :
    rtn = True
    try:
        comlogging.logger.info('sql-'+ sql)
        comlogging.logger.info('data-len ' + len(data))
        cursor = conn.cursor()

        if len(data) > 0 :
            cursor.executemany(sql, data)
        else :
            rtn = False
            raise Exception('no data found')

    except Exception as err:
        comlogging.logger.error('▲delete()-ERR:' + str(err))
        rtn = False
    else:
        comlogging.logger.info('▲delete()-성공:')
    finally:
        cursor.close()
        return rtn

# sqlid = insert_doc_sentiment_01
def select(sql,parameter) :
    rtn = True
    try:
        global gdbmsSession
        if len(parameter) == 0 :
            pass
        elif len(parameter) == 1 :
            sql = (sql) % (parameter[0])
        elif len(parameter) == 2:
            sql = (sql) % (parameter[0],parameter[1])
        elif len(parameter) == 3:
            sql = (sql) % (parameter[0],parameter[1],parameter[2])
        elif len(parameter) == 4:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3])
        elif len(parameter) == 5:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4])
        elif len(parameter) == 6:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5])
        elif len(parameter) == 7:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5],parameter[6])
        else :
            raise Exception('too many parameters')
            rtn = False

        if rtn == True :
            comlogging.logger.info('sql-'+sql)

            conn = gdbmsSession[0]
            cursor = conn.cursor()

            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()

    except Exception as err:
        comlogging.logger.error('▲select()-ERR:'+ str(err))
        rtn = False
    else:
        # comlogging.logger.info('▲select()-성공:',result)
        pass
    finally:
        cursor.close()
        if rtn == False :
            return False
        else :
            return result

def select_conn(conn,sql,parameter) :
    rtn = True
    try:
        if len(parameter) == 0 :
            pass
        elif len(parameter) == 1 :
            sql = (sql) % (parameter[0])
        elif len(parameter) == 2:
            sql = (sql) % (parameter[0],parameter[1])
        elif len(parameter) == 3:
            sql = (sql) % (parameter[0],parameter[1],parameter[2])
        elif len(parameter) == 4:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3])
        elif len(parameter) == 5:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4])
        elif len(parameter) == 6:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5])
        elif len(parameter) == 7:
            sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5],parameter[6])
        else :
            raise Exception('too many parameters')
            rtn = False

        if rtn == True :
            comlogging.logger.info('sql-'+sql)

            cursor = conn.cursor()

            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()

    except Exception as err:
        comlogging.logger.error('▲select()-ERR:'+ str(err))
        rtn = False
    else:
        # comlogging.logger.info('▲select()-성공:',result)
        pass
    finally:
        cursor.close()
        if rtn == False :
            return False
        else :
            return result


# sqlid = insert_doc_sentiment_01
def select_sqlid(type,sql_id,parameter) :
    rtn = True
    try:
        sql, xparameter = getsql(sql_id)

        if sql == False:
            rtn = False
            raise Exception('getsql failed')

        if len(xparameter) != 0 :
            if len(xparameter) == 0:
                pass
            elif len(xparameter) == 1:
                sql = (sql) % (xparameter[0])
            elif len(xparameter) == 2:
                sql = (sql) % (xparameter[0], xparameter[1])
            elif len(xparameter) == 3:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2])
            elif len(xparameter) == 4:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2], xparameter[3])
            elif len(xparameter) == 5:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2], xparameter[3], xparameter[4])
            elif len(xparameter) == 6:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2], xparameter[3], xparameter[4], xparameter[5])
            elif len(xparameter) == 7:
                sql = (sql) % (
                xparameter[0], xparameter[1], xparameter[2], xparameter[3], xparameter[4], xparameter[5], xparameter[6])
            else:
                rtn = False
                raise Exception('too many parameters')
        else :
            if len(parameter) == 0 :
                pass
            elif len(parameter) == 1 :
                sql = (sql) % (parameter[0])
            elif len(parameter) == 2:
                sql = (sql) % (parameter[0],parameter[1])
            elif len(parameter) == 3:
                sql = (sql) % (parameter[0],parameter[1],parameter[2])
            elif len(parameter) == 4:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3])
            elif len(parameter) == 5:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4])
            elif len(parameter) == 6:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5])
            elif len(parameter) == 7:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5],parameter[6])
            else :
                rtn = False
                raise Exception('too many parameters')

        # comlogging.logger.info('2.sql-'+sql)
        global gdbmsSession
        conn = gdbmsSession[0]
        cursor = conn.cursor()


        cursor.execute("Set Session TRANSACTION ISOLATION LEVEL READ COMMITTED")

        if type == 'fetchall' :
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        elif type == 'fetchmany':
            cursor.execute(sql)
            result = cursor.fetchmany(size=100)
        elif type == 'fetchone' :
            pass
        else :
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
    except Exception as err:
        comlogging.logger.error('▲select_sqlid()-ERR:' + str(err))
        rtn = False
    else:
        # comlogging.logger.info('▲select()-성공:',result)
        pass
    finally:
        cursor.close()
        if rtn == False :
            return False
        else :
            return result


# sqlid = insert_doc_sentiment_01
def select_sqlid_conn(conn,type,sql_id,parameter) :
    rtn = True
    try:
        sql, xparameter = getsql(sql_id)

        if sql == False:
            rtn = False
            raise Exception('getsql failed')

        if len(xparameter) != 0 :
            if len(xparameter) == 0:
                pass
            elif len(xparameter) == 1:
                sql = (sql) % (xparameter[0])
            elif len(xparameter) == 2:
                sql = (sql) % (xparameter[0], xparameter[1])
            elif len(xparameter) == 3:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2])
            elif len(xparameter) == 4:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2], xparameter[3])
            elif len(xparameter) == 5:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2], xparameter[3], xparameter[4])
            elif len(xparameter) == 6:
                sql = (sql) % (xparameter[0], xparameter[1], xparameter[2], xparameter[3], xparameter[4], xparameter[5])
            elif len(xparameter) == 7:
                sql = (sql) % (
                xparameter[0], xparameter[1], xparameter[2], xparameter[3], xparameter[4], xparameter[5], xparameter[6])
            else:
                rtn = False
                raise Exception('too many parameters')
        else :
            if len(parameter) == 0 :
                pass
            elif len(parameter) == 1 :
                sql = (sql) % (parameter[0])
            elif len(parameter) == 2:
                sql = (sql) % (parameter[0],parameter[1])
            elif len(parameter) == 3:
                sql = (sql) % (parameter[0],parameter[1],parameter[2])
            elif len(parameter) == 4:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3])
            elif len(parameter) == 5:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4])
            elif len(parameter) == 6:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5])
            elif len(parameter) == 7:
                sql = (sql) % (parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5],parameter[6])
            else :
                rtn = False
                raise Exception('too many parameters')

        # comlogging.logger.info('2.sql-'+sql)
        cursor = conn.cursor()

        cursor.execute("Set Session TRANSACTION ISOLATION LEVEL READ COMMITTED")

        if type == 'fetchall' :
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        elif type == 'fetchmany':
            cursor.execute(sql)
            result = cursor.fetchmany(size=100)
        elif type == 'fetchone' :
            pass
        else :
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
    except Exception as err:
        comlogging.logger.error('▲select_sqlid()-ERR:' + str(err))
        rtn = False
    else:
        # comlogging.logger.info('▲select()-성공:',result)
        pass
    finally:
        cursor.close()
        if rtn == False :
            return False
        else :
            return result


# 여러개의 데이타를 insert를 수행하는 테스트
def multi_insert_test() :
    dbopen()

    date = comutil.getsysdate()
    time = comutil.getsystime()
    data = [('DO0007', '-0.123456', 'positive', '2017-12-27', 'N', date, time, date, time),
            ('DO0008', '-0.123457', 'positive', '2017-12-28', 'N', date, time, date, time),
            ('D00009', '-0.123458', 'positive', '2017-12-29', 'N', date, time, date, time)]

    # insert('insert_doc_sentiment_01',data)
    sql,parameter = tpsutil.tpbegin_1("insert", "insert_doc_sentiment_01")
    if sql == False:
        comlogging.logger.error('getsql fail')
        return False

    if insert(sql,parameter,data) ==  True :
        comlogging.logger.info('insert success')
        tpsutil.tpcommit()
    else :
        tpsutil.tprollback()

 #   tpsutil.gdbmsSession[0].close()

# 여러개의 데이타를 update를 수행하는 테스트
def multi_update_test() :
    dbopen()

    date = comutil.getsysdate()
    time = comutil.getsystime()
    data = [('Y', date, time, 'DO0007', date),
             ('Y', date, time, 'DO0008', date),
             ('Y', date, time, 'D00009', date)]
    ddata = [('DO0007', date),
             ('DO0008', date),
             ('D00009', date)]
    # insert('insert_doc_sentiment_01',data)
    sql,parameter = tpsutil.tpbegin_1("insert", "update_doc_sentiment_04")
    if sql == False:
        comlogging.logger.error('getsql fail')
        return False

    if update(sql,parameter,data) ==  True :
        comlogging.logger.info('update success')
        tpsutil.tpcommit()
    else :
        tpsutil.tprollback()

#    tpsutil.gdbmsSession[0].close()

def selete_test() :
    dbopen()

    sql,parameter = tpsutil.tpbegin_1("insert", "select_doc_sentiment_06")
    if sql == False:
        comlogging.logger.info('getsql fail')
        return False

    rtn = select(sql, parameter)
    if  rtn ==  False :
        comlogging.logger.error('select fail')
    else :
        comlogging.logger.info('select data-'+ rtn)


def multi_delete_test() :
    dbopen()

    date = comutil.getsysdate()
    time = comutil.getsystime()
    data = [('DO0007', date),
             ('DO0008', date),
             ('D00009', date)]
    # insert('insert_doc_sentiment_01',data)
    sql,parameter = tpsutil.tpbegin_1("insert", "delete_doc_sentiment_07")

    if sql == False:
        comlogging.logger.info('getsql fail')
        return False

    if delete(sql,parameter,data) ==  True :
        comlogging.logger.info('delete success')
        tpsutil.tpcommit()
    else :
        tpsutil.tprollback()

    #tpsutil.gdbmsSession[0].close()


def call_watson(a,b) :
    comlogging.logger.info("---", 'watson call'+ a + b)
    return True

def controller():
    dbopen()


    while True :
        comlogging.logger.info("=============================================================")
        sql, parameter = tpsutil.tpbegin()
        if sql == False:
            comlogging.logger.info('tpbegin fail')
            return False

        time.sleep(5)

        rows = select_sqlid("select_doc_sentiment_06", parameter)
        if rows == False:
            comlogging.logger.info('select fail')
        else:
            comlogging.logger.info('select data-'+ rows)
            cnt = 0
            for row in rows:
                doc_id = row[0]
                cnt += 1
                comlogging.logger.info('=>>'+cnt+'-'+row[0])

                parameter = [doc_id,'N']
                data = select_sqlid("select_doc_sentiment_08",parameter)
                if data == False:
                    comlogging.logger.info('select fail-1')
                    continue
                else:
                    calldata = []

                    kk=0
                    for r in data:
                        calldata.append(r)
                        kk += 1

                        if call_watson(r[0],r[1]) == True:
                            date = comutil.getsysdate()
                            tm = comutil.getsystime()
                            tup = [('DO0007', '-0.123456', 'positive', '2017-12-27', 'N', date, tm, date, tm)]
                            if upsert("insert_doc_sentiment_01", [], tup) == True:
                                comlogging.logger.info('insert success')
                            tup = [('Y', date, tm,  r[0] )]
                            if upsert("update_doc_sentiment_09", [], tup) == True:
                                comlogging.logger.info('update success')

                    tpsutil.tpcommit()

# controller()

# #multi_delete_test()
# multi_insert_test()
# time.sleep(1)
# multi_update_test()
# time.sleep(1)
# selete_test()