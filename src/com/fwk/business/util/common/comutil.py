# ----------------------------------------------------------------------------------------------------------------------
# 작성일   : 2018년01월20일
# 모듈내용 : TCF(Transaction Control Function)의 Foundation 모듈
# 작성자   : 로이안 (SK 금융사업1그룹)
# ----------------------------------------------------------------------------------------------------------------------

import os
import re
import time
import sys
import math
import random
import platform
import json
import socket


def gethostname() :
	return socket.gethostname()

def getcwd() :
	return os.getcwd()

def getostype() :
	return platform.system()

def getsysargv() :
	return sys.argv

def getpid() :
	pid = "%08d" % (os.getpid())
	return pid

def getsysdate() :
	now = time.localtime()
	s = "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
	return s

def getsystime() :
	now = time.localtime()
	s = "%02d%02d%02d" % (now.tm_hour, now.tm_min, now.tm_sec)
	return s

def getsysdtme() :
	now = time.localtime()
	s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
	return s

def getsysweek() :
	now = time.localtime()
	week = ('월', '화', '수', '목', '금', '토', '일');
	return week[now.tm_wday]

# 특정 달을 파라미터로 입력하면,
# 그 달에 해당되는 분기가 반환되는 함수
def getquarterYear(month):
  return math.ceil( month / 3.0 )

# 현재 월 반환 함수
def getcurrentMonth():
  now = time.localtime()
  return now.tm_mon # 현재 월만 반환

# 정수형으로 유닉스 타임 출력
def getcurrentInttime() :
	return int(time())

# 지정한 특정 환경변수 출력
def getenviron(type) :
	return os.environ[type]


def getenvirons() :
	# 모든 환경변수 출력
	keys = os.environ.keys()
	keys.sort()
	for item in keys:
		print ("%s=%s" % (item, os.environ[item]))

# strnum = "123"
def getInt(strnum) :
	return int(strnum)

# strnum = "123.456"
def getFloat(strnum) :
	return float(strnum)

# strnum = "999999999999999999999999999999999999999999999"
def getLong(strnum) :
	return long(strnum)

# tochar(33) - a
def tochar(charno) :
	return chr(charno)

# toasc (33)
def toasc(char) :
	return ord(char)

def num2str(num) :
	return str(num)

def fprint(filename,message) :
	pid = getpid()
	lsdtme = getsysdtme()
	print("[%s][%s][%s] %s" % (pid, lsdtme, filename, message));

def str2hex(str) :
	return str.encode("hex")

def hex2str(hexvalue) :
	return hexvalue.decode("hex")

def num2bin(num) :
	return bin(num)

def num2oct(num) :
	return oct(num)

def num2hex(num) :
	return hex(num)

#----------------------------------------------------------------------------------------------------------
# 문자열 관련
#----------------------------------------------------------------------------------------------------------

# 문자열을 구분자로 합친다.
def str2join(gubun,list) :
	return gubun.join(list)
#print ( str2join(',',['rk','sk','ek']))

# 문자열을 분리하여 리스트로 전환
def str2sep2list(gubun,str) :
	return str.split(gubun)

#print( str2sep2list(',','rk,sk,ek'))

# 문자열 포맷터 예
# 위치를 기준으로 한 포맷팅
def str2format() :
	s = "Name: {0}, Age: {1}".format("강수", 30)
	print(s)  # 출력: Name: 강수, Age: 30

	# 필드명을 기준으로 한 포맷팅
	s = "Name: {name}, Age: {age}".format(name="강수", age=30)
	print(s)  # 출력: Name: 강수, Age: 30

	# object의 인덱스 혹은 키를 사용하여 포맷팅
	area = (10, 20)
	s = "width: {x[0]}, height: {x[1]}".format(x=area)
	print(s)  # 출력: width: 10, height: 20

def str2encode() :
	s1 = "A\u00e5"
	s2=s1.encode('utf-8')
	s2.decode('utf-8')

# 문자열을 단어별 카운터
# word_count('but soft what light in yonder window breaks')
def word_count(txt) :
	txt = 'but soft what light in yonder window breaks'
	words = txt.split()

	# 단어와 카운터를 동시에 저장
	t = list()
	for word in words:
		t.append((len(word), word))
		t.sort(reverse=True)

	print(t)
	# [(6, 'yonder'), (6, 'window'), (6, 'breaks'), (5, 'light'), (4, 'what'), (4, 'soft'), (3, 'but'), (2, 'in')]

	# 단어만 리스트에 저장
	res = list()
	for length, word in t:
		res.append(word)

	print(res)


#----------------------------------------------------------------------------------------------------------
# 일반유틸리티
#----------------------------------------------------------------------------------------------------------
def getRandomNum(start_num, end_num) :
	return random.randrange(start_num,end_num,1)


