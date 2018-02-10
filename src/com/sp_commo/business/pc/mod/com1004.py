
# 감성어 사전 구축 http://jjssoolee.tistory.com/5?category=693132

import os
from konlpy.tag import Twitter
from konlpy.utils import pprint
import collections
import time
import xlrd
import xlwt
import re
from xlutils.copy import copy


def allfiles(path) :
    res = []
    for root, dirs, files in os.walk(path) :
        rootpath = os.path.join(os.path.abspath(path),root)
        for file in files :
            filepath = os.path.join(rootpath, file)
            res.append(filepath)
    return res

def doing() :
    filenames = allfiles("C:\jDev\MyWorks\PycharmProjects\Roian\log\input")
    spliter = Twitter()
    nouns = []
    return_list = []

    # print(filenames)
    no = 1
    for filename in filenames :
        print(filename)
        open_file = xlrd.open_workbook(filename)
        try :
            open_workssheet_name = open_file.sheet_by_name("파우더룸2")
        except:
            continue

        reviews = open_workssheet_name.col_values(11)
        print(reviews)
        t=1
        for review in reviews :
            print(review)
            review = re.sub('[n\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]','',review).strip()
            emogi_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F" # emotion
                                       u"\U0001F300-\U0001F55F" # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF" # transport & map symbos
                                       u"\U0001F1E0-\U0001F1FF"  # flags
                                        "]" , flags =re.UNICODE)
            review = emogi_pattern.sub(r'',review)
            nouns.append(spliter.nouns(review))
            t = t+1

        c = collections.Counter()
        for nouns in nouns :
            c.update(nouns)

        for n,c in c.most_common(3000):
            temp = 'tag: ' +  n +', count: ' + str(c) + "\n"
            return_list.append(temp)

        output_file = open("noun2.txt",'w',encoding="utf-8")
        for l in return_list :
            output_file.write(l)

        output_file.close()


doing()





