import pymysql.cursors
import sys
import logging
import re
from json_patch import *



# 데이터베이스 생성
# CREATE DATABASE o2 CHARACTER SET utf8 COLLATE utf8_general_ci;


def create_database() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234qwer',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'CREATE DATABASE roiandb'
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()

# create_database()


def create_table() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234qwer',
                           db='roiandb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = '''
                CREATE TABLE users (
                    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    email varchar(255) NOT NULL,
                    password varchar(255) NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8
                '''
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()

#create_table()

def insert_data_01() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234qwer',
                           db='roiandb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'INSERT INTO users (email, password) VALUES (%s, %s)'
            cursor.execute(sql, ('test@test.com', 'my-passwd'))
        conn.commit()
        print(cursor.lastrowid)
        # 1 (last insert id)

        i=2
        while i < 5 :
            i += 1
            email = 'test%02d@test.com' % (i)
            passwd = 'my-passwd%02d' % (i)

            with conn.cursor() as cursor:
                sql = 'INSERT INTO users (email, password) VALUES (%s, %s)'
                cursor.execute(sql, (email, passwd))

        conn.commit()
        print(cursor.lastrowid)


    finally:
        conn.close()

# insert_data_01()

def select_data_01() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234qwer',
                           db='roiandb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM users WHERE email = %s'
            cursor.execute(sql, ('test@test.com',))
            result = cursor.fetchone()
            print(result)
            # (1, 'test@test.com', 'my-passwd')
    finally:
        conn.close()

#select_data_01()

def select_data_02() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234qwer',
                           db='roiandb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'INSERT INTO users (email, password) VALUES (%s, %s)'
            cursor.execute(sql, ('your@test.com', 'your-passwd'))
        conn.commit()

        with conn.cursor() as cursor:
            sql = 'SELECT * FROM users'
            cursor.execute(sql)
            result = cursor.fetchall()
            #print(result)
            # ((1, 'test@test.com', 'my-passwd'), (2, 'your@test.com', 'your-passwd'))
    finally:
        conn.close()
        return result

def select_data_03() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234qwer',
                           db='roiandb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM users'
            cursor.execute(sql)
            result = cursor.fetchall()
            #print(result)
            # ((1, 'test@test.com', 'my-passwd'), (2, 'your@test.com', 'your-passwd'))
    finally:
        conn.close()
        return result

tp = select_data_03()
for val in tp :
    id = val[0];   email = val[1];    passwd = val[2]
    print("id=%d email=%s passwd=%s" % (id,email,passwd) )


def update_data_02() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password=None,
                           db='roiandb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'UPDATE users SET email = %s WHERE email = %s'
            cursor.execute(sql, ('my@test.com', 'test@test.com'))
        conn.commit()
        print(cursor.rowcount)  # 1 (affected rows)
    finally:
        conn.close()

def delete_data() :
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234qwer',
                           db='roiandb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'DELETE FROM users WHERE email = %s'
            cursor.execute(sql, ('my@test.com',))
        conn.commit()
        print(cursor.rowcount)  # 1 (affected rows)
    finally:
        conn.close()


# !/usr/bin/env python
# -*- coding: utf8 -*-

class DBConnection:

    def __init__(self):
        self.data_idx = 0
        self.data_array = []
        self.data_list = {'seq': 1, 'prec_id': '', 'title': '', 'content': '', 'etc': ''}
        self.insert_count = 0
        self.fail_count = 0

    def __enter__(self):
        self.conn = pymysql.connect(host='000.000.000.000', port=8080, user='hyunminseo', password='hyunminseo',
                                    db='db_name', charset='utf8')
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.conn.close()

    def InsertDB(self, target_tbl):
        try:
            sql = 'insert into %s(SEQ, ID, TITLE, CONTENT, ETC) values (%s, %s, %s, %s, %s)' % (target_tbl)
            self.cursor.execute(sql,
                                (int(self.data_list['seq']),
                                 self.data_list['id'].strip('\r\n'),
                                 self.data_list['title'].strip('\r\n'),
                                 self.data_list['content'].strip('\r\n'),
                                 self.data_list['etc'].strip('\r\n')))
            # self.conn.commit()
        except Exception as e:
            self.fail_count += 1
            logging.debug('# Insert DB error : %s, %s' % (self.data_list['seq'], e))

    def DynamicInsertDB(self, target_tbl):
        total = len(self.data_array)
        if total != 500:
            logging.debug('# data_array length check : %s' % (total))
        fail = 0
        try:
            sql = 'insert into %s(SEQ, ID, TITLE, CONTENT, ETC) values (%s, %s, %s, %s, %s)' % (target_tbl)
            if len(self.data_array) > 0:
                self.cursor.executemany(sql, self.data_array)
            else:
                return False
            self.conn.commit()
        except Exception as e:
            fail += 1
            self.fail_count += 1
            logging.debug('# Insert DB error : %s, %s' % (self.data_list['seq'], e))
        self.insert_count += total - fail

    def CountDB(self, target_tbl):
        try:
            sql = "select count(*) from %s" % (target_tbl)
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            logging.debug('# %s table count : %s' % (target_tbl, rs[0]))
        except Exception as e:
            logging.debug('# Select count(*) error : %s' % (e))

    def SelectDB(self, target_tbl):
        try:
            sql = "select * from %s" % (target_tbl)
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            for row in rs:
                print
                dump_json(row)
        except Exception as e:
            logging.debug('# Select DB error : %s' % (e))

    def DeleteDB(self, target_tbl):
        try:
            sql = "delete from %s" % (target_tbl)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logging.debug('# Delete DB error : %s' % (e))

    def Run(self, input_file):

        with open(input_file) as f:
            for line in f:
                '''
                데이터 처리하는 소스
        
                '''
                proc += 1
                if proc % 1000 == 0:
                    logging.debug('# %s docs is finished' % proc)

                else:
                    self.InsertDB()
                    # self.DumpData()
                    seq += 1
                    self.data_list = {'seq': seq, 'prec_id': '', 'title': '', 'content': '', 'etc': ''}
            else:
                temp += line

        self.AddByType(tag_type, temp)
        self.InsertDB()
        # self.DumpData()
        try:
            ## InserDB()를 사용할 경우 일괄 commit
            self.conn.commit()
        except Exception as e:
            logging.error('# Commit error : %s' % (e))

    logging.debug('# Total %s docs, Fail %s docs' % (proc, self.fail_count))


def DumpData(self):
    for k in self.data_list.keys():
        self.data_list[k] = self.data_list[k].strip('\r\n')
    # print dump_json(self.data_list, ind="\t")
    print
    self.data_list['seq'] + '\t' + self.data_list['prec_id']


def DumpData2(self):
    for k in self.data_array:
        # print str(k[0])+'\t'+'\t'.join(k[1:])
        print
        str(k[0]) + '\t' + k[1]


#
# main
#
# if __name__ == '__main__':
#
#     reload(sys)
#     sys.setdefaultencoding('utf8')
#     logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
#
#     if len(sys.argv) == 2:
#         input_file = sys.argv[1]
#     else:
#         logging.info('usage) %s input_file_path' % sys.argv[0])
#         logging.info('   ex) %s input_file.txt' % sys.argv[0])
#         sys.exit(-1)
#
#     with DBConnection() as db_conn:
#         db_conn.DeleteDB()
#         # db_conn.SelectDB()
#         db_conn.Run(input_file)
#         db_conn.CountDB()
#
#     sys.exit(0)
#
