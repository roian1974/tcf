
for 변수 in 리스트(또는 튜플, 문자열):
    수행할 문장1
    수행할 문장2
    ...

1. 전형적인 for문

>>> test_list = ['one', 'two', 'three']
>>> for i in test_list:
...     print(i)
...
one
two
three


2. 다양한 for문의 사용

>>> a = [(1,2), (3,4), (5,6)]
>>> for (first, last) in a:
...     print(first + last)
...
3
7
11

# marks1.py
marks = [90, 25, 67, 45, 80]

number = 0
for mark in marks:
    number = number +1
    if mark >= 60:
        print("%d번 학생은 합격입니다." % number)
    else:
        print("%d번 학생은 불합격입니다." % number)

# marks2.py
marks = [90, 25, 67, 45, 80]

number = 0
for mark in marks:
    number = number +1
    if mark < 60: continue
    print("%d번 학생 축하합니다. 합격입니다. " % number)

>>> a = range(10)
>>> a
range(0, 10)

>>> sum = 0
>>> for i in range(1, 11):
...     sum = sum + i
...
>>> print(sum)
55

>>> for i in range(2,10):
...     for j in range(1, 10):
...         print(i*j, end=" ")
...     print('')
...
2 4 6 8 10 12 14 16 18
3 6 9 12 15 18 21 24 27
4 8 12 16 20 24 28 32 36
5 10 15 20 25 30 35 40 45
6 12 18 24 30 36 42 48 54
7 14 21 28 35 42 49 56 63
8 16 24 32 40 48 56 64 72
9 18 27 36 45 54 63 72 81


# key 를 가져온다.
>>> ages = {'siwa': 33, 'sunshine': 29, 'tom': 27}
>>> for key in ages.keys():  # keys() 생략 가능
...     print(key)
...
siwa
sunshine
tom

# value를 가져온다.
>>> for value in ages.values():
...     print(value)
...
33
29
27

key와 value 둘 다 가져올 수 있다.
>>> for key, value in ages.items():
...     print('{}의 나이는 {}입니다'.format(key, value))
...
siwa의 나이는 33입니다
sunshine의 나이는 29입니다
tom의 나이는 27입니다

def dic2lst(dic) :
    d = {'a': 10, 'b': 20, 'c': 30}
    l = list()
    for (key,val) in d.items() :
        l.append((key,val))
    l.sort(reverse=True)
    print(l)


or 변수 in 리스트(또는 튜플, 문자열):
    수행할 문장1
    수행할 문장2

출처: http://kanonxkanon.tistory.com/2294 [Monochrome :)]