def getLottoNo() :
	num = int(input("lotto 게임 수를 입력하세요 : "))

	print("lotto 자동 번호 입니다.")
	print("----------------------")
	# 입력한 게임 수 만큼 반복
	for x in range(1, num + 1):
		lotto = [0, 0, 0, 0, 0, 0]

		lotto[0] = random.randrange(1, 46, 1)

		lotto[1] = lotto[0]
		lotto[2] = lotto[0]
		lotto[3] = lotto[0]
		lotto[4] = lotto[0]
		lotto[5] = lotto[0]

		# 중복된 수가 발생되지 않도록 채번
		while (lotto[0] == lotto[1]):
			lotto[1] = random.randrange(1, 46, 1)
		while (lotto[0] == lotto[2] or lotto[1] == lotto[2]):
			lotto[2] = random.randrange(1, 46, 1)
		while (lotto[0] == lotto[3] or lotto[1] == lotto[3] or lotto[2] == lotto[3]):
			lotto[3] = random.randrange(1, 46, 1)
		while (lotto[0] == lotto[4] or lotto[1] == lotto[4] or lotto[2] == lotto[4] or lotto[3] == lotto[4]):
			lotto[4] = random.randrange(1, 46, 1)
		while (lotto[0] == lotto[5] or lotto[1] == lotto[5] or lotto[2] == lotto[5] or lotto[3] == lotto[5] or lotto[
			4] == lotto[5]):
			lotto[5] = random.randrange(1, 46, 1)

		# 결과를 정렬
		lotto.sort()

		# 결과 출력
		print(lotto)

def guguDan() :
	print("★ 구구단을 출력합니다.\n")
	for x in range(2, 10): # 2 <= x < 10
		print("------- [" + str(x) + "단] -------")
		for y in range(1, 10):
			print(x, "X", y, "=", x * y)
	print("---------------------")

def prntTree() :
    line = int(input("Tree 의 높이를 입력하세요(5~30) : "))

    for x in range(1, line * 2, 2):
        print((" " * ( (line * 2 - 1 - x) // 2 )) + ("*" * x))

    for y in range(1, 4):
        print(" " * (line-2) + "***")

def prntDiamond() :
    line = int(input("Diamond 의 길이를 입력하세요(2~30) : "))

    for x in range(1, line * 2, 2):
        print((" " * ( (line * 2 - 1 - x) // 2 )) + ("*" * x))

    for y in range(line * 2-3, 0, -2):
        print((" " * ( (line * 2 - 1 - y) // 2 )) + "*" * y)

#----------------------------------------------------------------------------------------------------------
# 클래스 관련
#----------------------------------------------------------------------------------------------------------
def isCheckInstance(o , t) :
	return isinstance(o,t)  # True False

def toUpper(str) :
	return str.upper()

#----------------------------------------------------------------------------------------------------------
# 정규식
#----------------------------------------------------------------------------------------------------------
def isMatch(ostr,term) :
	return re.match(term,ostr)

# re.sub('apple|orange', 'fruit', 'apple box orange tree')    # apple 또는 orange를 fruit로 바꿈
def substr(pattern, t_str, o_str) :
	return re.sub(pattern, t_str, o_str)

#print( '-----' , substr('apple|orangeg', 'fruit', 'apple box orange tree') )

# 숫자만 찾아서 n으로 바꿈
def substr_n2c(char,o_str) :
	return re.sub('[0-9]+', char, o_str)

#print( '-----' , substr_n2c('ee', 'apple2 box3 orange tree') )

# 문자그룹 숫자그룹으로 된 형식을 반복하기
def substr_g2g(t_str) :
	return  re.sub('([a-z]+) ([0-9]+)', '\\2 \\1 \\2 \\1', t_str)

#print( '-----' , substr_g2g('box 222') )

# dic을 '{ "name": "james" }'을 '<name>james</name>' 변환
# ({\s*)
# "(\w+)" --<\\2>
# :
# \s*"(\w+)" --
# (\s*})'
# , '<\\2>\\3</\\2>'

def substr_d2c(str) :
	return re.sub('({\s*)"(\w+)":\s*"(\w+)"(\s*})', '<\\2>\\3</\\2>',str )
#print('----' , substr_d2c('{ "name": "james" }'))



#----------------------------------------------------------------------------------------------------------
# 메시지 출력관련
#----------------------------------------------------------------------------------------------------------
def ferrprint(filename,function,message) :
	pid = getpid()
	lsdtme = getsysdtme()
	print("[%s][%s][%s] ERR:함수[%s][%s]" % (pid, lsdtme, filename, function, message));

def fsusprint(filename,function,message) :
	pid = getpid()
	lsdtme = getsysdtme()
	print("[%s][%s][%s] SUS:함수[%s][%s]" % (pid, lsdtme, filename, function, message));

def allfiles(path):
	res = []
	rtn = 0

	try:
		for root, dirs, files in os.walk(path):
			rootpath = os.path.join(os.path.abspath(path),root)
			for file in files:
				filepath = os.path.join(rootpath,file)
				res.append(filepath)
	except Exception as err:
		ferrprint(__file__, 'allfiles', str(err))
		rtn = -1
	else:
		rr=''
		fsusprint(__file__,'allfiles','성공')
	finally:
		if rtn == -1 :
			print('allfiles call fail')
			return -1
		else :
			print('allfiles call success')
			return res


#------------------------------------
# 일반적인 내용
def dic2lst(dic) :
    #dic = {'a': 10, 'b': 20, 'c': 30}
    l = list()
    for (key,val) in dic.items() :
        l.append((val,key))
    l.sort(reverse=True)
    return l

# 스트링을 dic 타입으로 변경한다.
def str2dic(str) :
	return json.loads(str)

def file_write(filename, text) :
    f = open(filename, 'w',encoding='utf8')
    f.write(text + '\n')
    f.close()

def file_append(filename, text) :
    f = open(filename, 'a',encoding='utf8')
    f.write(text + '\n')
    f.close()
