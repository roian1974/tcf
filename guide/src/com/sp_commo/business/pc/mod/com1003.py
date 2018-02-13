#=+ coding: utf-8 -*-
import os
import xlrd
import re
import pymysql
from src.com.fwk.business.info import include


# 엑셀파일을 읽어서 원하는 데이터를 추출하는 방법

def allfiles(path) :
    res = []
    for root, dirs, files in os.walk(path) :
        rootpath = os.path.join(os.path.abspath(path),root)
        for file in files :
            filepath = os.path.join(rootpath, file)
            res.append(filepath)
    return res


def doing():
    filenames = allfiles("C:\jDev\MyWorks\PycharmProjects\Roian\log\input")

    print(filenames)
    no = 1
    for filename in filenames :
        open_file = xlrd.open_workbook(filename)
        try :
            open_workssheet_name = open_file.sheet_by_name("파우더룸")
        except:
            continue

        bigcategory = os.path.splitdrive(filename)
        # print(filename, bigcategory)
        bigcategory = bigcategory[1].split('\\')
        # print(filename, bigcategory)
        bigcategory = bigcategory[2]
        # print('-',filename, bigcategory)

        print('-',filename)
        category = os.path.splitext(filename)
        # print('2',category)
        category = os.path.split(category[0])
        # print('3',category)
        category = category[1]
        print('4',category)

        no_cate = open_workssheet_name.col_values(0)
        print('no_cate',no_cate)
        product = open_workssheet_name.col_values(1)
        print('product',product)
        img = open_workssheet_name.col_values(2)
        print('img',img)
        score = open_workssheet_name.col_values(3)
        reviewnum = open_workssheet_name.col_values(4)
        positive = open_workssheet_name.col_values(6)
        negative = open_workssheet_name.col_values(7)
        print('negative',negative)

        # curs = include.gdb[0].cursors()
        for i in range(len(no_cate)) :
            no_cate[i] = int(no_cate[i])
            product[i] = re.sub("[\n]",'',product[i])
            sql = "insert into bigdata(no,no_cate,bigcategory,category,product,img,score,review_num,positieve,negative) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # curs.execute(sql, (no,no_cate[i],bigcategory.encode('utf-8'),category.encode('utf-8'),positive[i].encode('utf-8'),negative[i].encode('utf-8')))
            # print (no, no_cate[i], bigcategory.encode('utf-8'), category.encode('utf-8'), positive[i].encode('utf-8'),negative[i].encode('utf-8'))
            print(no, no_cate[i], bigcategory, category, product[i],img[i],reviewnum[i],positive[i], negative[i])
            no += 1

doing()
