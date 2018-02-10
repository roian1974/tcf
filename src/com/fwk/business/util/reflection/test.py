from src.com.fwk.business.util.reflection import test2


def getAction(svcname) :
    return

def foo(aa) :
    return aa

print( locals()['foo'](11) )

call = getattr(test2,'a')  #test2 모듈의 a 함수를 호출한다.
result = call('1111')
print(result)


